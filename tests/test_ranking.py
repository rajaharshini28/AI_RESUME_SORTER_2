from services.ranking_service import (
    calculate_skill_score, calculate_experience_score,
    calculate_education_score, compute_explainable_score
)

def test_calculate_skill_score():
    cand_skills = ["Python", "SQL", "Pandas", "Docker"]
    req_skills = ["Python", "SQL", "Pandas", "Machine Learning"]

    score, matched, missing = calculate_skill_score(cand_skills, req_skills)
    assert score == 75.0
    assert "Python" in matched
    assert "SQL" in matched
    assert "Pandas" in matched
    assert "Machine Learning" in missing

def test_compute_explainable_score():
    eval_result = compute_explainable_score(
        semantic_score=80.0,
        candidate_skills=["Python", "SQL", "Flask"],
        required_skills=["Python", "SQL", "Flask", "Docker"],
        candidate_years=3.0,
        candidate_edu="Bachelor's Degree"
    )

    # Weights: 0.60 * 80 + 0.25 * 75 + 0.10 * 100 + 0.05 * 80
    # 48.0 + 18.75 + 10.0 + 4.0 = 80.75 -> 80.8
    assert eval_result["final_score"] == 80.8
    assert "High semantic alignment" in eval_result["reason"]
