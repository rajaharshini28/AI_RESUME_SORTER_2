import re
from typing import Dict, List, Any, Tuple

# Comprehensive taxonomy of technical skills
SKILL_TAXONOMY = [
    # Programming Languages
    "Python", "Java", "C++", "C#", "JavaScript", "TypeScript", "SQL", "R", "Go", "Rust", "PHP", "Ruby", "HTML", "CSS", "C",
    # Frameworks & Libraries
    "Flask", "FastAPI", "Django", "React", "Angular", "Vue", "Spring Boot", "Pandas", "NumPy", "Scikit-Learn", "PyTorch", "TensorFlow", "Keras",
    # AI & Data Science
    "Machine Learning", "Deep Learning", "NLP", "Data Science", "Data Analytics", "Computer Vision", "Generative AI", "LLMs", "ETL",
    # Databases
    "SQLite", "PostgreSQL", "MySQL", "MongoDB", "Redis", "Oracle", "SQL Server",
    # Cloud & DevOps
    "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Git", "GitHub", "GitLab", "CI/CD", "Linux",
    # Architecture & Tools
    "REST API", "GraphQL", "Microservices", "Agile", "Scrum"
]

def extract_email(text: str) -> str:
    """Extract email address from text using regex."""
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(pattern, text)
    return match.group(0) if match else "Not Provided"

def extract_phone(text: str) -> str:
    """Extract phone number from text using regex."""
    pattern = r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    match = re.search(pattern, text)
    return match.group(0) if match else "Not Provided"

def extract_name(text: str, filename: str = "") -> str:
    """
    Extract candidate name heuristics:
    1. Examines top lines of text (excluding headers like CV, Resume, email, phone).
    2. Fallback to filename if text heuristics do not return a valid name.
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    ignore_words = {'resume', 'curriculum', 'vitae', 'cv', 'profile', 'summary', 'contact', 'page'}

    for line in lines[:8]:
        # Skip emails, phone numbers, URLs, and header titles
        if re.search(r'@|\d{7,}|http|www\.', line, re.I):
            continue
        cleaned_line = re.sub(r'[^a-zA-Z\s]', '', line).strip()
        words = cleaned_line.split()

        if 2 <= len(words) <= 4:
            if not any(w.lower() in ignore_words for w in words):
                # Ensure words are capitalized or properly formatted
                return " ".join([w.capitalize() for w in words])

    # Fallback to filename
    if filename:
        clean_file = re.sub(r'\.(pdf|docx)$', '', filename, flags=re.I)
        clean_file = re.sub(r'[-_]', ' ', clean_file)
        clean_file = re.sub(r'\b(resume|cv|doc|docx|pdf)\b', '', clean_file, flags=re.I).strip()
        if clean_file:
            return clean_file.title()

    return "Unknown Candidate"

def extract_skills(text: str, available_skills: List[str] = SKILL_TAXONOMY) -> List[str]:
    """
    Extract skills using strict regex word boundaries to prevent false positive substring matches.
    Example: 'C' will NOT match inside 'CSS', 'C++', 'C#', or 'JavaScript'.
    """
    extracted = []
    text_lower = text.lower()

    for skill in available_skills:
        # Build strict boundary regex based on skill composition
        if skill == "C":
            pattern = r'(?:\bc\b(?!\+\+|\#))'
        elif skill == "C++":
            pattern = r'\bc\+\+(?!\w)'
        elif skill == "C#":
            pattern = r'\bc\#(?!\w)'
        elif skill == ".NET":
            pattern = r'(?:^|\b|\s)\.net(?!\w)'
        else:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'

        if re.search(pattern, text_lower):
            extracted.append(skill)

    return sorted(list(set(extracted)))

def extract_education(text: str) -> str:
    """Extract education background and degree levels."""
    degree_patterns = [
        (r'\b(Ph\.?D\.?|Doctor of Philosophy|Doctorate)\b', "Ph.D."),
        (r'\b(M\.?Tech|Master of Technology|M\.?S\.?|Master of Science|M\.?E\.?|Master of Engineering|MBA|Master of Business Administration|Master)\b', "Master's Degree"),
        (r'\b(B\.?Tech|Bachelor of Technology|B\.?E\.?|Bachelor of Engineering|B\.?S\.?|Bachelor of Science|B\.?A\.?|Bachelor of Arts|Bachelor)\b', "Bachelor's Degree"),
        (r'\b(Diploma|Associate Degree|Higher Secondary)\b', "Diploma/Associate")
    ]
    
    found_degrees = []
    for pattern, label in degree_patterns:
        if re.search(pattern, text, re.I):
            found_degrees.append(label)

    if found_degrees:
        return " / ".join(found_degrees)
    return "Degree Not Specified"

def extract_experience_years(text: str) -> float:
    """
    Extract approximate years of experience using pattern matching.
    Looks for phrases like '5 years of experience', '3+ years', or computes date ranges.
    """
    # Pattern 1: 'X+ years of experience' or 'X years'
    pattern = r'(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)\b(?:\s*of\s*experience)?'
    matches = re.findall(pattern, text, re.I)

    years = []
    for m in matches:
        try:
            val = float(m)
            if 0.5 <= val <= 35:  # Filter out realistic career durations
                years.append(val)
        except ValueError:
            continue

    if years:
        return max(years)

    # Pattern 2: Calculate date ranges like 2018 - 2023
    date_range_pattern = r'\b(20\d{2}|19\d{2})\s*[-–—to]+\s*(20\d{2}|present|current)\b'
    date_matches = re.findall(date_range_pattern, text, re.I)

    total_duration = 0.0
    for start_str, end_str in date_matches:
        try:
            start_yr = float(start_str)
            end_yr = 2026.0 if end_str.lower() in ('present', 'current') else float(end_str)
            duration = end_yr - start_yr
            if 0 < duration <= 35:
                total_duration += duration
        except ValueError:
            continue

    if total_duration > 0:
        return round(min(total_duration, 35.0), 1)

    return 0.0

def extract_candidate_info(text: str, filename: str = "") -> Dict[str, Any]:
    """Façade function to perform full structured extraction on resume text."""
    return {
        "name": extract_name(text, filename),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience_years": extract_experience_years(text)
    }
