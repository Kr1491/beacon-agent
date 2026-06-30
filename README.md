# Beacon

**An agent that finds, ranks, translates, and explains opportunities — for students anywhere the listings don't reach.**

Built for the Kaggle AI Agents: Intensive Vibe Coding Capstone Project · Track: **Agents for Good**

🔗 **Live demo:** https://kr1491.github.io/beacon-agent/beacon_agent_demo.html

---

## The problem

Hackathons, internships, and youth programs exist all over the world — but most listings are posted in one or two dominant languages, on platforms that skew toward students already in well-connected cities and institutions. Students in rural districts, smaller towns, and underserved regions of any country are routinely left out, not for lack of ability, but for lack of someone translating and filtering on their behalf.

## What Beacon does

Beacon runs a four-step agent pipeline:

1. **Fetch** — pulls opportunity listings from multiple sources
2. **Filter & rank** — scores each listing against the student's profile (field, education level, region, deadline urgency)
3. **Translate & simplify** — rewrites listings in the student's preferred language, stripping jargon
4. **Explain & deliver** — generates a plain-language reason for *why* each result fits, then delivers it

See [`ARCHITECTURE.md`](./ARCHITECTURE.md) for the full pipeline breakdown, including what's simulated in this demo vs. what a production build would run live.

## Try it

Open [the live demo](https://kr1491.github.io/beacon-agent/beacon_agent_demo.html), fill in a sample student profile (region, language, education level, field), and click "Find opportunities for me" to watch the agent trace run end-to-end.

No installation needed — it's a single self-contained HTML file.

## Repo contents

| File | Purpose |
|---|---|
| `beacon_agent_demo.html` | The working demo — agent pipeline simulation + UI |
| `ARCHITECTURE.md` | Full architecture, including the production (live-LLM) version |
| `README.md` | This file |

## Tools used

HTML/CSS/JS (vanilla, no framework dependency), Google Fonts (Fraunces, Noto Serif Devanagari, Inter). Production target: Gemini API for ranking + translation, Telegram Bot API for delivery.

## Author

Built solo by Krishna Jha for the Kaggle AI Agents Capstone window.
