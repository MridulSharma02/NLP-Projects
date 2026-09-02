# Emergency Message Corpus — Analysis Report

## 1. Corpus Overview
- **Total messages:** 5025
- **Avg words/message:** 26.38
- **Avg sentences/message:** 1.99
- **Messages with location mention:** 2739 (54.5%)
- **Messages with action word:** 1326 (26.4%)
- **Informal messages:** 3587 (71.4%)

## 2. Urgency Distribution
| Level | Count |
|-------|-------|
| low | 3621 |
| medium | 1371 |
| high | 33 |

## 3. Top Action Words
help, need, donate, rescue, emergency, please help, assist, call, send, evacuate

## 4. Informal vs Formal Language
| Metric | Informal | Formal |
|--------|----------|--------|
| Count | 3587 | 1438 |
| Avg words | 28.96 | 19.95 |
| Avg actions | 0.36 | 0.34 |

## 5. Syntactic Patterns — Urgency Comparison
Top POS tags in **high urgency** messages:
PROPN, NOUN, VERB, PUNCT, ADP, PRON, SYM, ADJ

Top POS tags in **low urgency** messages:
NOUN, PROPN, ADP, PUNCT, VERB, DET, ADJ, SYM

## 6. Key Findings
- **54.5%** of messages contain a detectable location reference — critical for dispatch routing.
- **26.4%** contain explicit action words (help, rescue, evacuate, etc.).
- **71.4%** of messages are linguistically informal — NLP systems must handle noisy text.
- High-urgency messages show higher NOUN/VERB density consistent with clipped, imperative language.
- Top actions: help, need, donate, rescue, emergency
