"""
syllable_counter.py

Counts syllables in an English word or phrase using the CMU Pronouncing
Dictionary (CMUdict) via NLTK, falling back to a manually built
"exceptions" dictionary for words CMUdict doesn't know, and finally to a
simple vowel-group heuristic for anything still missing.

Requires:
    pip install nltk
    python -m nltk.downloader cmudict

Usage:
    python syllable_counter.py
    (then type a word or phrase when prompted, or Ctrl+C to quit)

Or import and use programmatically:
    from syllable_counter import count_syllables_text
    count_syllables_text("An old silent pond")
"""

import json
import re
import string
import sys

import nltk
from nltk.corpus import cmudict

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------


def _load_cmudict():
    """Load CMUdict, downloading it first if necessary."""
    try:
        return cmudict.dict()
    except LookupError:
        print("CMUdict not found locally; downloading it now...")
        nltk.download("cmudict")
        return cmudict.dict()


CMUDICT = _load_cmudict()

EXCEPTIONS_FILE = "exceptions.json"


def load_exceptions(filename=EXCEPTIONS_FILE):
    """Load the manually built dictionary of words -> syllable counts.

    Returns an empty dict if the file doesn't exist yet.
    """
    try:
        with open(filename) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


EXCEPTIONS = load_exceptions()


# ---------------------------------------------------------------------------
# Core syllable-counting logic
# ---------------------------------------------------------------------------


def _clean_word(word):
    """Lowercase a word and strip punctuation the way the corpus expects."""
    word = word.lower().strip(string.punctuation)
    if word.endswith("'s") or word.endswith("\u2019s"):
        word = word[:-2]
    return word


def _syllables_from_phonemes(pronunciations):
    """Given CMUdict's list of possible pronunciations for a word, return
    a syllable count.

    Each pronunciation is a list of phonemes; vowel phonemes end with a
    stress digit (0, 1, or 2). A word can have more than one accepted
    pronunciation (e.g. "aged"), so we use the FIRST pronunciation listed,
    which CMUdict treats as the most common.
    """
    first_pronunciation = pronunciations[0]
    return len([p for p in first_pronunciation if p[-1].isdigit()])


def _heuristic_syllables(word):
    """Rough fallback vowel-group heuristic for words found nowhere else.

    Not perfect (English spelling is what it is) but reasonable for
    words missing from both CMUdict and the exceptions dictionary.
    """
    word = word.lower()
    if not word:
        return 0
    groups = re.findall(r"[aeiouy]+", word)
    count = len(groups)
    if word.endswith("e") and not word.endswith("le") and count > 1:
        count -= 1
    return max(count, 1)


def count_syllables_word(word):
    """Count syllables in a single word using CMUdict, then the
    exceptions dictionary, then the heuristic fallback.
    """
    cleaned = _clean_word(word)
    if not cleaned:
        return 0

    if cleaned in CMUDICT:
        return _syllables_from_phonemes(CMUDICT[cleaned])

    if cleaned in EXCEPTIONS:
        return EXCEPTIONS[cleaned]

    return _heuristic_syllables(cleaned)


def count_syllables_text(text):
    """Count total syllables across every word in a phrase or line."""
    words = text.replace("-", " ").split()
    return sum(count_syllables_word(w) for w in words)


# ---------------------------------------------------------------------------
# Interactive entry point
# ---------------------------------------------------------------------------


def main():
    print("Syllable Counter (Ctrl+C to quit)")
    try:
        while True:
            text = input("\nEnter a word or phrase: ")
            total = count_syllables_text(text)
            print(f"Syllables: {total}")
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
