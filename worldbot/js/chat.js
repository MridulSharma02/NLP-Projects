// ============================================================
//  Chat Module
//  Handles:
//    - Maintaining conversation history
//    - Calling the Anthropic Claude API (NLG)
//    - Rendering messages in the UI
// ============================================================

const Chat = {
  history: [],   // full conversation history sent to API each turn

  // ── Append a message bubble to the chat window ──
  appendMessage(role, htmlContent) {
    const container = document.getElementById("messages");
    const div = document.createElement("div");
    div.className = `msg ${role}`;

    const avatar = document.createElement("div");
    avatar.className = `avatar ${role}`;
    avatar.textContent = role === "bot" ? "W" : "U";

    const bubble = document.createElement("div");
    bubble.className = `bubble ${role}`;
    bubble.innerHTML = htmlContent;

    div.appendChild(avatar);
    div.appendChild(bubble);
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
    return bubble;
  },

  // ── Show a "thinking..." indicator ──
  showTyping() {
    const container = document.getElementById("messages");
    const div = document.createElement("div");
    div.className = "msg bot";
    div.id = "typing-indicator";
    div.innerHTML = `
      <div class="avatar bot">W</div>
      <div class="bubble bot typing">thinking…</div>`;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
  },

  removeTyping() {
    const el = document.getElementById("typing-indicator");
    if (el) el.remove();
  },

  // ── Call the Anthropic API ──
  async callClaude(userText) {
    // Add user turn to history
    this.history.push({ role: "user", content: userText });

    const response = await fetch(CONFIG.API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${CONFIG.API_KEY}`,
      },
      body: JSON.stringify({
      model: CONFIG.MODEL,
      max_tokens: CONFIG.MAX_TOKENS,
      messages: [
        { role: "system", content: CONFIG.SYSTEM_PROMPT },
        ...this.history
      ]
    })
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.error?.message || "API error");
    }

    const data = await response.json();
    const rawText = data.choices[0].message.content;

    // Push assistant reply into history (clean version without NLU block)
    const cleanText = NLP.cleanResponse(rawText);
    this.history.push({ role: "assistant", content: cleanText });

    return rawText;   // return raw so NLU block can be parsed
  }
};
