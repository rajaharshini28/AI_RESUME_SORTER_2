import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path

from config import Config
from models.database import Database
from services.document_parser import extract_resume_text, ParsingError
from services.text_processor import clean_text_for_embedding, clean_text_for_extraction
from services.information_extractor import extract_candidate_info, extract_skills
from services.embedding_service import EmbeddingService
from services.similarity_service import calculate_cosine_similarity, scale_similarity_to_score
from services.ranking_service import compute_explainable_score

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask App
app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Database
db = Database(app.config['DATABASE_PATH'])

# Lazy-load embedding model singleton
embedding_service = EmbeddingService(app.config['EMBEDDING_MODEL_NAME'])

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """Dashboard homepage listing all posted job descriptions."""
    jobs = db.get_all_jobs()
    return render_template('index.html', jobs=jobs)

@app.route('/job/create', methods=['GET', 'POST'])
def create_job():
    """Create a new job description."""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        custom_skills = request.form.get('required_skills', '').strip()

        if not title or not description:
            flash('Job title and job description are required.', 'error')
            return redirect(url_for('create_job'))

        # If custom required skills not provided, extract from job description text
        if custom_skills:
            required_skills_list = [s.strip() for s in custom_skills.split(',') if s.strip()]
        else:
            required_skills_list = extract_skills(description)

        required_skills_str = ", ".join(required_skills_list)
        job_id = db.insert_job(title, description, required_skills_str)
        flash(f'Job description "{title}" created successfully!', 'success')
        return redirect(url_for('upload_resumes', job_id=job_id))

    return render_template('job_create.html')

@app.route('/job/<int:job_id>/upload', methods=['GET', 'POST'])
def upload_resumes(job_id: int):
    """Upload multiple PDF/DOCX resumes for candidate evaluation."""
    job = db.get_job(job_id)
    if not job:
        flash('Target job description not found.', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        if 'resumes' not in request.files:
            flash('No resume files selected.', 'error')
            return redirect(url_for('upload_resumes', job_id=job_id))

        uploaded_files = request.files.getlist('resumes')
        if not uploaded_files or all(f.filename == '' for f in uploaded_files):
            flash('Please select at least one PDF or DOCX file.', 'error')
            return redirect(url_for('upload_resumes', job_id=job_id))

        # Encode Job Description into 384d vector embedding
        job_clean_text = clean_text_for_embedding(f"{job['title']} \n {job['description']}")
        job_embedding = embedding_service.encode(job_clean_text)

        required_skills = [s.strip() for s in job['required_skills'].split(',') if s.strip()] if job['required_skills'] else []

        success_count = 0
        error_messages = []

        for file in uploaded_files:
            if not file or file.filename == '':
                continue

            if not allowed_file(file.filename):
                error_messages.append(f"Skipped '{file.filename}': Unsupported file format. Only PDF and DOCX allowed.")
                continue

            orig_filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], orig_filename)

            # Prevent overwriting identical file names by prepending unique counter if needed
            counter = 1
            file_base, file_ext = os.path.splitext(orig_filename)
            while os.path.exists(save_path):
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_base}_{counter}{file_ext}")
                counter += 1

            file.save(save_path)

            try:
                # 1. Document Text Extraction
                raw_text = extract_resume_text(save_path)
                clean_text = clean_text_for_embedding(raw_text)

                # 2. Structured Information Extraction
                candidate_info = extract_candidate_info(raw_text, filename=orig_filename)

                # 3. Vector Embedding Generation
                resume_embedding = embedding_service.encode(clean_text)

                # 4. Cosine Similarity Calculation
                raw_sim = calculate_cosine_similarity(resume_embedding, job_embedding)
                semantic_score = scale_similarity_to_score(raw_sim)

                # 5. Explainable Weighted Score Computation
                evaluation = compute_explainable_score(
                    semantic_score=semantic_score,
                    candidate_skills=candidate_info['skills'],
                    required_skills=required_skills,
                    candidate_years=candidate_info['experience_years'],
                    candidate_edu=candidate_info['education']
                )

                # 6. Save to SQLite Database
                candidate_id = db.insert_candidate(
                    name=candidate_info['name'],
                    email=candidate_info['email'],
                    phone=candidate_info['phone'],
                    resume_filename=os.path.basename(save_path),
                    resume_text=raw_text,
                    education=candidate_info['education'],
                    experience_years=candidate_info['experience_years'],
                    skills=candidate_info['skills']
                )

                db.save_ranking(
                    job_id=job_id,
                    candidate_id=candidate_id,
                    semantic_score=evaluation['semantic_score'],
                    skill_score=evaluation['skill_score'],
                    experience_score=evaluation['experience_score'],
                    education_score=evaluation['education_score'],
                    final_score=evaluation['final_score'],
                    matched_skills=", ".join(evaluation['matched_skills']),
                    missing_skills=", ".join(evaluation['missing_skills']),
                    reason=evaluation['reason']
                )

                success_count += 1

            except ParsingError as pe:
                error_messages.append(f"Error processing '{orig_filename}': {str(pe)}")
            except Exception as e:
                logger.error(f"Unexpected failure processing {orig_filename}: {e}", exc_info=True)
                error_messages.append(f"Failed to process '{orig_filename}': {str(e)}")

        if success_count > 0:
            flash(f"Successfully processed and ranked {success_count} resume(s)!", 'success')
        for err in error_messages:
            flash(err, 'error')

        return redirect(url_for('rankings', job_id=job_id))

    return render_template('upload.html', job=job)

@app.route('/job/<int:job_id>/rankings')
def rankings(job_id: int):
    """View candidate rankings dashboard for a specific job description."""
    job = db.get_job(job_id)
    if not job:
        flash('Job not found.', 'error')
        return redirect(url_for('index'))

    ranking_list = db.get_rankings_for_job(job_id)
    return render_template('results.html', job=job, rankings=ranking_list)

@app.route('/job/<int:job_id>/candidate/<int:candidate_id>')
def candidate_detail(job_id: int, candidate_id: int):
    """Detailed breakdown page for an individual candidate evaluation."""
    candidate_ranking = db.get_candidate_ranking(job_id, candidate_id)
    if not candidate_ranking:
        flash('Candidate evaluation record not found.', 'error')
        return redirect(url_for('rankings', job_id=job_id))

    job = db.get_job(job_id)
    return render_template('candidate.html', candidate=candidate_ranking, job=job)

if __name__ == '__main__':
    logger.info("Starting AI Resume Sorter Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
