import numpy as np
import logging

logger = logging.getLogger(__name__)

def calculate_cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Computes Cosine Similarity between two N-dimensional embedding vectors.
    Formula: Cosine Sim(u, v) = (u . v) / (||u|| * ||v||)
    Returns float value in [-1.0, 1.0].
    """
    if vec1 is None or vec2 is None:
        return 0.0

    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    dot_product = np.dot(vec1, vec2)
    similarity = float(dot_product / (norm1 * norm2))
    # Clip to valid mathematical bounds due to floating point precision
    return max(-1.0, min(1.0, similarity))

def scale_similarity_to_score(similarity: float) -> float:
    """
    Scales raw cosine similarity [-1.0, 1.0] to a 0.0 - 100.0 percentage score.
    For semantic text embeddings, negative similarities are near impossible;
    scores are mapped linearly from [0, 1] -> [0, 100].
    """
    clamped_sim = max(0.0, float(similarity))
    score = round(clamped_sim * 100.0, 1)
    return max(0.0, min(100.0, score))
