import pytest
import tempfile
import os
from services.document_parser import extract_resume_text, ParsingError

def test_missing_file_raises_error():
    with pytest.raises(FileNotFoundError):
        extract_resume_text("non_existent_resume_file.pdf")

def test_unsupported_file_extension():
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
        f.write(b"Sample text")
        tmp_path = f.name
    
    try:
        with pytest.raises(ValueError) as exc:
            extract_resume_text(tmp_path)
        assert "Unsupported file format" in str(exc.value)
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
