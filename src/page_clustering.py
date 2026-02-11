"""
Page Clustering & Visualization Module
----------------------------------------
Clusters PDF pages by topical similarity using TF-IDF + KMeans,
then reduces to 2D with PCA for scatter plot visualization.
"""

import re
import numpy as np
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


def _clean_text(s: str) -> str:
    """Basic text cleaning."""
    s = s or ""
    s = re.sub(r"\s+", " ", s).strip()
    return s


def cluster_pages(pdf_path: str, n_clusters: int = 4, min_chars: int = 60) -> dict:
    """
    Cluster PDF pages by content similarity and return 2D coordinates
    for visualization.

    Args:
        pdf_path:    Path to the PDF file.
        n_clusters:  Number of topic clusters to create.
        min_chars:   Minimum characters per page to include.

    Returns:
        dict with:
            - pages: list of {page_number, x, y, cluster, label, preview}
            - n_clusters: actual number of clusters used
            - cluster_labels: {cluster_id: top keywords}
            - total_pages: total pages in PDF
            - included_pages: pages with enough text
    """
    # Extract per-page text
    page_texts = []
    page_numbers = []

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        for idx, page in enumerate(pdf.pages, start=1):
            text = _clean_text(page.extract_text() or "")
            if len(text) >= min_chars:
                page_texts.append(text)
                page_numbers.append(idx)

    if len(page_texts) < 3:
        return {
            "pages": [],
            "n_clusters": 0,
            "cluster_labels": {},
            "total_pages": total_pages,
            "included_pages": len(page_texts),
            "warning": "Not enough text-rich pages (need at least 3) for clustering.",
        }

    # TF-IDF vectorization
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5000,
        ngram_range=(1, 2),
    )
    X = vectorizer.fit_transform(page_texts)
    feature_names = vectorizer.get_feature_names_out()

    # Adjust n_clusters to not exceed number of pages
    actual_k = min(n_clusters, len(page_texts))
    if actual_k < 2:
        actual_k = 2

    # KMeans clustering
    kmeans = KMeans(n_clusters=actual_k, n_init="auto", random_state=42)
    labels = kmeans.fit_predict(X)

    # PCA to 2D
    if X.shape[1] < 2:
        coords = np.zeros((X.shape[0], 2))
    else:
        n_components = min(2, X.shape[0], X.shape[1])
        pca = PCA(n_components=n_components, random_state=42)
        coords = pca.fit_transform(X.toarray())
        if coords.shape[1] == 1:
            coords = np.column_stack([coords, np.zeros(coords.shape[0])])

    # Generate cluster labels from top TF-IDF terms per cluster
    cluster_labels = {}
    for c in range(actual_k):
        mask = labels == c
        if mask.sum() == 0:
            cluster_labels[c] = "Empty"
            continue
        centroid = X[mask].mean(axis=0).A1
        top_indices = centroid.argsort()[-3:][::-1]
        top_words = [feature_names[i] for i in top_indices]
        cluster_labels[c] = ", ".join(top_words)

    # Build results
    pages = []
    for i, (pg_num, text) in enumerate(zip(page_numbers, page_texts)):
        preview = text[:100] + "..." if len(text) > 100 else text
        pages.append({
            "page_number": pg_num,
            "x": float(coords[i, 0]),
            "y": float(coords[i, 1]),
            "cluster": int(labels[i]),
            "label": cluster_labels[int(labels[i])],
            "preview": preview,
        })

    return {
        "pages": pages,
        "n_clusters": actual_k,
        "cluster_labels": cluster_labels,
        "total_pages": total_pages,
        "included_pages": len(page_texts),
        "warning": None,
    }
