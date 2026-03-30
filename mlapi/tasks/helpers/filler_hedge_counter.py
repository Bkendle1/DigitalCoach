from __future__ import annotations

import re
from typing import Dict, List, Tuple, Union

from tasks.helpers.constants import FILLER_WORDS, HEDGE_PHRASES
from tasks.helpers.text_preprocessing import _preprocess

Transcript = Union[str, List[str]]

def _flatten(transcript: Transcript | None) -> str:
    if transcript is None:
        return ""
    if isinstance(transcript, list):
        return " ".join([t for t in transcript if isinstance(t, str)])
    if isinstance(transcript, str):
        return transcript
    return ""

def _count_phrases(preprocessed_text: str, phrases: List[str]) -> Tuple[int, Dict[str, int]]:
    working = f" {preprocessed_text.strip()} "
    phrases_sorted = sorted(set(phrases), key=lambda p: len(p.split()), reverse=True)

    total = 0
    by_phrase: Dict[str, int] = {}

    for phrase in phrases_sorted:
        needle = f" {phrase} "
        pattern = re.escape(needle)

        matches = re.findall(pattern, working)
        count = len(matches)

        by_phrase[phrase] = count
        total += count

        if count:
            working = re.sub(pattern, " ", working)
            working = re.sub(r"\s+", " ", working)

    return total, by_phrase

def count_filler_and_hedge(transcript: Transcript | None) -> dict:
    text = _flatten(transcript)
    cleaned = _preprocess(text)  # IMPORTANT: don’t use clean_text() (stopwords would break phrases)

    filler_total, filler_by = _count_phrases(cleaned, sorted(FILLER_WORDS))
    hedge_total, hedge_by = _count_phrases(cleaned, sorted(HEDGE_PHRASES))

    return {
        "filler": {"total": filler_total, "by_phrase": filler_by},
        "hedge": {"total": hedge_total, "by_phrase": hedge_by},
        "total": filler_total + hedge_total,
    }