FROM python:3.11-slim

WORKDIR /app

COPY 01-contradiction-detector/backend/requirements.txt .
RUN pip install -r requirements.txt

RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger'); nltk.download('punkt_tab')"

COPY 01-contradiction-detector/backend /app/backend
COPY 01-contradiction-detector/frontend /app/frontend

# Start both FastAPI and Streamlit
CMD uvicorn backend.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/app.py --server.port 7860 --server.address 0.0.0.0