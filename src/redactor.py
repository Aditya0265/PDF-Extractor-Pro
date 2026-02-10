"""
PDF Redaction Module
---------------------
Redacts sensitive content from PDFs by drawing black rectangles
over matched text. Supports custom keywords, emails, phone numbers,
and common PII patterns.
"""

import re
import os
import fitz  # PyMuPDF


# --- Pre-built regex patterns for common PII ---
PATTERNS = {
    "Email Addresses": r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",
    "Phone Numbers": r"(\+?\d{1,3}[\s\-]?)?(\(?\d{2,4}\)?[\s\-]?)?\d{3,5}[\s\-]?\d{4}",
    "Dates (DD/MM/YYYY)": r"\b\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4}\b",
    "URLs": r"https?://[^\s,)]+",
    "Currency Amounts": r"[\$\£\€\₹]\s?\d[\d,]*\.?\d*",
}


def get_available_patterns() -> dict:
    """Return the dictionary of built-in PII patterns."""
    return PATTERNS.copy()


def redact_pdf(
    input_path: str,
    output_path: str,
    keywords: list = None,
    pattern_keys: list = None,
    custom_regex: str = None,
) -> dict:
    """
    Redact a PDF by blacking out matched text.

    Args:
        input_path:   Path to the source PDF.
        output_path:  Path where the redacted PDF will be saved.
        keywords:     List of exact keywords/phrases to redact.
        pattern_keys: List of keys from PATTERNS dict to apply.
        custom_regex: An optional user-supplied regex string.

    Returns:
        dict with redaction stats:
            - total_redactions: int
            - per_page: list of {page, count}
            - patterns_used: list of str
            - output_path: str
    """
    keywords = keywords or []
    pattern_keys = pattern_keys or []

    doc = fitz.open(input_path)

    # Build list of (label, compiled_regex) to search
    search_items = []

    # 1) Exact keywords (case-insensitive, word-boundary)
    for kw in keywords:
        kw = kw.strip()
        if kw:
            search_items.append((f"Keyword: {kw}", re.compile(re.escape(kw), re.IGNORECASE)))

    # 2) Built-in patterns
    for key in pattern_keys:
        if key in PATTERNS:
            search_items.append((key, re.compile(PATTERNS[key])))

    # 3) Custom regex
    if custom_regex and custom_regex.strip():
        try:
            search_items.append(("Custom Pattern", re.compile(custom_regex.strip())))
        except re.error:
            pass  # silently ignore invalid regex

    total_redactions = 0
    per_page = []
    patterns_used = list(set(label for label, _ in search_items))

    for page_num in range(len(doc)):
        page = doc[page_num]
        page_count = 0

        for label, pattern in search_items:
            # Get all text on page to find regex matches
            text = page.get_text("text")
            matches = pattern.finditer(text)

            for match in matches:
                matched_text = match.group()
                # Find all instances of this matched text on the page
                instances = page.search_for(matched_text)
                for inst in instances:
                    # Add a filled black rectangle redaction annotation
                    page.add_redact_annot(inst, fill=(0, 0, 0))
                    page_count += 1

        # Apply all redactions on this page at once
        if page_count > 0:
            page.apply_redactions()

        total_redactions += page_count
        per_page.append({"page": page_num + 1, "count": page_count})

    doc.save(output_path)
    doc.close()

    return {
        "total_redactions": total_redactions,
        "per_page": per_page,
        "patterns_used": patterns_used,
        "output_path": output_path,
    }
