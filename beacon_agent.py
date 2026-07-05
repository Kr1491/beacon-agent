import os
import json
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ==========================================
# CONFIGURATION — reads from environment variables, never hardcoded
# ==========================================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not GEMINI_API_KEY or not TELEGRAM_BOT_TOKEN:
    raise SystemExit(
        "Missing environment variables.\n"
        "Set them before running, e.g.:\n"
        "  export GEMINI_API_KEY='your-key-here'\n"
        "  export TELEGRAM_BOT_TOKEN='your-token-here'\n"
        "  python beacon_agent.py"
    )

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# ==========================================
# BEACON AGENT PIPELINE
# ==========================================

class BeaconAgent:
    def __init__(self):
        self.student_profile = {}

    def set_profile(self, text):
        """Parses the student's free-text message into a lightweight profile."""
        self.student_profile = {
            "raw_input": text,
            "language": self._extract_language(text)
        }
        return self.student_profile

    def _extract_language(self, text):
        """Simple keyword heuristic to guess preferred language, defaults to English."""
        text_lower = text.lower()
        language_map = {
            "hindi": "Hindi", "spanish": "Spanish", "french": "French",
            "swahili": "Swahili", "tamil": "Tamil", "bengali": "Bengali",
            "portuguese": "Portuguese", "arabic": "Arabic"
        }
        for keyword, language in language_map.items():
            if keyword in text_lower:
                return language
        return "English"

    # STEP 1: FETCH
    def fetch_opportunities(self):
        """
        In production, this would pull from live sources (Devpost, Internshala,
        government youth portals, etc.) on a scheduled job. For this demo,
        it returns a fixed seed dataset so the pipeline is fully testable
        without external scraping infrastructure.
        """
        print("[Beacon Pipeline] Step 1: Fetching opportunities...")
        return [
            {"title": "Global AI Hackathon", "desc": "48-hour virtual hackathon building AI for social good. Open globally, beginner track available.", "skills": ["AI", "Python"], "deadline": "Rolling entry"},
            {"title": "AgriTech Remote Internship", "desc": "3-month remote internship building IoT soil sensors. Stipend provided.", "skills": ["IoT", "Python", "Agriculture"], "deadline": "Closes in 20 days"},
            {"title": "Advanced Web3 Bootcamp", "desc": "6-week intensive Solidity program. Requires prior blockchain experience.", "skills": ["Blockchain", "Web3"], "deadline": "Closes in 10 days"},
            {"title": "Youth Business Plan Challenge", "desc": "District-level business plan competition for first-time entrepreneurs.", "skills": ["Business"], "deadline": "Closes in 25 days"},
            {"title": "UI/UX Design Sprint", "desc": "Fully remote design sprint judged on prototypes, no coding required.", "skills": ["Design"], "deadline": "Closes in 9 days"}
        ]

    # STEPS 2-4: FILTER, RANK, TRANSLATE, SIMPLIFY & EXPLAIN
    def process_with_gemini(self, opportunities):
        print("[Beacon Pipeline] Steps 2-4: Filtering, translating, and explaining via Gemini...")

        prompt = f"""You are Beacon, an AI opportunity agent for students in rural and underserved regions.

Student's message: {self.student_profile['raw_input']}
Target language: {self.student_profile['language']}

Fetched opportunities (JSON):
{json.dumps(opportunities)}

Tasks:
1. FILTER & RANK: select only the top 2 most relevant to the student's stated skills/situation, using judgment rather than exact keyword matching.
2. TRANSLATE & SIMPLIFY: translate the title and description into {self.student_profile['language']}, removing jargon while keeping factual details (dates, requirements) exact.
3. EXPLAIN: write one sentence, in {self.student_profile['language']}, on why this specifically fits this student.

Return STRICTLY a JSON array, no markdown code fences, in this shape:
[{{"translated_title": "...", "translated_desc": "...", "why_it_fits": "...", "deadline": "..."}}]"""

        try:
            response = model.generate_content(prompt)
            clean_text = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_text)
        except Exception as e:
            print(f"Gemini error: {e}")
            return []

# ==========================================
# TELEGRAM BOT DELIVERY (STEP 4: DELIVER)
# ==========================================

beacon = BeaconAgent()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🚦 Welcome to Beacon!\n\n"
        "I find, rank, translate, and explain hackathons and internships for you — in your own language.\n\n"
        "Tell me a bit about yourself:\n"
        "- Your skills or field (e.g. Python, agriculture, design)\n"
        "- Your background (e.g. first-year student, diploma holder)\n"
        "- Your preferred language (e.g. Hindi, Spanish, Swahili)"
    )
    await update.message.reply_text(welcome_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text("🤖 On it — fetching and matching opportunities for you...")

    beacon.set_profile(user_text)
    raw_opportunities = beacon.fetch_opportunities()
    processed = beacon.process_with_gemini(raw_opportunities)

    if not processed:
        await update.message.reply_text(
            "Sorry, I couldn't process that right now — please try again in a moment."
        )
        return

    for opp in processed:
        message = (
            f"🎯 *{opp.get('translated_title', 'Opportunity')}*\n\n"
            f"📝 {opp.get('translated_desc', 'No description available')}\n\n"
            f"🗓️ *Deadline:* {opp.get('deadline', 'N/A')}\n\n"
            f"💡 *Why it fits you:* {opp.get('why_it_fits', '')}"
        )
        await update.message.reply_text(message, parse_mode="Markdown")

def main():
    print("Beacon Telegram bot is running...")
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()