from services.text_processor import normalize_whitespace, clean_text_for_embedding, clean_text_for_extraction

def test_normalize_whitespace():
    raw = "  Hello   World!\n\n\n\nThis   is   a   test.  "
    cleaned = normalize_whitespace(raw)
    assert cleaned == "Hello World!\n\nThis is a test."

def test_clean_text_for_embedding_preserves_context():
    raw = "Senior Software Engineer proficient in C++, C#, and .NET Framework."
    cleaned = clean_text_for_embedding(raw)
    assert "C++" in cleaned
    assert "C#" in cleaned
    assert ".NET" in cleaned
    assert "Software Engineer" in cleaned

def test_empty_string_handling():
    assert clean_text_for_embedding("") == ""
    assert clean_text_for_extraction(None) == ""
