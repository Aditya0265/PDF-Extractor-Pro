import os
import fitz  # PyMuPDF
import unicodedata
import numpy as np
import pdfplumber
import pandas as pd
import pytesseract
from PIL import Image
from collections import defaultdict
from sklearn.cluster import KMeans
from deep_translator import GoogleTranslator

# NOTE: If Tesseract is not in your PATH, you might need to uncomment and set this:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def analyze_structure(doc):
    """
    Analyzes the document to extract a semantic outline (Title, H1-H3).
    """
    font_scores = defaultdict(int)
    heading_candidates = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict").get("blocks", [])

        for b in blocks:
            for line in b.get("lines", []):
                spans = line.get("spans", [])
                if not spans: continue

                valid_spans = [s for s in spans if "text" in s and "size" in s and s["text"].strip()]
                if not valid_spans: continue

                text = " ".join(span["text"].strip() for span in valid_spans)
                text = unicodedata.normalize("NFC", text)

                if len(text) < 5 or not any(char.isalnum() for char in text):
                    continue

                font_size = valid_spans[0].get("size", 0)
                is_bold = "bold" in valid_spans[0].get("font", "").lower()

                heading_candidates.append({
                    "text": text,
                    "size": font_size,
                    "bold": is_bold,
                    "page": page_num + 1
                })
                font_scores[font_size] += 1

    if not heading_candidates:
        return "Untitled Document", []

    sizes = np.array(list(font_scores.keys())).reshape(-1, 1)
    try:
        n_clusters = min(3, len(sizes))
        if n_clusters == 0: return "Untitled Document", []
            
        kmeans = KMeans(n_clusters=n_clusters, n_init="auto", random_state=0).fit(sizes)
    except Exception:
        return "Untitled Document", []

    sorted_centers = sorted([(c[0], i) for i, c in enumerate(kmeans.cluster_centers_)], reverse=True)
    defined_levels = ["H1", "H2", "H3"]
    level_map = {entry[1]: level for entry, level in zip(sorted_centers, defined_levels)}
    font_to_level = {size[0]: level_map[cluster] for size, cluster in zip(sizes, kmeans.labels_)}

    seen = set()
    outline = []
    
    for h in heading_candidates:
        if h["size"] not in font_to_level: continue
        clean_text = h["text"].strip()
        if clean_text.lower() in seen: continue
        seen.add(clean_text.lower())
        if not h["bold"] and h["size"] < 10: continue

        outline.append({
            "level": font_to_level[h["size"]],
            "text": clean_text,
            "page": h["page"]
        })

    title = doc.metadata.get("title", "")
    if not title and outline: title = outline[0]["text"]
    if not title: title = "Untitled Document"

    return title, outline

def clean_headers(headers):
    """
    Renames duplicate or empty headers to ensure Streamlit compatibility.
    """
    seen = {}
    new_headers = []
    for i, h in enumerate(headers):
        if h is None or str(h).strip() == "":
            base_name = f"Unnamed_{i}"
        else:
            base_name = str(h).strip()
        
        if base_name in seen:
            seen[base_name] += 1
            new_name = f"{base_name}_{seen[base_name]}"
        else:
            seen[base_name] = 0
            new_name = base_name
            
        new_headers.append(new_name)
    return new_headers

def extract_tables(pdf_path):
    """
    Extracts tables from the PDF using pdfplumber.
    """
    extracted_tables = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                tables = page.extract_tables()
                if tables:
                    for table_data in tables:
                        clean_data = [row for row in table_data if any(row)]
                        if clean_data:
                            if len(clean_data) > 1:
                                raw_headers = clean_data[0]
                                unique_headers = clean_headers(raw_headers)
                                df = pd.DataFrame(clean_data[1:], columns=unique_headers)
                            else:
                                df = pd.DataFrame(clean_data)

                            extracted_tables.append({
                                "page": i + 1,
                                "dataframe": df,
                                "rows": len(df),
                                "cols": len(df.columns)
                            })
    except Exception as e:
        print(f"Table extraction error: {e}")
    return extracted_tables

def translate_content(text, target_lang='es'):
    """
    Translates text to target language.
    """
    translator = GoogleTranslator(source='auto', target=target_lang)
    chunks = [text[i:i+4500] for i in range(0, len(text), 4500)]
    translated_chunks = []
    try:
        for chunk in chunks:
            translated_chunks.append(translator.translate(chunk))
        return "\n".join(translated_chunks)
    except Exception as e:
        return f"Translation Error: {str(e)}"

def process_pdf(doc, output_dir, file_path, password=None):
    """
    Extracts text (with OCR fallback), images, structure, metadata, AND tables.
    """
    if doc.is_encrypted:
        if not password: return None, None, None, "PASSWORD_REQUIRED"
        if not doc.authenticate(password): return None, None, None, "INVALID_PASSWORD"

    images_dir = os.path.join(output_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    text_chunks = []
    image_count = 0

    # 1. Structure & Meta
    doc_title, doc_outline = analyze_structure(doc)
    raw_metadata = doc.metadata

    # 2. Content (Text, OCR & Images)
    for page_num, page in enumerate(doc):
        # A. Smart Text Extraction (with OCR trigger)
        text = page.get_text()
        
        # If text is very sparse (< 10 chars), assume it's a scanned image and try OCR
        if len(text.strip()) < 10:
            try:
                pix = page.get_pixmap()
                # Convert PyMuPDF Pixmap to PIL Image
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                
                # Perform OCR
                ocr_text = pytesseract.image_to_string(img)
                if ocr_text.strip():
                    text = f"[OCR Extracted]\n{ocr_text}"
            except Exception as e:
                # If Tesseract is not installed or fails, keep original empty text
                # We don't print to avoid spamming logs, but you could log 'e'
                pass

        text_chunks.append(f"\n--- Page {page_num + 1} ---\n{text}\n")

        # B. Images
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            try:
                base_image = doc.extract_image(xref)
                with open(os.path.join(images_dir, f"page{page_num+1}_img{img_index}.{base_image['ext']}"), "wb") as f:
                    f.write(base_image["image"])
                image_count += 1
            except: continue

    full_text = "".join(text_chunks)
    text_path = os.path.join(output_dir, "extracted_text.txt")
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(full_text)
        
    # 3. Tables
    tables = extract_tables(file_path)

    structure_data = {
        "title": doc_title,
        "outline": doc_outline,
        "text_path": text_path,
        "pdf_meta": raw_metadata,
        "tables": tables 
    }

    return full_text, image_count, structure_data, "SUCCESS"