FROM python:3.11-slim

WORKDIR /app

COPY 01-contradiction-detector/backend/requirements.txt .
RUN pip install -r requirements.txt

RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger'); nltk.download('punkt_tab')"

COPY 01-contradiction-detector/backend /app

CMD ["python", "app_gradio.py"]