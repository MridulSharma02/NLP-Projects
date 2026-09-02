# 🚨 Emergency Message Corpus & Syntactic Pattern Detection

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![spaCy](https://img.shields.io/badge/spaCy-en_core_web_sm-09A3D5?style=flat)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?style=flat&logo=pandas)
![NLP](https://img.shields.io/badge/NLP-Corpus%20Analysis-orange?style=flat)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=flat)

**NLP Project 3 · B.Tech CSE (AI & ML) · IILM University × IBM**

[Live Dashboard →](https://mridulsharma02.github.io/NLP-Projects/03-Emergency-Corpus/ui/)

</div>

---

## 📌 Problem Statement

> Construct a corpus of disaster/emergency messages and identify syntactic patterns that indicate **locations** and **required actions**.

Emergency messages are chaotic — informal spelling, missing punctuation, mixed languages, and extreme urgency. This project builds a pipeline that collects, cleans, annotates, and analyzes 76,000+ real crisis tweets to extract two critical signals: **where** the emergency is and **what** is needed.

---

## 📊 Results at a Glance

| Metric | Value |
|--------|-------|
| Total messages collected | 76,508 |
| Annotated sample | 5,025 |
| Messages with location pattern | 54.5% |
| Messages with action word | 26.4% |
| Informal messages | 71.4% |
| Avg words per message | 26.38 |

---

## 🔍 Key Findings

### Location Patterns
| Pattern | Example | Frequency |
|---------|---------|-----------|
| `PREP + PROPN` | *near Durbar Square*, *in Wayanad* | 938 |
| `PROPN + LOC_NOUN` | *Patna district*, *Kerala coast* | 120 |
| `LOC_NOUN` | *highway*, *station*, *river bank* | 155 |

### Action Patterns
| Pattern | Example | Frequency |
|---------|---------|-----------|
| `ACTION_VERB` | *send*, *rescue*, *evacuate*, *help* | 501 |
| `URGENCY_ADVERB` | *immediately*, *asap*, *urgently* | 117 |
| `DISTRESS_SIGNAL` | *SOS*, *URGENT*, *MAYDAY* | 67 |
| `VICTIM_STATE` | *trapped*, *stranded*, *injured* | 61 |
| `PLEA_PATTERN` | *please help*, *please send* | 25 |
| `NEED + RESOURCE` | *need food*, *need boats* | 19 |

### Syntactic Insight
High-urgency messages follow a **PROPN → NOUN → VERB** structure — clipped, imperative language with location names up front and fewer determiners. Low-urgency messages use more **DET → NOUN** constructions typical of news-style reporting.

---

## 🗂️ Dataset

| Source | Type | Messages |
|--------|------|----------|
| [HumAID](https://huggingface.co/datasets/riddle_sense/humaid) | Real crisis tweets (labeled) | ~76,460 |
| Manual (Indian context) | Curated emergency messages | 50 |

Covers: **earthquake, flood, cyclone, wildfire, tsunami, landslide, medical, structural** disasters.

---

## ⚙️ Pipeline

```
collect_data.py   →  76,508 raw messages from HumAID + manual
clean_data.py     →  URL/mention removal, whitespace normalization
annotate.py       →  spaCy NER, POS tags, urgency scoring, location/action extraction
spell_check.py    →  informal pattern detection (abbreviations, ALL CAPS, number-words)
pattern_detect.py →  syntactic pattern labeling (PREP+PROPN, ACTION_VERB, etc.)
analyze.py        →  corpus-level statistics and comparisons
report.py         →  markdown summary report
save_outputs.py   →  chart-ready CSVs + stat summaries
```

---

## 📁 Project Structure

```
03-Emergency-Corpus/
├── data/
│   ├── raw/              ← downloaded datasets
│   ├── cleaned/          ← after URL/mention cleaning
│   ├── annotated/        ← spaCy annotated corpus (5,025 messages)
│   └── results/          ← analysis.json, pattern_detect.csv, report.md
├── src/
│   ├── collect_data.py
│   ├── clean_data.py
│   ├── annotate.py
│   ├── spell_check.py
│   ├── pattern_detect.py
│   ├── analyze.py
│   ├── report.py
│   └── save_outputs.py
├── output/
│   ├── figures/          ← chart-ready CSVs
│   └── stats/            ← text summaries
├── ui/
│   └── index.html        ← interactive dashboard (Chart.js)
└── README.md
```

---

## 🛠️ Tech Stack

- **Python 3.11** — pipeline scripts
- **spaCy** `en_core_web_sm` — NER, POS tagging, dependency parsing
- **pandas** — data wrangling
- **Chart.js** — dashboard visualizations
- **HumAID** — primary dataset

---

## 🚀 Run It Yourself

```bash
# Install dependencies
pip install pandas spacy requests
python -m spacy download en_core_web_sm

# Run full pipeline
python src/collect_data.py
python src/clean_data.py
python src/annotate.py
python src/spell_check.py
python src/pattern_detect.py
python src/analyze.py
python src/report.py
python src/save_outputs.py
```

---

## 👤 Author

**Mridul Sharma**
B.Tech CSE (AI & ML) · IILM University × IBM 
[GitHub](https://github.com/MridulSharma02)