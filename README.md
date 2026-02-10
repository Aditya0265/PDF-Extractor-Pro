# 🔍 DocSense

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Status](https://img.shields.io/badge/Status-Active-success)

> **Understand Your Documents. Instantly.**

------------------------------------------------------------------------

## 📌 Overview

**DocSense** is a document intelligence platform that extracts, analyzes, and transforms PDF files into actionable insights — all from a single browser interface.

It combines classical PDF parsing, ML-powered structure detection, readability scoring, persona-driven semantic ranking, and PII redaction into one unified tool. Everything runs **locally and offline** — no API keys, no cloud dependencies, no data leaving your machine.

### What It Demonstrates

- PDF text, image, and table extraction with OCR fallback
- Document hierarchy detection via font-based KMeans clustering
- Readability analysis using 4 standard formulas (Flesch, Gunning Fog, Coleman-Liau)
- Persona-driven semantic ranking using TF-IDF + Cosine Similarity
- Regex-based PII detection and permanent PDF redaction
- Multilingual translation support
- Professional Streamlit web interface with 10-tab dashboard

------------------------------------------------------------------------

## 🧠 System Workflow

```
PDF Upload
   ↓
Text + Image + Table Extraction (with OCR fallback)
   ↓
Document Structure Detection (KMeans on font sizes)
   ↓
Readability Scoring (Flesch, Fog, Coleman-Liau)
   ↓
Persona + Task Mapping → Semantic Ranking (TF-IDF)
   ↓
PII Detection + Redaction (Regex + Pattern Matching)
   ↓
Export (TXT, JSON, XLSX, ZIP, Redacted PDF)
```

------------------------------------------------------------------------

## 🚀 Features

### 📑 PDF Extraction Engine

- Full text extraction from multi-page PDFs
- Embedded image extraction with ZIP download
- Table detection and extraction via pdfplumber
- OCR fallback for scanned/image-only pages (Tesseract)
- Encrypted PDF support (password input)

------------------------------------------------------------------------

### 🧠 Structure Detection

- Automatic title detection from metadata or content
- Heading hierarchy (H1–H3) via KMeans clustering on font sizes
- Bold text filtering and deduplication
- Generates a semantic outline (table of contents) from raw PDF

------------------------------------------------------------------------

### 📖 Readability Analysis

- **Flesch Reading Ease** — overall readability score (0–100) with color-coded display
- **Flesch-Kincaid Grade Level** — U.S. school grade equivalent
- **Gunning Fog Index** — years of education needed to understand the text
- **Coleman-Liau Index** — character-based grade level estimate
- Word count, sentence count, average sentence length
- Estimated reading time (200 WPM baseline)
- Complexity breakdown — simple vs complex words (3+ syllables) with visual bar
- Human-friendly labels (e.g., "Difficult (College Level)")

> All formulas implemented from scratch in pure Python — no external NLP libraries.

------------------------------------------------------------------------

### 🌍 Universal Reader (Translation)

- Side-by-side original and translated text
- 5 supported languages: Spanish, French, German, Hindi, Chinese
- Powered by Google Translator (via `deep-translator`)

------------------------------------------------------------------------

### 🛡️ PDF Redaction Tool

- Permanently blacks out matched text using PyMuPDF's redaction API
- **Custom keywords** — enter any words/phrases to redact (one per line)
- **5 built-in PII patterns:**
    - Email addresses
    - Phone numbers
    - Dates (DD/MM/YYYY)
    - URLs
    - Currency amounts ($, £, €, ₹)
- **Custom regex** — supply your own pattern for advanced use cases
- Per-page redaction count with bar chart visualization
- Download the redacted PDF directly

------------------------------------------------------------------------

### 👤 Persona AI (Semantic Ranking)

- Define a persona (e.g., "Legal Analyst") and a task (e.g., "Find compliance clauses")
- TF-IDF vectorization with bigrams across all pages
- Cosine similarity scoring against persona+task query
- Returns top-K most relevant pages ranked by score
- Exportable as structured JSON

------------------------------------------------------------------------

### 📊 Visual Analysis

- Word Cloud generation from extracted text
- Dark-themed visualization matching the app's UI

------------------------------------------------------------------------

### 🖼️ Image Gallery

- Grid display of all extracted images
- Individual image captions
- Bulk download as ZIP

------------------------------------------------------------------------

### 📦 Export Hub

| Format | Contents |
|--------|----------|
| `.txt` | Full extracted text |
| `.json` | Document structure + metadata |
| `.xlsx` | Extracted tables (one sheet per table) |
| `.zip` | All extracted images |
| `.pdf` | Redacted document |
| `.json` | Persona AI ranked results |

------------------------------------------------------------------------

### 💻 Web Interface

- Built with Streamlit (wide layout, collapsed sidebar)
- Custom CSS dark theme with glassmorphism cards
- Google Material Symbols icons
- 10-tab dashboard in logical flow:

```
Metadata → Structure → Readability → Reader → Redact → Persona AI → Tables → Visuals → Gallery → Export
```

- Progress bar during PDF processing
- Session state persistence across tab switches

------------------------------------------------------------------------

## 🛠 Tech Stack

| Category | Libraries |
|----------|-----------|
| **Frontend** | Streamlit, Custom CSS, Google Material Icons |
| **PDF Parsing** | PyMuPDF (fitz), pdfplumber |
| **Machine Learning** | scikit-learn (TF-IDF, Cosine Similarity, KMeans) |
| **Readability** | Custom Python (Flesch, Fog, Coleman-Liau formulas) |
| **OCR** | pytesseract, Pillow (optional — requires Tesseract) |
| **Translation** | deep-translator (Google Translate wrapper) |
| **Visualization** | Matplotlib, WordCloud |
| **Data Handling** | Pandas, NumPy, openpyxl |
| **Containerization** | Docker |

------------------------------------------------------------------------

## 📂 Project Structure

```
DocSense/
│
├── app.py                  # Main Streamlit application (UI + tab routing)
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker containerization
├── README.md
│
├── src/
│   ├── __init__.py
│   ├── extractor.py        # PDF text, image, table extraction + OCR + translation
│   ├── persona_intel.py    # Persona-based semantic ranking (TF-IDF + cosine)
│   ├── readability.py      # Readability scoring (4 indices + text stats)
│   ├── redactor.py         # PII detection + PDF redaction (regex + PyMuPDF)
│   └── utils.py            # File I/O, PDF validation, cleanup
│
├── downloads/              # Output directory (generated at runtime)
└── temp_uploads/           # Temporary upload storage (auto-cleaned)
```

------------------------------------------------------------------------

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/Aditya0265/DocSense.git
cd DocSense
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate:

```bash
# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. (Optional) Install Tesseract for OCR

- **Windows:** Download from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) and add to PATH
- **Mac:** `brew install tesseract`
- **Linux:** `sudo apt install tesseract-ocr`

------------------------------------------------------------------------

## ▶️ Run Application

```bash
python -m streamlit run app.py
```

Open in browser:

```
http://localhost:8501
```

------------------------------------------------------------------------

## 🧪 Use Cases

| Scenario | Tabs Used |
|----------|-----------|
| Assess if a research paper is too advanced for students | Readability |
| Find compliance-relevant sections in a 200-page contract | Persona AI |
| Strip names and emails before sharing a document externally | Redact |
| Extract financial tables from an annual report into Excel | Tables → Export |
| Skim a foreign-language paper to decide if it's worth translating | Reader |
| Pull all figures from a technical manual | Gallery → Export |
| Generate a table of contents for a PDF that lacks bookmarks | Structure |
| Get a quick thematic overview of a long document | Visuals |

------------------------------------------------------------------------

## ⚠️ Limitations

- **Semantic ranking uses TF-IDF** — no deep understanding of synonyms or paraphrasing. "financial risk" won't match "monetary exposure" unless those exact words appear.
- **Readability formulas are English-only** — syllable counting uses English vowel patterns. Results for non-English text are unreliable.
- **Structure detection is heuristic** — KMeans on font sizes works well for structured documents but breaks down with single-font or decorative-font PDFs.
- **Redaction is text-layer only** — text in embedded images or flattened scans won't be caught. OCR output isn't fed into the redaction pipeline.
- **Translation truncates at 5000 characters** — long documents show `[Truncated]`. No chunked full-document translation.
- **No batch processing** — one PDF at a time. No multi-file comparison or bulk redaction.
- **No persistence** — results live in Streamlit session state. Refreshing the browser resets everything.
- **Large PDFs are slow** — sequential page-by-page processing with no parallelism.

------------------------------------------------------------------------

## 📌 Future Scope

- **Vector database (FAISS/ChromaDB)** — replace TF-IDF with sentence embeddings for true semantic search
- **LLM integration** — extractive/abstractive summarization, natural language Q&A over documents
- **Named Entity Recognition (spaCy NER)** — auto-detect PERSON, ORG, MONEY entities for smarter redaction
- **Batch processing** — upload multiple PDFs, cross-document similarity heatmap
- **Multilingual readability** — language-specific formulas (Fernández-Huerta for Spanish, LIX for Scandinavian)
- **Full-document translation** — chunked progressive translation with progress bar
- **Structured export** — Markdown/HTML reports preserving headings, highlights, and scores
- **Cloud deployment** — Docker + AWS/GCP with auth, persistent storage, and job queuing
- **PDF annotation** — highlight and bookmark sections with SQLite persistence

------------------------------------------------------------------------

## 👤 Author

**Aditya** — [GitHub](https://github.com/Aditya0265)

------------------------------------------------------------------------
