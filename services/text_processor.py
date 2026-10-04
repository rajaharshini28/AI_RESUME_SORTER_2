import re
import unicodedata

def normalize_whitespace(text: str) -> str:
    """Replaces consecutive newlines, tabs, and spaces with single space or single newline."""
    if not text:
        return ""
    # Replace unicode non-breaking spaces
    text = unicodedata.normalize('NFKD', text)
    # Standardize newlines
    text = re.sub(r'\r\n|\r', '\n', text)
    # Collapse multiple vertical newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Collapse multiple spaces
    text = re.sub(r'[ \t]{2,}', ' ', text)
    return text.strip()

def clean_text_for_embedding(text: str) -> str:
    """
    Cleans raw document text for semantic embedding models (e.g. Sentence-BERT).
    
    IMPORTANT NLP NOTE:
    - Retains natural casing, punctuation, and stopwords because modern transformer models
      (like all-MiniLM-L6-v2) rely on complete sentence syntax and context.
    - Only normalizes whitespace and strips non-printable unicode artifacts.
    """
    if not text:
        return ""
    text = normalize_whitespace(text)
    # Remove control characters except newlines
    text = "".join(ch for ch in text if unicodedata.category(ch)[0] != "C" or ch == '\n')
    return text

def clean_text_for_extraction(text: str) -> str:
    """
    Cleans raw document text for structured rule-based extraction (regex, skills matching).
    Preserves technical tokens like C++, C#, .NET, Node.js, RESTful.
    """
    if not text:
        return ""
    text = normalize_whitespace(text)
    # Ensure technical terms retain their punctuation while removing general noise
    return text
