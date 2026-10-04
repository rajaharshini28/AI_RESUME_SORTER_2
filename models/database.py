import sqlite3
import logging
from contextlib import contextmanager
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_db()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()

    def init_db(self):
        """Creates table schemas if they do not exist."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Jobs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    required_skills TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Candidates table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS candidates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT,
                    phone TEXT,
                    resume_filename TEXT NOT NULL,
                    resume_text TEXT NOT NULL,
                    education TEXT,
                    experience_years REAL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Candidate Skills table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS candidate_skills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    candidate_id INTEGER NOT NULL,
                    skill TEXT NOT NULL,
                    FOREIGN KEY (candidate_id) REFERENCES candidates (id) ON DELETE CASCADE
                )
            ''')

            # Rankings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS rankings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_id INTEGER NOT NULL,
                    candidate_id INTEGER NOT NULL,
                    semantic_score REAL NOT NULL,
                    skill_score REAL NOT NULL,
                    experience_score REAL NOT NULL,
                    education_score REAL NOT NULL,
                    final_score REAL NOT NULL,
                    matched_skills TEXT,
                    missing_skills TEXT,
                    reason TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (job_id) REFERENCES jobs (id) ON DELETE CASCADE,
                    FOREIGN KEY (candidate_id) REFERENCES candidates (id) ON DELETE CASCADE
                )
            ''')
            logger.info("Database schema initialized successfully.")

    # --- Job Operations ---
    def insert_job(self, title: str, description: str, required_skills: str = "") -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO jobs (title, description, required_skills) VALUES (?, ?, ?)",
                (title, description, required_skills)
            )
            return cursor.lastrowid

    def get_job(self, job_id: int) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_all_jobs(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM jobs ORDER BY created_at DESC")
            return [dict(r) for r in cursor.fetchall()]

    # --- Candidate Operations ---
    def insert_candidate(self, name: str, email: str, phone: str, resume_filename: str,
                         resume_text: str, education: str, experience_years: float, skills: List[str]) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO candidates (name, email, phone, resume_filename, resume_text, education, experience_years)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, email, phone, resume_filename, resume_text, education, experience_years))
            candidate_id = cursor.lastrowid

            for skill in skills:
                cursor.execute(
                    "INSERT INTO candidate_skills (candidate_id, skill) VALUES (?, ?)",
                    (candidate_id, skill)
                )
            return candidate_id

    def get_candidate(self, candidate_id: int) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM candidates WHERE id = ?", (candidate_id,))
            row = cursor.fetchone()
            if not row:
                return None
            candidate = dict(row)
            cursor.execute("SELECT skill FROM candidate_skills WHERE candidate_id = ?", (candidate_id,))
            candidate['skills'] = [r['skill'] for r in cursor.fetchall()]
            return candidate

    # --- Ranking Operations ---
    def save_ranking(self, job_id: int, candidate_id: int, semantic_score: float,
                     skill_score: float, experience_score: float, education_score: float,
                     final_score: float, matched_skills: str, missing_skills: str, reason: str) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO rankings 
                (job_id, candidate_id, semantic_score, skill_score, experience_score, education_score, final_score, matched_skills, missing_skills, reason)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (job_id, candidate_id, semantic_score, skill_score, experience_score, education_score, final_score, matched_skills, missing_skills, reason))
            return cursor.lastrowid

    def get_rankings_for_job(self, job_id: int) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT r.*, c.name, c.email, c.phone, c.resume_filename, c.education, c.experience_years
                FROM rankings r
                JOIN candidates c ON r.candidate_id = c.id
                WHERE r.job_id = ?
                ORDER BY r.final_score DESC
            ''', (job_id,))
            return [dict(r) for r in cursor.fetchall()]

    def get_candidate_ranking(self, job_id: int, candidate_id: int) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT r.*, c.name, c.email, c.phone, c.resume_filename, c.resume_text, c.education, c.experience_years, j.title as job_title, j.description as job_description
                FROM rankings r
                JOIN candidates c ON r.candidate_id = c.id
                JOIN jobs j ON r.job_id = j.id
                WHERE r.job_id = ? AND r.candidate_id = ?
            ''', (job_id, candidate_id))
            row = cursor.fetchone()
            if not row:
                return None
            result = dict(row)
            cursor.execute("SELECT skill FROM candidate_skills WHERE candidate_id = ?", (candidate_id,))
            result['skills'] = [r['skill'] for r in cursor.fetchall()]
            return result
