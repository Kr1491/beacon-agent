# Beacon — Architecture

**Track:** Agents for Good
**One-line pitch:** An agent that finds, ranks, translates, and explains hackathon/internship opportunities for students in rural and underserved regions worldwide who are cut off from them by language and platform fragmentation.

## The problem
Opportunity listings (hackathons, internships, govt schemes) are scattered across many platforms, almost always posted in English, and written assuming the reader already knows how to evaluate eligibility and relevance. Students in rural/regional areas are disproportionately excluded — not because they lack ability, but because of three compounding barriers:
1. **Discovery** — they don't know where to look (platforms aren't designed for them, ads target urban/elite colleges).
2. **Language** — listings are in English; regional language is the language of confidence.
3. **Relevance filtering** — even when found, students can't quickly tell if they qualify or if it's "for people like them."

## Why an agent (not a static directory)
A static aggregator site still requires the student to read English, judge eligibility themselves, and trust an unfamiliar source. An agent is the right shape for this because the core task is **multi-step reasoning over each student's specific situation**, repeated per source, per listing:
fetch → filter by eligibility → rank by genuine fit and urgency → translate/simplify → explain *why* in plain language.
That reasoning chain is what a knowledgeable senior or career counselor would normally do for a student — the agent is standing in for that missing local guidance.

## Pipeline (production architecture)

```
 ┌─────────────┐   ┌──────────────────┐   ┌────────────────────┐   ┌───────────────────┐
 │  1. FETCH   │ → │ 2. FILTER & RANK │ → │ 3. TRANSLATE &      │ → │ 4. EXPLAIN & SEND  │
 │             │   │                  │   │    SIMPLIFY         │   │                    │
 │ Pull listings│   │ LLM scores each │   │ LLM rewrites listing│   │ Deliver via        │
 │ from sources │   │ listing against │   │ in user's language, │   │ Telegram bot /     │
 │ (national/    │   │ user profile:    │   │ removes jargon,     │   │ web chat — channel │
 │ global program│   │ field, education,│   │ keeps eligibility   │   │ chosen for low     │
 │ boards, govt   │   │ region, deadline │   │ facts exact         │   │ data/literacy      │
 │ youth portals) │   │ urgency          │   │                     │   │ friction            │
 └─────────────┘   └──────────────────┘   └────────────────────┘   └───────────────────┘
```

- **Step 1 (Fetch):** scheduled scraping/API pulls from a fixed set of sources, normalized into a common schema (title, field, eligibility, deadline, remote/in-person, link).
- **Step 2 (Filter & Rank):** an LLM call (Gemini) takes the student's profile + the normalized listings and returns a ranked shortlist with a relevance score — this is where "is this realistically for me" judgment happens, which a keyword filter can't do well (e.g. recognizing that a diploma student is eligible for a scheme that says "undergraduate or equivalent technical qualification").
- **Step 3 (Translate & Simplify):** a second LLM call translates and rewrites the listing in the student's language, holding factual details (dates, eligibility) fixed while simplifying the surrounding language.
- **Step 4 (Explain & Deliver):** the agent generates a one-line "why this fits you" explanation per result and sends it through a low-friction channel.

## What the demo shows
The attached demo (`beacon_agent_demo.html`) simulates this exact four/five-step pipeline end-to-end in the browser, with a visible agent trace so the reasoning process is transparent rather than a black box. To keep the demo self-contained and judge-runnable with no API keys, the LLM calls in steps 2–4 are replaced with a small rule-based scorer and a pre-built translation table covering Hindi, Spanish, and Swahili for the seed dataset — this is disclosed directly in the demo's footer. The seed dataset (6 representative opportunity types — an open source mentorship program, a national hackathon, a government youth internship scheme, a design hackathon, an agri-tech fellowship, and a small business challenge — modeled on real program structures across South Asia, Latin America, and East Africa) demonstrates the kind of source diversity step 1 would pull from live in any given country or region.

## What would change for a full production build
- Swap the rule-based scorer/translator for live Gemini API calls.
- Add a scheduled fetch job (cron) hitting real source APIs/RSS where available, and a lightweight scraper where not.
- Move delivery to a Telegram bot (no app install, works on basic smartphones, supports voice notes for low-literacy users).
- Add a feedback loop: track which recommendations a student actually applies to, to improve ranking over time.

## Tools used in this build
- Frontend: HTML/CSS/JS (vanilla), Google Fonts (Fraunces, Noto Serif Devanagari, Inter)
- No external API calls in the demo build (works offline / without keys)
- Production target: Gemini API for ranking + translation, Telegram Bot API for delivery
