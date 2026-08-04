// ============================================================
//  Voice Module
//  Handles:
//    STT — Speech-to-Text  (Web Speech API / SpeechRecognition)
//    TTS — Text-to-Speech  (Web Speech API / SpeechSynthesis)
// ============================================================

const Voice = {
  isListening: false,
  ttsEnabled: true,
  recognition: null,
  currentUtterance: null,

  // ── Check browser support ──
  sttSupported() {
    return "webkitSpeechRecognition" in window || "SpeechRecognition" in window;
  },
  ttsSupported() {
    return "speechSynthesis" in window;
  },

  // ── Start / Stop voice input ──
  toggleListening(onResult, onStatusChange) {
    if (this.isListening) {
      this.recognition && this.recognition.stop();
      return;
    }
    if (!this.sttSupported()) {
      onStatusChange("⚠️ Voice input not supported — please use Chrome or Edge");
      return;
    }

    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    this.recognition = new SpeechRecognition();
    this.recognition.lang = document.getElementById("langSelect").value;
    this.recognition.interimResults = true;
    this.recognition.continuous = false;

    this.recognition.onstart = () => {
      this.isListening = true;
      document.getElementById("micBtn").classList.add("listening");
      onStatusChange("🎤 Listening… speak now");
    };

    this.recognition.onresult = (event) => {
      const transcript = Array.from(event.results)
        .map(r => r[0].transcript)
        .join("");
      document.getElementById("textInput").value = transcript;

      if (event.results[event.results.length - 1].isFinal) {
        onStatusChange("✅ Got it! Sending…");
        setTimeout(() => onResult(transcript), 300);
      }
    };

    this.recognition.onerror = (e) => {
      this.isListening = false;
      document.getElementById("micBtn").classList.remove("listening");
      onStatusChange(`⚠️ Voice error (${e.error}) — try again or type`);
    };

    this.recognition.onend = () => {
      this.isListening = false;
      document.getElementById("micBtn").classList.remove("listening");
    };

    this.recognition.start();
  },

  // ── Speak text aloud ──
  speak(text) {
    if (!this.ttsEnabled || !this.ttsSupported()) return;
    speechSynthesis.cancel();
    const lang = document.getElementById("langSelect").value;
    const utt = new SpeechSynthesisUtterance(text);
    utt.lang = lang;
    utt.rate = 0.95;
    utt.pitch = 1;
    this.currentUtterance = utt;
    speechSynthesis.speak(utt);
  },

  // ── Toggle TTS on/off ──
  toggleTTS() {
    this.ttsEnabled = !this.ttsEnabled;
    const btn = document.getElementById("speakBtn");
    btn.classList.toggle("muted", !this.ttsEnabled);
    if (!this.ttsEnabled) speechSynthesis.cancel();
    return this.ttsEnabled;
  }
};
