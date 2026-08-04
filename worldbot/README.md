# 🌐 WorldBot — NLP Chatbot (College Lab Project)

A general-purpose AI chatbot with **Text + Voice** interaction that
demonstrates the full NLP pipeline:  
**Input → NLU → Context Manager → NLG → NLE → Output**

---

## 📁 Project Structure

```
worldbot/
├── index.html          ← Main UI
├── css/
│   └── style.css       ← All styling
├── js/
│   ├── config.js       ← API key + system prompt  ⬅ EDIT THIS
│   ├── nlp.js          ← NLU parsing + NLE evaluation
│   ├── voice.js        ← Speech-to-Text + Text-to-Speech
│   ├── chat.js         ← Claude API calls + message rendering
│   └── app.js          ← Main controller (wires everything)
└── README.md
```

---

## 🚀 Setup (3 steps)

### Step 1 — Get a free API key
1. Go to https://console.anthropic.com/
2. Sign up / log in
3. Click **API Keys** → **Create Key**
4. Copy the key (starts with `sk-ant-...`)

### Step 2 — Paste your key
Open `js/config.js` and replace `YOUR_API_KEY_HERE`:
```js
ANTHROPIC_API_KEY: "sk-ant-xxxxxxxxxxxxxxxx",
```

### Step 3 — Run in VS Code
**Option A — Live Server (recommended)**
1. Install the **Live Server** extension in VS Code
2. Right-click `index.html` → **Open with Live Server**
3. It opens in Chrome at `http://127.0.0.1:5500`

**Option B — Direct browser**
- Just double-click `index.html` to open in Chrome
- ⚠️ Voice input requires http:// (use Live Server) or it works on localhost

---

## 🧠 NLP Components Explained

| Component | What it does | Technology used |
|-----------|-------------|-----------------|
| **NLU** (Natural Language Understanding) | Extracts intent, named entities, sentiment, topic from user input | Claude API (prompted to return structured JSON) |
| **NLG** (Natural Language Generation) | Generates fluent, accurate, context-aware answers | Anthropic Claude API (`claude-sonnet-4-6`) |
| **NLE** (Natural Language Evaluation) | Scores response on fluency %, coherence, relevance | Custom JS scoring logic |
| **STT** (Speech-to-Text) | Converts voice input to text | Web Speech API (`SpeechRecognition`) |
| **TTS** (Text-to-Speech) | Reads bot responses aloud | Web Speech API (`SpeechSynthesis`) |

---

## 🌍 Supported Languages (for voice)
English, Hindi, Spanish, French, Arabic, Chinese, German, Portuguese

---

## ⚠️ Notes
- Voice input works best in **Google Chrome** or **Microsoft Edge**
- The API key is in the frontend JS — for a real production app,
  you would move API calls to a backend server to keep the key secret.
  For a college lab demo, this is fine.
