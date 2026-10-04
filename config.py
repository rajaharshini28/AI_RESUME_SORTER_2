import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-dev-secret-key-change-in-production')
    DATABASE_PATH = os.getenv('DATABASE_PATH', str(BASE_DIR / 'ai_resume_sorter.db'))
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', str(BASE_DIR / 'uploads'))
    ALLOWED_EXTENSIONS = {'pdf', 'docx'}
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16 MB
    
    # AI Embedding Model
    EMBEDDING_MODEL_NAME = os.getenv('EMBEDDING_MODEL_NAME', 'sentence-transformers/all-MiniLM-L6-v2')
    
    # Configurable Scoring Weights (Must sum to 1.0)
    SEMANTIC_WEIGHT = 0.60
    SKILL_WEIGHT = 0.25
    EXPERIENCE_WEIGHT = 0.10
    EDUCATION_WEIGHT = 0.05
