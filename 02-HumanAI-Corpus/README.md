# 02 — Human vs AI Corpus Analysis

A corpus of human–AI interactions with synthetic linguistic annotations, analyzing structural differences between human and AI generated text.

## Dataset
- Source: [tatsu-lab/alpaca](https://huggingface.co/datasets/tatsu-lab/alpaca)
- Total turns: 4000 (2000 human, 2000 AI)
- Free and publicly available on HuggingFace

## Key Findings
| Metric | Human | AI |
|--------|-------|----|
| Avg Word Count | 10.45 | 47.47 |
| Avg Sentence Count | 1.01 | 2.97 |
| Avg Word Length | 4.55 | 4.35 |

## How to Run
```bash
pip install datasets pandas nltk matplotlib
python download_data.py
python annotate.py
python analyze.py
python report.py
```

## Files
- `download_data.py` — downloads dataset from HuggingFace
- `annotate.py` — adds POS tags, word count, sentence count
- `analyze.py` — generates comparison charts
- `report.py` — generates text report
- `analysis_chart.png` — output chart
- `report.txt` — output report

## Live Demo
[View on GitHub Pages](https://mridulsharma02.github.io/NLP-Projects/02-HumanAI-Corpus/)