---
title: Contradiction Detector
emoji: 🔍
colorFrom: blue
colorTo: red
sdk: gradio
sdk_version: 4.44.0
app_file: app_gradio.py
pinned: false
---

# 🔍 Contradiction Detector

A Natural Language Processing system that determines whether two sentences are **Consistent**, **Contradictory**, or **Unrelated** — built with FastAPI, NLTK, and a pretrained NLI model.

---

## 📌 Problem Statement

Given two sentences A and B, classify their relationship:

| Label | Meaning | Example |
|---|---|---|
| 🔴 Contradiction | Sentences conflict | "The server is running." vs "The server is offline." |
| 🟢 Consistent | Sentences agree | "A man is eating pizza." vs "A man is having food." |
| 🟡 Unrelated | Sentences share no connection | "The cat is sleeping." vs "Stock market crashed." |

---

## 🏗️ Project Structure

```
contradiction-detector/
├── backend/
│   ├── main.py            # FastAPI app and route definitions
│   ├── model.py           # Pretrained NLI model + prediction logic
│   ├── preprocessor.py    # NLTK preprocessing pipeline
│   ├── schemas.py         # Pydantic request/response models
│   ├── logger.py          # Prediction logging to JSON and CSV
│   ├── evaluator.py       # SNLI dataset evaluation script
│   └── requirements.txt
│
└── frontend/
    └── app.py             # Streamlit UI
```

---

## ⚙️ How It Works

### 1. NLTK Preprocessing Pipeline
Every input sentence goes through a full preprocessing pipeline before analysis:
- **Lowercasing** — normalize text
- **Tokenization** — split into words using `word_tokenize`
- **Stopword Removal** — remove common words (the, is, a...)
- **Lemmatization** — reduce words to base form using `WordNetLemmatizer`

### 2. NLTK Feature Extraction
After preprocessing, three linguistic features are computed:
- **Token Overlap** — ratio of shared words between both sentences
- **Antonym Detection** — checks if any word in A is an antonym of any word in B using WordNet
- **WordNet Similarity** — semantic similarity score using `path_similarity`

### 3. Pretrained NLI Model
The cleaned sentences are passed to `cross-encoder/nli-deberta-v3-small` — a pretrained Natural Language Inference model from HuggingFace that classifies the pair as Contradiction / Entailment / Neutral.

### 4. NLTK Override Layer
To handle edge cases where the model mislabels completely unrelated sentences as Contradiction, an override rule is applied:

> If model predicts **Contradiction** AND token overlap is **0.0** AND WordNet similarity is **below 0.15** → override to **Unrelated**

This uses NLTK analysis as a correction layer on top of the model.

---

---

## 🎓 Model Training

The base `cross-encoder/nli-deberta-v3-small` model was fine-tuned on 10,000 samples from the SNLI dataset to improve domain-specific performance.

### Run Fine-tuning

```bash
cd backend
.\venv\Scripts\activate
python model_training.py
```

This will:
- Load 10,000 SNLI training samples
- Fine-tune the model for 1 epoch
- Evaluate on 100 test samples before and after
- Save trained weights to `fine-tuned-model/`

The API automatically loads the fine-tuned model if available.

---

---

## 📊 Model Performance

Evaluated on **100 samples** from the SNLI test set:

| Label | Precision | Recall | F1 |
|---|---|---|---|
| Contradiction | 0.91 | 0.97 | 0.94 |
| Consistent | 0.94 | 0.94 | 0.94 |
| Unrelated | 0.90 | 0.84 | 0.87 |
| **Overall Accuracy** | | | **92%** |

---

## 🚀 Setup & Run

### Prerequisites
- Python 3.11+
- VS Code or any terminal

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger'); nltk.download('punkt_tab')"
uvicorn main:app --reload
```

API runs at: `http://localhost:8000`  
Interactive docs at: `http://localhost:8000/docs`

### Frontend

```bash
# Open a new terminal, keep backend running
cd backend
.\venv\Scripts\activate
streamlit run ../frontend/app.py
```

UI opens at: `http://localhost:8501`

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API status |
| GET | `/health` | Health check + model status + total predictions |
| POST | `/predict` | Single sentence pair prediction |
| POST | `/predict/batch` | Multiple pairs at once |
| GET | `/stats` | Label distribution + average confidence |

### Example Request

```bash
POST /predict
{
  "sentence_a": "The server is running.",
  "sentence_b": "The server is offline."
}
```

### Example Response

```json
{
  "label": "Contradiction",
  "confidence": 0.9995,
  "nltk_analysis": {
    "cleaned_a": "server running",
    "cleaned_b": "server offline",
    "token_overlap": 0.5,
    "common_tokens": ["server"],
    "antonyms_found": [],
    "wordnet_similarity": 0.5278
  }
}
```

---

## 📁 Logs

Every prediction is automatically saved to:
- `backend/logs/predictions.json` — full prediction history
- `backend/logs/predictions.csv` — tabular format for analysis

---

## 🧪 Evaluate on SNLI Dataset

```bash
cd backend
.\venv\Scripts\activate
python evaluator.py
```

Downloads 100 samples from SNLI test set, runs predictions, and prints classification report + confusion matrix.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Backend Framework | FastAPI |
| NLP Preprocessing | NLTK (tokenization, lemmatization, WordNet) |
| NLI Model | `cross-encoder/nli-deberta-v3-small` |
| Dataset | SNLI (Stanford Natural Language Inference) |
| Frontend | Streamlit |
| Logging | JSON + CSV |

---

## 👤 Author

**Mridul Sharma**  
B.Tech AI/ML — IILM University (in collaboration with IBM)  
GitHub: [MridulSharma02](https://github.com/MridulSharma02)  
LinkedIn: [mridul-sharma-a5b9a9408](https://linkedin.com/in/mridul-sharma-a5b9a9408)