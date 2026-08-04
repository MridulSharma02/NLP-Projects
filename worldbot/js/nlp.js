// ============================================================
//  NLP Module
//  Handles:
//    NLU — extracts intent, entities, sentiment from Claude's response
//    NLE — evaluates response quality (fluency, coherence, length)
// ============================================================

const NLP = {

  // ── NLU: Parse the <NLU>{...}</NLU> block Claude returns ──
  extractNLU(rawText) {
    const match = rawText.match(/<NLU>([\s\S]*?)<\/NLU>/);
    if (!match) return null;
    try {
      return JSON.parse(match[1]);
    } catch (e) {
      console.warn("NLU parse error:", e);
      return null;
    }
  },

  // ── NLU: Strip the <NLU> block from the response text ──
  cleanResponse(rawText) {
    return rawText.replace(/<NLU>[\s\S]*?<\/NLU>/, "").trim();
  },

  // ── NLE: Natural Language Evaluation ──
  // Scores the bot response on three simple metrics
  evaluate(text) {
    const words = text.split(/\s+/).filter(Boolean);
    const sentences = text.split(/[.!?]+/).filter(Boolean);

    // Fluency: penalise very short or very long responses
    const fluency = words.length < 5  ? 60
                  : words.length > 200 ? 78
                  : Math.min(98, 72 + Math.floor(words.length / 3));

    // Coherence: rough proxy — sentence variety
    const avgWords = words.length / Math.max(sentences.length, 1);
    const coherence = avgWords > 4 && avgWords < 40 ? "high" : "medium";

    // Relevance: did we actually get a non-trivial answer?
    const relevance = words.length >= 10 ? "high" : "medium";

    return { fluency, coherence, relevance };
  },

  // ── Build HTML tags to show NLU annotations ──
  renderNLUTags(nluData) {
    if (!nluData) return "";
    let html = "";
    if (nluData.intent)
      html += `<span class="nlp-tag tag-intent">intent: ${nluData.intent}</span>`;
    if (nluData.entities && nluData.entities.length)
      nluData.entities.forEach(e => {
        html += `<span class="nlp-tag tag-entity">entity: ${e}</span>`;
      });
    if (nluData.sentiment)
      html += `<span class="nlp-tag tag-sentiment">sentiment: ${nluData.sentiment}</span>`;
    if (nluData.topic)
      html += `<span class="nlp-tag tag-entity">topic: ${nluData.topic}</span>`;
    return html;
  },

  // ── Build HTML tags to show NLE scores ──
  renderNLETags(nleData) {
    return `
      <span class="nlp-tag tag-nle">fluency: ${nleData.fluency}%</span>
      <span class="nlp-tag tag-nle">coherence: ${nleData.coherence}</span>
      <span class="nlp-tag tag-nle">relevance: ${nleData.relevance}</span>
    `;
  }
};
