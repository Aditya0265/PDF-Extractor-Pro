# 📄 PDF Extractor Pro


![Python](https://img.shields.io/badge/Python-3.x-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Status](https://img.shields.io/badge/Status-Active-success)


------------------------------------------------------------------------

## 📌 Overview

**PDF Extractor Pro** is an enhanced document intelligence tool designed
to extract structured content from PDF files and perform persona-driven
semantic document analysis.

The system combines classical PDF parsing, document structure detection,
and lightweight machine learning-based semantic ranking to help users
quickly identify relevant sections of documents based on user roles and
job tasks.

This project demonstrates practical implementation of: - PDF text and
image extraction - Document hierarchy detection - Semantic document
ranking - Interactive Streamlit-based user interface

------------------------------------------------------------------------

## 🧠 System Workflow

    PDF Upload
       ↓
    Text + Image Extraction
       ↓
    Document Structure Detection
       ↓
    Persona + Task Mapping
       ↓
    Semantic Ranking (TF-IDF + Cosine Similarity)
       ↓
    Structured Results + Export

------------------------------------------------------------------------

## 🚀 Key Features

### 📑 Advanced PDF Extraction

-   Extract full text from PDFs
-   Extract embedded images
-   Handles multi-page documents
-   OCR support for scanned PDFs (if Tesseract is installed)

------------------------------------------------------------------------

### 🧠 Document Structure Intelligence

-   Title detection
-   Heading detection (H1--H3 approximation)
-   Font-based clustering using KMeans
-   Converts raw PDFs into structured document representation

------------------------------------------------------------------------

### 👤 Persona-Based Document Intelligence

-   Persona-driven semantic search
-   TF-IDF document vectorization
-   Cosine similarity-based section ranking
-   Persona + Task → Relevant Document Sections mapping
-   JSON-style structured outputs

------------------------------------------------------------------------

### 🌍 Multilingual Support

-   Google Translator wrapper support
-   Helps analyze documents in multiple languages

------------------------------------------------------------------------

### 📊 Text Analytics

-   Word Cloud generation
-   Basic data visualization using Matplotlib
-   Quick document theme understanding

------------------------------------------------------------------------

### 📦 Export & Output Management

-   Structured output folders
-   Extracted images ZIP download
-   Extracted text export
-   Temporary file cleanup

------------------------------------------------------------------------

### 💻 Professional Web Interface

-   Built using Streamlit
-   Custom CSS dark theme
-   Clean upload → analyze → download workflow

------------------------------------------------------------------------

## 🛠 Tech Stack

### Core

-   Python 3.x
-   Streamlit

### PDF Processing

-   PyMuPDF (fitz)
-   pdfplumber

### Machine Learning

-   Scikit-learn
    -   TF-IDF Vectorizer
    -   Cosine Similarity
    -   KMeans Clustering

### NLP & Processing

-   WordCloud
-   Regex
-   Unicode normalization

### OCR (Optional)

-   Tesseract OCR
-   pytesseract

### Data & Visualization

-   Pandas
-   NumPy
-   Matplotlib
-   Pillow

------------------------------------------------------------------------

## 📂 Typical Project Structure

    PDF-Extractor-Pro/
    │
    ├ app.py
    ├ requirements.txt
    │
    ├ src/
    │ ├ extractor.py
    │ ├ persona_engine.py
    │ ├ utils.py
    │
    ├ downloads/
    ├ uploads/

------------------------------------------------------------------------

## ⚙️ Installation

### 1️⃣ Clone Repository

    git clone <repo-url>
    cd PDF-Extractor-Pro

------------------------------------------------------------------------

### 2️⃣ Create Virtual Environment (Recommended)

    python -m venv venv

Activate:

Windows:

    venv\Scripts\activate

Mac / Linux:

    source venv/bin/activate

------------------------------------------------------------------------

### 3️⃣ Install Dependencies

    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt

------------------------------------------------------------------------

## ▶️ Run Application

    python -m streamlit run app.py

Open browser:

    http://localhost:8501

------------------------------------------------------------------------

## 🧪 Example Use Cases

-   Research paper analysis
-   Policy document review
-   Business document filtering
-   Academic document intelligence demos
-   Hackathon and portfolio demonstration

------------------------------------------------------------------------

## ⚠️ Limitations

-   Uses TF-IDF (not deep LLM semantic reasoning)
-   OCR accuracy depends on scan quality
-   Structure detection is heuristic-based
-   Very large PDFs may increase processing time

------------------------------------------------------------------------

## 📌 Future Improvements

-   Vector database (FAISS) integration
-   LLM reasoning layer
-   Multi-document semantic search
-   Auto summarization
-   Cloud deployment support

------------------------------------------------------------------------


