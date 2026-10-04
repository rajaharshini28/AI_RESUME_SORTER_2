# ⚡ AI Resume Sorter & Job Matcher

> **An AI-Assisted Resume-to-Job Matching and Candidate Ranking System built with Flask, Sentence Transformers (`all-MiniLM-L6-v2`), PyMuPDF, python-docx, and SQLite.**

---

## 📌 Resume Statement Alignment
This project directly implements and verifies the following statement:

> *"Built a Flask-based application to parse PDF/DOCX resumes, extract structured candidate information, rank resumes using AI similarity scoring, and manage data using SQLite. Applied document processing and data extraction techniques aligned with analytics workflows."*

---

## 🚀 Overview & Key Features

Modern recruitment requires sifting through hundreds of candidate resumes against specific job descriptions. Traditional Keyword Applicant Tracking Systems (ATS) suffer from **rigid keyword matching**, missing highly qualified candidates who use synonymous phrasing (e.g., matching "Machine Learning" to "Predictive Modeling" or "Data Science").

**AI Resume Sorter** combines **Local Semantic AI Embeddings** with **Explicit Skill & Rules-Based Scoring** to deliver an **objective, explainable candidate ranking dashboard**.

### Core Capabilities:
- 📄 **Multi-Format Document Parsing**: Robust text extraction from `.pdf` (PyMuPDF / PyPDF) and `.docx` (python-docx) files. Detects image-only/scanned PDFs.
- 🧹 **Context-Aware Preprocessing**: Preserves sentence structures for neural embeddings while retaining technical syntax (`C++`, `C#`, `.NET`, `Node.js`).
- 🔍 **Structured Candidate Extraction**: Deterministic extraction of Candidate Name, Email, Phone Number, Education level, and Years of Experience.
- 🧠 **Local Semantic AI Scoring**: Uses `sentence-transformers/all-MiniLM-L6-v2` to map resumes and job descriptions into 384-dimensional dense vector space and computes **Cosine Similarity**.
- 🛠️ **Regex Word-Boundary Skill Matching**: Explicit skill extraction against a 50+ tech skill dictionary with strict word boundaries `\b` (prevents matching `C` inside `CSS` or `JavaScript`).
- 📊 **Explainable Weighted Scoring**: Transparent composite scoring engine ($60\%$ Semantic Similarity, $25\%$ Skill Match, $10\%$ Experience, $5\%$ Education) with natural language explanations.
- ⚖️ **Fairness & Demographic Neutrality**: Explicitly excludes gender, age, race, photos, and non-job demographics from ranking logic.
- 💾 **SQLite Persistence**: Structured database storage for job descriptions, candidates, extracted skills, and ranking evaluations.

---

## 🏗️ System Architecture

```
User (Recruiter)
       │
       ▼
Flask Web Dashboard (HTML5 / Modern Glassmorphic CSS3 / JavaScript)
       │
       ├──> Job Description Input & Skill Extraction
       └──> Bulk Resume Upload (PDF & DOCX)
       │
       ▼
Document Processing Layer
       ├──> PyMuPDF / PyPDF (PDF Parsing)
       └──> python-docx (DOCX Parsing)
       │
       ▼
Text Cleaning & Preprocessing Module
       │
       ▼
Structured Information Extractor
       ├──> Name, Email, Phone (Regex)
       ├──> Technical Skills (Word Boundary Taxonomy)
       └──> Education & Experience Heuristics
       │
       ▼
Vector Embedding Engine (SentenceTransformer: all-MiniLM-L6-v2 -> 384d Vectors)
       ├──> Job Description Vector
       └──> Candidate Resume Vector
       │
       ▼
Cosine Similarity Engine: Cosine(u, v) = (u . v) / (||u|| ||v||)
       │
       ▼
Explainable Weighted Scoring Engine:
Final Score = 0.60(Semantic) + 0.25(Skill) + 0.10(Exp) + 0.05(Edu)
       │
       ▼
SQLite Database (jobs, candidates, candidate_skills, rankings)
       │
       ▼
Ranked Candidate Dashboard & Detailed Analysis View
```

---

## 🛠️ Technology Stack

| Layer | Technology | Rationale |
| :--- | :--- | :--- |
| **Backend Web Framework** | Python 3.13, Flask 3.0 | Lightweight, flexible, easy to maintain and explain in technical interviews. |
| **AI / Semantic Model** | `sentence-transformers` (`all-MiniLM-L6-v2`) | Local execution (no paid external API keys required), 384-dimensional dense embeddings, optimized for speed and semantic sentence alignment. |
| **Document Parsing** | PyMuPDF (`fitz`), PyPDF, `python-docx` | Fast, accurate text extraction from text-based PDFs and Word documents. |
| **Database** | SQLite 3 | Serverless, zero-config file database built into Python; ideal for local development and technical interview defense. |
| **Frontend UI** | HTML5, CSS3, JavaScript | Responsive dashboard featuring Google Fonts (Inter), glassmorphism styling, drag-and-drop file upload, and score breakdown UI. |
| **Testing** | `pytest` | Suite of automated unit tests covering document parsing, regex extraction, skill boundaries, cosine similarity, and score ordering. |

---

## 📐 Explainable Scoring Formula

The candidate match score is calculated transparently:

$$\text{Final Score} = (0.60 \times \text{Semantic Score}) + (0.25 \times \text{Skill Match Score}) + (0.10 \times \text{Experience Score}) + (0.05 \times \text{Education Score})$$

### Score Components:
1. **Semantic Score ($60\%$)**: Cosine similarity between 384-dimensional dense vectors of the job description and candidate resume, rescaled to $[0, 100]$.
2. **Skill Score ($25\%$)**: Percentage of required technical skills explicitly matched on the resume.
3. **Experience Score ($10\%$)**: Extracted career duration evaluated against target job experience requirements.
4. **Education Score ($5\%$)**: Recognized degree qualification level (Ph.D., Master's, Bachelor's, Diploma).

---

## 📦 Installation & Quickstart Guide

### 1. Clone & Navigate to Workspace
```bash
cd ai_resume_sorter
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Application
```bash
python app.py
```
Open your browser and navigate to `http://localhost:5000`.

---

## 🧪 Running Automated Tests

Run the full `pytest` test suite:
```bash
pytest -v
```

---

## 🔒 Security & Fairness Considerations
- **Demographic Neutrality**: Personal demographic indicators (gender, ethnicity, age, marital status, profile images) are excluded from scoring.
- **Secure File Handling**: File uploads validate extension types (`.pdf`, `.docx`), limit file sizes to 16MB, and use `secure_filename()` to prevent directory traversal attacks.
- **Data Privacy**: All AI embeddings run 100% locally on your machine. No resume data is transmitted to external third-party cloud servers.
