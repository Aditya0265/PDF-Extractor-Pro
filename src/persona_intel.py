from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any, Tuple
import re
import os

import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class RankedBlock:
    document: str
    page_number: int
    text: str
    score: float


def _clean_text(s: str) -> str:
    s = s or ""
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _extract_page_blocks(pdf_path: str, min_chars: int = 60) -> List[Tuple[int, str]]:
    blocks: List[Tuple[int, str]] = []
    with pdfplumber.open(pdf_path) as pdf:
        for idx, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            text = text.strip()
            if len(text) >= min_chars:
                blocks.append((idx, text))
    return blocks


def run_persona_intelligence(
    pdf_path: str,
    persona_name: str,
    job_task: str,
    top_k: int = 8,
    min_chars: int = 60,
) -> Dict[str, Any]:
    """Run a lightweight Challenge-1B-like semantic ranking over a SINGLE PDF.

    - Extracts per-page text blocks using pdfplumber
    - Builds a TF-IDF model over blocks
    - Scores blocks against query = persona + task
    - Returns a JSON-friendly dict similar to 1B outputs
    """

    persona_name = persona_name.strip() if persona_name else "Generic User"
    job_task = job_task.strip() if job_task else ""
    query = _clean_text(f"{persona_name} {job_task}")

    page_blocks = _extract_page_blocks(pdf_path, min_chars=min_chars)
    if not page_blocks:
        return {
            "metadata": {
                "persona": persona_name,
                "job_to_be_done": job_task,
                "input_documents": [pdf_path],
            },
            "extracted_sections": [],
            "subsection_analysis": [],
            "warning": "No readable text blocks were extracted (PDF may be scanned/images or protected).",
        }

    texts = [_clean_text(t) for _, t in page_blocks]

    # TF-IDF: keep it small & fast
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=30000,
        ngram_range=(1, 2),
    )
    X = vectorizer.fit_transform(texts)
    q = vectorizer.transform([query])

    scores = cosine_similarity(X, q).reshape(-1)

    ranked = sorted(
        [
            RankedBlock(
                document=os.path.basename(pdf_path),
                page_number=page_no,
                text=texts[i],
                score=float(scores[i]),
            )
            for i, (page_no, _) in enumerate(page_blocks)
        ],
        key=lambda b: b.score,
        reverse=True,
    )

    ranked = ranked[: max(1, int(top_k))]

    extracted_sections = []
    subsection_analysis = []
    for rank, b in enumerate(ranked, start=1):
        # section title: first sentence-ish
        title = b.text.split("\n")[0]
        title = re.sub(r"\s+", " ", title).strip()
        if len(title) > 110:
            title = title[:110] + "…"

        refined = _summarize_2_sentences(b.text)

        extracted_sections.append(
            {
                "document": b.document,
                "section_title": title if title else f"Relevant Section (Page {b.page_number})",
                "importance_rank": rank,
                "page_number": b.page_number,
                "score": round(b.score, 6),
            }
        )
        subsection_analysis.append(
            {
                "document": b.document,
                "refined_text": refined,
                "page_number": b.page_number,
                "score": round(b.score, 6),
            }
        )

    return {
        "metadata": {
            "persona": persona_name,
            "job_to_be_done": job_task,
            "input_documents": [os.path.basename(pdf_path)],
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis,
    }


def _summarize_2_sentences(text: str) -> str:
    text = re.sub(r"\s+", " ", (text or "")).strip()
    if not text:
        return ""
    # naive sentence split (fast, offline)
    sents = re.split(r"(?<=[.!?])\s+", text)
    if len(sents) >= 2:
        return " ".join(sents[:2]).strip()
    return text[:4000]
