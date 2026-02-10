"""
Readability & Text Analytics Module
------------------------------------
Computes reading-level metrics (Flesch-Kincaid, Gunning Fog, etc.),
estimated reading time, and basic text statistics.
"""

import re
import math


def _count_syllables(word: str) -> int:
    """Estimate syllable count for an English word."""
    word = word.lower().strip()
    if not word:
        return 0
    # Remove trailing 'e' (silent e)
    if word.endswith("e") and len(word) > 2:
        word = word[:-1]
    # Count vowel groups
    count = len(re.findall(r"[aeiouy]+", word))
    return max(count, 1)


def _split_sentences(text: str) -> list:
    """Split text into sentences using punctuation boundaries."""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s for s in sentences if len(s.strip()) > 2]


def _split_words(text: str) -> list:
    """Extract words (alphabetic tokens) from text."""
    return re.findall(r"[a-zA-Z]+", text)


def compute_readability(text: str) -> dict:
    """
    Compute readability metrics for the given text.

    Returns a dict with:
        - word_count
        - sentence_count
        - avg_sentence_length
        - avg_syllables_per_word
        - flesch_reading_ease
        - flesch_kincaid_grade
        - gunning_fog_index
        - coleman_liau_index
        - reading_time_minutes
        - reading_level  (human-friendly label)
    """
    if not text or not text.strip():
        return _empty_result()

    sentences = _split_sentences(text)
    words = _split_words(text)
    sentence_count = len(sentences)
    word_count = len(words)

    if word_count == 0 or sentence_count == 0:
        return _empty_result()

    # --- Core counts ---
    syllable_counts = [_count_syllables(w) for w in words]
    total_syllables = sum(syllable_counts)
    complex_words = sum(1 for s in syllable_counts if s >= 3)

    avg_sentence_length = word_count / sentence_count
    avg_syllables_per_word = total_syllables / word_count

    # --- Character counts for Coleman-Liau ---
    total_chars = sum(len(w) for w in words)

    # --- Flesch Reading Ease ---
    # 206.835 - 1.015 * ASL - 84.6 * ASW
    flesch_re = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
    flesch_re = round(max(0, min(flesch_re, 100)), 1)

    # --- Flesch-Kincaid Grade Level ---
    # 0.39 * ASL + 11.8 * ASW - 15.59
    fk_grade = (0.39 * avg_sentence_length) + (11.8 * avg_syllables_per_word) - 15.59
    fk_grade = round(max(0, fk_grade), 1)

    # --- Gunning Fog Index ---
    # 0.4 * (ASL + 100 * (complex / words))
    fog = 0.4 * (avg_sentence_length + 100 * (complex_words / word_count))
    fog = round(max(0, fog), 1)

    # --- Coleman-Liau Index ---
    # 0.0588 * L - 0.296 * S - 15.8
    # L = avg letters per 100 words, S = avg sentences per 100 words
    L = (total_chars / word_count) * 100
    S = (sentence_count / word_count) * 100
    cli = 0.0588 * L - 0.296 * S - 15.8
    cli = round(max(0, cli), 1)

    # --- Reading Time (avg 200 wpm for non-fiction) ---
    reading_time = word_count / 200
    reading_time = round(reading_time, 1)

    # --- Human-friendly label ---
    reading_level = _get_reading_level(flesch_re)

    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "syllable_count": total_syllables,
        "complex_word_count": complex_words,
        "avg_sentence_length": round(avg_sentence_length, 1),
        "avg_syllables_per_word": round(avg_syllables_per_word, 2),
        "flesch_reading_ease": flesch_re,
        "flesch_kincaid_grade": fk_grade,
        "gunning_fog_index": fog,
        "coleman_liau_index": cli,
        "reading_time_minutes": reading_time,
        "reading_level": reading_level,
    }


def _get_reading_level(flesch_score: float) -> str:
    """Map Flesch Reading Ease score to a human-readable label."""
    if flesch_score >= 90:
        return "Very Easy (5th Grade)"
    elif flesch_score >= 80:
        return "Easy (6th Grade)"
    elif flesch_score >= 70:
        return "Fairly Easy (7th Grade)"
    elif flesch_score >= 60:
        return "Standard (8th-9th Grade)"
    elif flesch_score >= 50:
        return "Fairly Difficult (10th-12th Grade)"
    elif flesch_score >= 30:
        return "Difficult (College Level)"
    else:
        return "Very Difficult (Graduate Level)"


def _empty_result() -> dict:
    """Return zeroed-out metrics when text is insufficient."""
    return {
        "word_count": 0,
        "sentence_count": 0,
        "syllable_count": 0,
        "complex_word_count": 0,
        "avg_sentence_length": 0,
        "avg_syllables_per_word": 0,
        "flesch_reading_ease": 0,
        "flesch_kincaid_grade": 0,
        "gunning_fog_index": 0,
        "coleman_liau_index": 0,
        "reading_time_minutes": 0,
        "reading_level": "N/A",
    }
