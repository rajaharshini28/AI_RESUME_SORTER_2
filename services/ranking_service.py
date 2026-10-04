from typing import List, Dict, Any, Tuple
from config import Config

def calculate_skill_score(candidate_skills: List[str], required_skills: List[str]) -> Tuple[float, List[str], List[str]]:
    """
    Computes explicit skill match score between candidate skills and required job skills.
    Returns (score_0_to_100, matched_skills, missing_skills).
    """
    if not required_skills:
        return 100.0, candidate_skills, []

    cand_set = {s.lower() for s in candidate_skills}
    req_set = {s.lower() for s in required_skills}

    matched_lower = cand_set.intersection(req_set)
    missing_lower = req_set.difference(cand_set)

    matched = [s for s in required_skills if s.lower() in matched_lower]
    missing = [s for s in required_skills if s.lower() in missing_lower]

    match_ratio = len(matched) / len(required_skills)
    skill_score = round(match_ratio * 100.0, 1)

    return skill_score, matched, missing

def calculate_experience_score(candidate_years: float, target_years: float = 2.0) -> float:
    """
    Computes experience score based on years of experience relative to job requirement.
    """
    if target_years <= 0:
        return 100.0
    if candidate_years >= target_years:
        return 100.0
    
    ratio = candidate_years / target_years
    return round(ratio * 100.0, 1)

def calculate_education_score(candidate_edu: str) -> float:
    """
    Computes education level score based on recognized degree qualifications.
    """
    cand_edu_lower = candidate_edu.lower()
    if "ph.d." in cand_edu_lower or "doctorate" in cand_edu_lower:
        return 100.0
    elif "master" in cand_edu_lower:
        return 90.0
    elif "bachelor" in cand_edu_lower:
        return 80.0
    elif "diploma" in cand_edu_lower or "associate" in cand_edu_lower:
        return 65.0
    else:
        return 50.0

def compute_explainable_score(
    semantic_score: float,
    candidate_skills: List[str],
    required_skills: List[str],
    candidate_years: float,
    candidate_edu: str,
    weights: Dict[str, float] = None
) -> Dict[str, Any]:
    """
    Computes explainable composite score and ranking details.
    """
    if weights is None:
        weights = {
            "semantic": Config.SEMANTIC_WEIGHT,
            "skill": Config.SKILL_WEIGHT,
            "experience": Config.EXPERIENCE_WEIGHT,
            "education": Config.EDUCATION_WEIGHT
        }

    skill_score, matched_skills, missing_skills = calculate_skill_score(candidate_skills, required_skills)
    exp_score = calculate_experience_score(candidate_years, target_years=2.0)
    edu_score = calculate_education_score(candidate_edu)

    final_score = round(
        (weights["semantic"] * semantic_score) +
        (weights["skill"] * skill_score) +
        (weights["experience"] * exp_score) +
        (weights["education"] * edu_score),
        1
    )

    # Generate natural language explanation reason
    reason_parts = []
    if semantic_score >= 75.0:
        reason_parts.append("High semantic alignment with job description duties.")
    elif semantic_score >= 50.0:
        reason_parts.append("Moderate semantic match with job role context.")
    else:
        reason_parts.append("Lower semantic alignment with job context.")

    if matched_skills:
        reason_parts.append(f"Matched {len(matched_skills)} required technical skills ({', '.join(matched_skills[:4])}).")
    if missing_skills:
        reason_parts.append(f"Missing {len(missing_skills)} key skills ({', '.join(missing_skills[:3])}).")

    reason = " ".join(reason_parts)

    return {
        "semantic_score": semantic_score,
        "skill_score": skill_score,
        "experience_score": exp_score,
        "education_score": edu_score,
        "final_score": final_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "reason": reason
    }
