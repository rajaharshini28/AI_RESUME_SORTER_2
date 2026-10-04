import pytest
import os
import sys
import tempfile

# Ensure project root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.database import Database

@pytest.fixture
def temp_db():
    """Provides a clean in-memory / temporary SQLite database for testing."""
    db_fd, db_path = tempfile.mkstemp()
    db = Database(db_path)
    yield db
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def sample_job_description():
    return {
        "title": "Senior Python Data Scientist",
        "description": "We are seeking a Data Scientist proficient in Python, SQL, Machine Learning, Pandas, NumPy, and PyTorch. Candidate must have 3+ years experience and a Bachelor's degree.",
        "required_skills": "Python, SQL, Machine Learning, Pandas, NumPy, PyTorch"
    }

@pytest.fixture
def sample_resume_text():
    return """
    Jane Doe
    Email: jane.doe@example.com
    Phone: (555) 123-4567

    Professional Summary:
    Experienced Data Scientist with 4 years of hands-on expertise building AI models using Python, SQL, Pandas, NumPy, and PyTorch. 

    Education:
    Bachelor of Science in Computer Science - State University (2020)

    Skills:
    Python, SQL, Pandas, NumPy, PyTorch, Git, Linux, Flask
    """
