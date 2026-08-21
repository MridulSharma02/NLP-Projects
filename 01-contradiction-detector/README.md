---
title: Contradiction Detector
emoji: 🔍
colorFrom: blue
colorTo: red
sdk: gradio
sdk_version: 4.44.1
app_file: backend/app_gradio.py
pinned: false
---

# 🔍 Contradiction Detector

A Natural Language Processing system that determines whether two sentences are **Consistent**, **Contradictory**, or **Unrelated** — built with Gradio, NLTK, and a pretrained NLI CrossEncoder model, deployed on HuggingFace Spaces with ZeroGPU.

---

## 📌 Problem Statement

Given two sentences A and B, classify their relationship:

| Label | Meaning | Example |
|---|---|---|
| ❌ Contradiction | Sentences conflict | "The server is running." vs "The server is offline." |
| ✅ Consistent | Sentences agree | "A man is eating pizza." vs "A man is having food." |
| ↔️ Unrelated | Sentences share no connection | "The cat is sleeping." vs "Stock market crashed." |

---

## 🏗️ Project Structure

```
contradiction-detector/
├── backend/
│   ├── app_gradio.py      # Gradio UI — main entry point for HF Space
│   ├── model.py           # Two-stage NLI prediction pipeline
│   ├── preprocessor.py    # NLTK preprocessing pipeline
│   ├── schemas.py         # Pydantic request/response models
│   ├── logger.py          # Prediction logging to JSON and CSV
│   └── evaluator.py       # SNLI dataset evaluation script
├── frontend/
│   └── app.py             # Local Streamlit UI (development only)
├── README.md
└── requirements.txt
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

### 3. Two-Stage Classification Pipeline

#### Stage 1: Semantic Disconnection Check (NLTK)
Before passing to the model, a lightweight NLTK-based filter checks if the sentences are semantically disconnected:

> If **token overlap == 0.0** AND **WordNet similarity < 0.12** → classify as **Unrelated** immediately

This catches obviously unrelated sentence pairs efficiently without wasting model inference.

#### Stage 2: CrossEncoder NLI Model
If sentences pass Stage 1 (i.e. they share some semantic connection), they are passed to `cross-encoder/nli-MiniLM2-L6-H768` — a pretrained Natural Language Inference CrossEncoder from HuggingFace that classifies the pair as:
- **Contradiction** (mapped to "Contradiction")
- **Entailment** (mapped to "Consistent")
- **Neutral** (mapped to "Unrelated")

This two-stage approach combines the efficiency of rule-based NLP with the accuracy of deep learning.

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

## 🚀 Local Setup & Run

### Prerequisites
- Python 3.11+
- VS Code or any terminal

### Backend (FastAPI)

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

### Frontend (Streamlit — local only)

```bash
cd backend
.\venv\Scripts\activate
streamlit run ../frontend/app.py
```

UI opens at: `http://localhost:8501`

### Gradio (HuggingFace Space)

```bash
cd backend
.\venv\Scripts\activate
python app_gradio.py
```

---

## 🌐 Deployment

This app is deployed on **HuggingFace Spaces** using **ZeroGPU** (free tier).

- **Live App:** [MridulSharma02/contradiction-detector](https://huggingface.co/spaces/MridulSharma02/contradiction-detector)
- **SDK:** Gradio 4.44.1
- **Hardware:** ZeroGPU (Nvidia RTX Pro 6000 Blackwell, dynamic allocation)

### Deployment Stack
| Component | Detail |
|---|---|
| Platform | HuggingFace Spaces |
| SDK | Gradio 4.44.1 |
| GPU | ZeroGPU (free, dynamic) |
| Decorator | `@spaces.GPU` on inference function |
| Web Server | Uvicorn + Starlette (via Gradio) |

---

## 🔌 API Endpoints (Local FastAPI)

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
| Gradio UI | Gradio 4.44.1 |
| Backend Framework | FastAPI + Uvicorn |
| NLP Preprocessing | NLTK (tokenization, stopwords, lemmatization, WordNet) |
| Feature Extraction | Token overlap, antonym detection, WordNet path similarity |
| NLI Model | `cross-encoder/nli-MiniLM2-L6-H768` (HuggingFace) |
| Model Framework | sentence-transformers (CrossEncoder) |
| Two-Stage Pipeline | NLTK semantic filter → CrossEncoder inference |
| Dataset | SNLI (Stanford Natural Language Inference) |
| Local Frontend | Streamlit |
| Deployment | HuggingFace Spaces + ZeroGPU |
| GPU Decorator | `spaces` library (`@spaces.GPU`) |
| Dependency Pinning | starlette==0.37.2, fastapi==0.111.0 |
| Logging | JSON + CSV |
| Data Validation | Pydantic |

---

## 👤 Author

**Mridul Sharma**  
B.Tech AI/ML — IILM University (in collaboration with IBM)  
GitHub: [MridulSharma02](https://github.com/MridulSharma02)  
LinkedIn: [mridul-sharma-a5b9a9408](https://linkedin.com/in/mridul-sharma-a5b9a9408)