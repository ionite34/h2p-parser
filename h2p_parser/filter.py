from unicodedata import normalize
import re


# Filters text before parsing
# @param text: text to be filtered
# @return: filtered text
def filter_text(text: str) -> str:
    """
    Filters text before parsing
    :param text: Input raw text
    :return: Text after stripped accents, lower-cased, and invalid punctuation removed
    """
    # Strip accents
    text = normalize('NFD', text)
    # To lowercase
    text = text.lower()
    # Remove all invalid punctuation
    text = re.sub(r"[^ a-z'.,?!\-]", "", text)
    # Return
    return text
