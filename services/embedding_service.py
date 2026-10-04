import logging
import numpy as np
from typing import List, Union

logger = logging.getLogger(__name__)

class EmbeddingService:
    _instance = None
    _model = None

    def __new__(cls, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        if cls._instance is None:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
            cls._instance.model_name = model_name
            cls._instance._load_model()
        return cls._instance

    def _load_model(self):
        """Loads the SentenceTransformer embedding model into memory once."""
        logger.info(f"Initializing SentenceTransformer model: {self.model_name}")
        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.model_name)
            logger.info("SentenceTransformer model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load SentenceTransformer model {self.model_name}: {e}")
            self._model = None

    @property
    def is_model_loaded(self) -> bool:
        return self._model is not None

    def encode(self, text: Union[str, List[str]]) -> np.ndarray:
        """
        Generates 384-dimensional dense vector embeddings for input text.
        Returns numpy array.
        """
        if not self.is_model_loaded:
            raise RuntimeError(
                "Embedding model is not loaded. Please check sentence-transformers installation."
            )

        if isinstance(text, str):
            if not text.strip():
                # Return zero vector of 384 dimensions for empty string
                return np.zeros(384, dtype=np.float32)
            embedding = self._model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
            return embedding
        elif isinstance(text, list):
            cleaned_texts = [t if t.strip() else " " for t in text]
            embeddings = self._model.encode(cleaned_texts, convert_to_numpy=True, normalize_embeddings=True)
            return embeddings
        else:
            raise ValueError("Input must be a string or list of strings.")
