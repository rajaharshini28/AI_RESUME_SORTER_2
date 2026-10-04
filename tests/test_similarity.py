import numpy as np
from services.similarity_service import calculate_cosine_similarity, scale_similarity_to_score

def test_cosine_similarity_identical_vectors():
    v1 = np.array([1.0, 2.0, 3.0], dtype=np.float32)
    v2 = np.array([1.0, 2.0, 3.0], dtype=np.float32)
    sim = calculate_cosine_similarity(v1, v2)
    assert abs(sim - 1.0) < 1e-5
    assert scale_similarity_to_score(sim) == 100.0

def test_cosine_similarity_orthogonal_vectors():
    v1 = np.array([1.0, 0.0], dtype=np.float32)
    v2 = np.array([0.0, 1.0], dtype=np.float32)
    sim = calculate_cosine_similarity(v1, v2)
    assert abs(sim - 0.0) < 1e-5
    assert scale_similarity_to_score(sim) == 0.0

def test_cosine_similarity_zero_vector():
    v1 = np.array([0.0, 0.0], dtype=np.float32)
    v2 = np.array([1.0, 2.0], dtype=np.float32)
    assert calculate_cosine_similarity(v1, v2) == 0.0
