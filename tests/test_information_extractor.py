from services.information_extractor import (
    extract_email, extract_phone, extract_name, extract_skills,
    extract_education, extract_experience_years
)

def test_extract_email():
    text = "Contact me at candidate.test@domain.co.in or call today."
    assert extract_email(text) == "candidate.test@domain.co.in"
    assert extract_email("No email present") == "Not Provided"

def test_extract_phone():
    text = "Mobile: +1 (555) 987-6543, Office: 555-123-4567"
    assert extract_phone(text) == "+1 (555) 987-6543"
    assert extract_phone("No phone present") == "Not Provided"

def test_extract_skills_boundary_matching():
    # Verify 'C' does not match 'CSS' or 'JavaScript'
    text = "We use CSS, HTML, JavaScript, and C++."
    skills = extract_skills(text, available_skills=["C", "C++", "CSS", "JavaScript", "Python"])
    
    assert "CSS" in skills
    assert "C++" in skills
    assert "JavaScript" in skills
    assert "C" not in skills  # Crucial test: 'C' should NOT be extracted!
    assert "Python" not in skills

def test_extract_education():
    text = "Graduated with a Bachelor of Technology in Computer Science."
    assert extract_education(text) == "Bachelor's Degree"
    
    phd_text = "Holds a Ph.D. in Artificial Intelligence."
    assert extract_education(phd_text) == "Ph.D."

def test_extract_experience_years():
    text = "Senior Developer with 5.5 years of experience in backend systems."
    years = extract_experience_years(text)
    assert years == 5.5
