// ============================================================
//  App Entry Point
//  Wires together: Chat, NLP (NLU + NLE), Voice (STT + TTS)
//  and the Pipeline UI
// ============================================================

// ── Pipeline UI helpers ──
function setPipeline(stage) {
  const ids = ["input","nlu","proc","nlg","nle","output"];
  const map  = { nlu:"active-nlu", proc:"active-proc", nlg:"active-nlg",
                 nle:"active-nle", output:"active-out" };
  ids.forEach(id => {
    const el = document.getElementById("pipe-" + id);
    el.className = "pipe-badge";
    if (id === stage && map[stage]) el.classList.add(map[stage]);
  });
}

function setStatus(msg) {
  document.getElementById("statusBar").textContent = msg;
}

// ── Suggestion chips ──
function fillSuggestion(el) {
  document.getElementById("textInput").value = el.textContent;
  document.getElementById("textInput").focus();
}

// ── Main send flow ──
async function sendMessage() {
  const input = document.getElementById("textInput");
  const text  = input.value.trim();
  if (!text) return;
  input.value = "";

  // Hide suggestion chips after first message
  document.getElementById("suggestions").style.display = "none";

  // 1️⃣  INPUT stage
  setPipeline("input");
  setStatus("Processing your input…");
  Chat.appendMessage("user", text);   // plain text for now; tags added after NLU

  // 2️⃣  NLU stage (simulated delay for visual effect)
  await delay(400);
  setPipeline("nlu");
  setStatus("NLU — extracting intent, entities & sentiment…");

  // 3️⃣  PROCESSING stage
  await delay(600);
  setPipeline("proc");
  setStatus("Context Manager — building conversation context…");

  // 4️⃣  NLG stage — actual API call
  await delay(500);
  setPipeline("nlg");
  setStatus("NLG — generating response via Claude API…");
  Chat.showTyping();

  try {
    const rawText = await Chat.callClaude(text);

    // Parse NLU block from response
    const nluData  = NLP.extractNLU(rawText);
    const cleanText = NLP.cleanResponse(rawText);

    // Annotate the user's bubble with NLU tags
    const userBubbles = document.querySelectorAll(".msg.user .bubble");
    const lastUserBubble = userBubbles[userBubbles.length - 1];
    if (lastUserBubble && nluData) {
      const infoDiv = document.createElement("div");
      infoDiv.className = "nlp-info";
      infoDiv.innerHTML = NLP.renderNLUTags(nluData);
      lastUserBubble.appendChild(infoDiv);
    }

    // 5️⃣  NLE stage
    Chat.removeTyping();
    await delay(500);
    setPipeline("nle");
    setStatus("NLE — evaluating response quality…");
    await delay(600);

    // 6️⃣  OUTPUT stage
    setPipeline("output");
    setStatus("Delivering response…");

    const nleData = NLP.evaluate(cleanText);
    const botHTML = `
      ${cleanText.replace(/\n/g, "<br>")}
      <div class="nlp-info">
        ${NLP.renderNLETags(nleData)}
      </div>`;

    Chat.appendMessage("bot", botHTML);

    // Speak response aloud
    Voice.speak(cleanText);

    // Reset
    await delay(300);
    setPipeline("");
    setStatus("Ready — type or tap 🎤 to speak");

  } catch (err) {
    Chat.removeTyping();
    Chat.appendMessage("bot",
      `<span style="color:#c62828">⚠️ Error: ${err.message}</span><br>
       Check your API key in <code>js/config.js</code>`);
    setPipeline("");
    setStatus("Error — check your API key in js/config.js");
    console.error(err);
  }
}

// ── Voice input button ──
function toggleVoice() {
  Voice.toggleListening(
    (transcript) => {
      document.getElementById("textInput").value = transcript;
      sendMessage();
    },
    (statusMsg) => setStatus(statusMsg)
  );
}

// ── TTS toggle button ──
function toggleTTS() {
  const enabled = Voice.toggleTTS();
  setStatus(enabled ? "🔊 Voice output enabled" : "🔇 Voice output disabled");
}

// ── Utility ──
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
