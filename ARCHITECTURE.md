# Beacon — Architecture

**Track:** Agents for Good
**One-line pitch:** An agent that finds, ranks, translates, and explains hackathon/internship opportunities for students in rural and underserved regions worldwide who are cut off from them by language and platform fragmentation.

## The problem
Opportunity listings (hackathons, internships, govt schemes) are scattered across many platforms, almost always posted in one or two dominant languages, and written assuming the reader already knows how to evaluate eligibility and relevance. Students in rural/regional areas are disproportionately excluded — not because they lack ability, but because of three compounding barriers:
1. **Discovery** — they don't know where to look (platforms aren't designed for them, ads target urban/elite colleges).
2. **Language** — listings are in English or another dominant language; the student's own language is the language of confidence.
3. **Relevance filtering** — even when found, students can't quickly tell if they qualify or if it's "for people like them."

## Why an agent (not a static directory)
A static aggregator site still requires the student to read an unfamiliar language, judge eligibility themselves, and trust an unfamiliar source. An agent is the right shape for this because the core task is **multi-step reasoning over each student's specific situation**, repeated per source, per listing:
fetch → filter by eligibility → rank by genuine fit and urgency → translate/simplify → explain *why* in plain language.
That reasoning chain is what a knowledgeable senior or career counselor would normally do for a student — the agent is standing in for that missing local guidance.

## Pipeline (production architecture)

```
 ┌─────────────┐   ┌──────────────────┐   ┌────────────────────┐   ┌───────────────────┐
 │  1. FETCH   │ → │ 2. FILTER & RANK │ → │ 3. TRANSLATE &      │ → │ 4. EXPLAIN & SEND  │
 │             │   │                  │   │    SIMPLIFY         │   │                    │
 │ Pull listings│   │ LLM scores each │   │ LLM rewrites listing│   │ Deliver via        │
 │ from sources │   │ listing against │   │ in user's language, │   │ Telegram bot —     │
 │ (national/    │   │ user profile:    │   │ removes jargon,     │   │ channel chosen for │
 │ global program│   │ field, education,│   │ keeps eligibility   │   │ low data/literacy  │
 │ boards, govt   │   │ region, deadline │   │ facts exact         │   │ friction            │
 │ youth portals) │   │ urgency          │   │                     │   │                    │
 └─────────────┘   └──────────────────┘   └────────────────────┘   └───────────────────┘
```

- **Step 1 (Fetch):** scheduled scraping/API pulls from a fixed set of sources, normalized into a common schema (title, field, eligibility, deadline, remote/in-person, link).
- **Step 2 (Filter & Rank):** an LLM call (Gemini) takes the student's profile + the normalized listings and returns a ranked shortlist — this is where "is this realistically for me" judgment happens, which a keyword filter can't do well (e.g. recognizing that a diploma student is eligible for a scheme that says "undergraduate or equivalent technical qualification").
- **Step 3 (Translate & Simplify):** the same call also translates and rewrites the listing in the student's language, holding factual details (dates, eligibility) fixed while simplifying the surrounding language.
- **Step 4 (Explain & Deliver):** the agent generates a short "why this fits you" explanation per result, in the student's language, and sends it through a low-friction channel.

## What the demo shows — and how it actually calls Gemini
The attached demo (`beacon_agent_demo.html`) runs steps 2–4 as a **live Gemini API call**, not a simulation. The user's profile and the seed listings are sent to Gemini in a single structured prompt; the model does the actual filtering, ranking, translation, and reasoning, and returns a JSON array that's rendered directly in the UI. The visible agent trace (fetch → call Gemini → response received) reflects what's actually happening, not a scripted animation.

Step 1 (Fetch) uses a fixed seed dataset of six representative opportunity types — an open source mentorship program, a national hackathon, a government youth internship scheme, a design hackathon, an agri-tech fellowship, and a small business challenge — modeled on real program structures across South Asia, Latin America, and East Africa. Live scraping of opportunity platforms is out of scope for a browser-only demo, so this step is not live.

If no API key is supplied, or the Gemini call fails for any reason, the demo falls back to a local rule-based simulation of the same four steps, clearly labeled as simulated in the UI, so the demo never breaks for a judge testing it without a key.

## An honest gap: who would actually use this, and how

The browser demo asks the user to paste a Gemini API key. This is a demo constraint, not a product decision — a static, publicly hosted HTML file has no backend to hold a key safely, so the key has to be supplied by whoever is running the demo (a judge, a developer).

**A rural student would never do this**, and the real product does not ask them to. The intended delivery layer is a **Telegram bot**: the API key lives on a server the student never sees, and the student interacts entirely through a chat message — e.g. sending "find me internships, I'm studying commerce, class 12" in their own language, and getting a translated, ranked, explained reply back. This requires:
- No app beyond Telegram, which is already installed for most target users
- No English literacy
- No understanding of what an API key or LLM is
- Works over low bandwidth, on basic smartphones

This is the actual shape of the product. The browser demo exists to make the agent's reasoning visible and judge-runnable within the constraints of a static-site hackathon submission.

## What would change for a full production build
- Move delivery to a Telegram bot with a server-side Gemini key — the primary interface for real users, not the browser demo.
- Add a scheduled fetch job (cron) hitting real source APIs/RSS where available, and a lightweight scraper where not.
- Add voice-note input/output support in the Telegram bot for low-literacy users.
- Add a feedback loop: track which recommendations a student actually applies to, to improve ranking over time.

## Tools used in this build
- Frontend: HTML/CSS/JS (vanilla), Google Fonts (Syne, Source Serif 4, JetBrains Mono)
- Live Gemini API call (`gemini-2.0-flash`) for filtering, ranking, translation, and explanation, with a rule-based local fallback
- Production target: Gemini API (server-side) + Telegram Bot API for delivery
