const express = require("express");
const fetch = (...args) => import("node-fetch").then(({default: fetch}) => fetch(...args));
require("dotenv").config();

const app = express();
app.use(express.json());
app.use(express.static("."));

app.post("/chat", async (req, res) => {
  try {
    const response = await fetch("https://api.groq.com/openai/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${process.env.GROQ_API_KEY}`
      },
      body: JSON.stringify(req.body)
    });
    const data = await response.json();
    res.json(data);
  } catch (err) {
    console.error("Server error:", err.message);
    res.status(500).json({ error: err.message });
  }
});

app.listen(3000, () => console.log("✅ WorldBot running at http://localhost:3000"));