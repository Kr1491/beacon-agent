# Beacon

**An agent that finds, ranks, translates, and explains opportunities — for students anywhere the listings don't reach.**

Built for the Kaggle AI Agents: Intensive Vibe Coding Capstone Project · Track: **Agents for Good**

🔗 **Browser demo (shows the pipeline):** https://kr1491.github.io/beacon-agent/beacon_agent_demo.html
🤖 **Telegram bot (the actual product):** see setup below

---

## The problem

Hackathons, internships, and youth programs exist all over the world — but most listings are posted in one or two dominant languages, on platforms that skew toward students already in well-connected cities and institutions. Students in rural districts, smaller towns, and underserved regions of any country are routinely left out, not for lack of ability, but for lack of someone translating and filtering on their behalf.

## What Beacon does

Beacon runs a four-step agent pipeline:

1. **Fetch** — pulls opportunity listings from multiple sources
2. **Filter & rank** — scores each listing against the student's profile (field, education level, region, deadline urgency)
3. **Translate & simplify** — rewrites listings in the student's preferred language, stripping jargon
4. **Explain & deliver** — generates a plain-language reason for *why* each result fits, then delivers it

Steps 2–4 are powered by a live Gemini API call, not a script — the model does the actual filtering, ranking, translation, and reasoning.

See [`ARCHITECTURE.md`](./ARCHITECTURE.md) for the full pipeline breakdown.

## Two interfaces, two purposes

This repo contains two working implementations, built deliberately for different jobs:

| | Purpose | Who it's for |
|---|---|---|
| **`beacon_agent_demo.html`** | Shows the pipeline running, step by step, with a visible agent trace | Judges / anyone who wants to see how the agent reasons |
| **`beacon_agent.py`** | The actual product | A real student, messaging a Telegram bot in plain language |

The browser demo requires the user to paste their own Gemini API key, since a public static file has no backend to hold one safely — that's a demo constraint, not how the real product works. The Telegram bot is what a student would actually use: no API key, no browser, no English required, just a message in their own language.

## Try the browser demo

Open [the live demo](https://kr1491.github.io/beacon-agent/beacon_agent_demo.html), paste a Gemini API key (free at [aistudio.google.com/apikey](https://aistudio.google.com/apikey)), fill in a sample student profile, and click "Find opportunities" to watch the agent trace run end-to-end. No key? It falls back to a clearly-labeled simulation so you can still see the flow.

## Run the Telegram bot (the real product)

### 1. Get a Telegram bot token
Open Telegram, message **[@BotFather](https://t.me/BotFather)**, send `/newbot`, and follow the prompts to name your bot. BotFather will give you a token that looks like `123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`.

### 2. Get a Gemini API key
Free at [aistudio.google.com/apikey](https://aistudio.google.com/apikey). If you hit a `429` quota error later, link a billing account in Google Cloud Console (no charge for normal usage) — this unlocks much higher free-tier limits.

### 3. Clone this repo and install dependencies
```bash
git clone https://github.com/Kr1491/beacon-agent.git
cd beacon-agent
pip install -r requirements.txt
```

### 4. Set your keys as environment variables
Never hardcode keys directly into `beacon_agent.py` — especially if you plan to push changes back to a public repo.

**macOS / Linux:**
```bash
export GEMINI_API_KEY="your-gemini-key-here"
export TELEGRAM_BOT_TOKEN="your-botfather-token-here"
```

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your-gemini-key-here"
$env:TELEGRAM_BOT_TOKEN="your-botfather-token-here"
```

### 5. Run the bot
```bash
python beacon_agent.py
```
You should see `Beacon Telegram bot is running...` in the terminal.

### 6. Talk to it
Open Telegram, find your bot by the username you gave it in step 1, send `/start`, then send a message describing yourself, e.g.:

> I'm a diploma student interested in agriculture, I prefer Hindi

The bot will reply with translated, ranked opportunity matches and an explanation for each.

### Stopping the bot
Press `Ctrl+C` in the terminal. The bot only runs while this process is active — for a persistent, always-on bot, it would need to be deployed to a small server (a natural next step, see ARCHITECTURE.md).

## Repo contents

| File | Purpose |
|---|---|
| `beacon_agent_demo.html` | Browser demo — shows the pipeline with a visible agent trace |
| `beacon_agent.py` | The Telegram bot — the actual product |
| `requirements.txt` | Python dependencies for the bot |
| `ARCHITECTURE.md` | Full architecture and design rationale |
| `README.md` | This file |

## Tools used

- **Browser demo:** HTML/CSS/JS (vanilla), Google Fonts (Syne, Source Serif 4, JetBrains Mono)
- **Telegram bot:** Python, `google-generativeai`, `python-telegram-bot`
- **Model:** Gemini 2.0 Flash for filtering, ranking, translation, and explanation

## Author

Built solo by Krishna Jha for the Kaggle AI Agents Capstone (Agents for Good track).
