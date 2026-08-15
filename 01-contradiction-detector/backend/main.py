from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import (
    PredictionRequest, PredictionResponse,
    BatchPredictionRequest, BatchPredictionResponse,
    NLTKAnalysis, StatsResponse, HealthResponse
)
from model import predict, predict_batch
from logger import log_prediction, get_stats

app = FastAPI(
    title="Contradiction Detector API",
    description="Detects whether two sentences are Consistent, Contradictory, or Unrelated.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def root():
    return {"message": "Contradiction Detector API is running. Visit /docs for API documentation."}


@app.get("/health", response_model=HealthResponse, tags=["General"])
def health_check():
    stats = get_stats()
    return HealthResponse(status="ok", model_loaded=True, total_predictions=stats["total_predictions"])


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict_contradiction(request: PredictionRequest):
    if not request.sentence_a.strip() or not request.sentence_b.strip():
        raise HTTPException(status_code=400, detail="Both sentences must be non-empty.")
    result = predict(request.sentence_a, request.sentence_b)
    log_prediction(request.sentence_a, request.sentence_b, result)
    return PredictionResponse(
        label=result["label"],
        confidence=result["confidence"],
        nltk_analysis=NLTKAnalysis(**result["nltk_analysis"])
    )


@app.post("/predict/batch", response_model=BatchPredictionResponse, tags=["Prediction"])
def predict_batch_endpoint(request: BatchPredictionRequest):
    if not request.pairs:
        raise HTTPException(status_code=400, detail="Pairs list must not be empty.")
    pairs = [{"sentence_a": p.sentence_a, "sentence_b": p.sentence_b} for p in request.pairs]
    results = predict_batch(pairs)
    for pair, result in zip(request.pairs, results):
        log_prediction(pair.sentence_a, pair.sentence_b, result)
    return BatchPredictionResponse(results=[
        PredictionResponse(
            label=r["label"],
            confidence=r["confidence"],
            nltk_analysis=NLTKAnalysis(**r["nltk_analysis"])
        ) for r in results
    ])


@app.get("/stats", response_model=StatsResponse, tags=["Analytics"])
def get_statistics():
    return StatsResponse(**get_stats())
