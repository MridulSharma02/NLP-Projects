from pydantic import BaseModel
from typing import List

class PredictionRequest(BaseModel):
    sentence_a: str
    sentence_b: str

class BatchPredictionRequest(BaseModel):
    pairs: List[PredictionRequest]

class NLTKAnalysis(BaseModel):
    cleaned_a: str
    cleaned_b: str
    token_overlap: float
    common_tokens: List[str]
    antonyms_found: List[str]
    wordnet_similarity: float

class PredictionResponse(BaseModel):
    label: str
    confidence: float
    nltk_analysis: NLTKAnalysis

class BatchPredictionResponse(BaseModel):
    results: List[PredictionResponse]

class StatsResponse(BaseModel):
    total_predictions: int
    label_distribution: dict
    average_confidence: float

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    total_predictions: int
