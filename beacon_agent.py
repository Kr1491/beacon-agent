import os
import json
import re
import requests
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ==========================================
# CONFIGURATION
# ==========================================
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ==========================================
# BEACON AGENT PIPELINE
# ==========================================

class BeaconAgent:
    def __init__(self):
        self.student_profile = {}

    def set_profile(self, text):
        """Parses the student's text to set their profile."""
        self.student_profile = {
            "raw_input": text,
            "language": self._extract_language(text)
        }
        return self.student_profile

    def _extract_language(self, text):
        """Simple heuristic to guess language or default to English"""
        text_lower = text.lower()
        if "hindi" in text_lower: return "Hindi"
        if "spanish" in text_lower: return "Spanish"
        if "french" in text_lower: return "French"
        return "English" # Default

    # STEP 1: FETCH
    def fetch_opportunities(self):
        """
        In production, you would scrape Devpost, LinkedIn, or use APIs.
        For this functional demo, we simulate a live fetch from an open data source.
        """
        print("[Beacon Pipeline] Step 1: Fetching opportunities...")
        # Simulating a fetched dataset from multiple platforms
        return [
            {"title": "Global AI Hackathon 2024", "desc": "48-hour virtual hackathon building AI for social good. Open globally.", "skills": ["AI", "Python"], "deadline": "2024-12-15"},
            {"title": "AgriTech Remote Internship", "desc": "3-month internship building IoT soil sensors. Stipend provided.", "skills": ["IoT", "Python", "Agriculture"], "deadline": "2024-11-30"},
            {"title": "Advanced Web3 Bootcamp", "desc": "6-week intensive Solidity program. Requires prior crypto experience.", "skills": ["Blockchain", "Web3"], "deadline": "2024-11-10"}
        ]

    # STEPS 2, 3 & 4: FILTER, RANK, TRANSLATE, SIMPLIFY & EXPLAIN
    def process_with_gemini(self, opportunities):
        print("[Beacon Pipeline] Steps 2-4: Filtering, Translating, and Explaining via Gemini...")
        
        prompt = f"""
        You are Beacon, an AI Opportunity Agent for rural students.
        Student Profile Context: {self.student_profile['raw_input']}
        Target Language: {self.student_profile['language']}

        Here is a JSON list of fetched opportunities:
        {json.dumps(opportunities)}

        Your Tasks:
        1. FILTER & RANK: Select only the top 2 most relevant to the student's skills/situation.
        2. TRANSLATE & SIMPLIFY: Translate the title and description into {self.student_profile['language']}. Keep it simple.
        3. EXPLAIN: Write a 1-sentence personalized explanation of WHY it fits the student.

        Return STRICTLY a JSON array with this format:
        [
          {{
            "translated_title": "...",
            "translated_desc": "...",
            "why_it_fits": "...",
            "deadline": "..."
          }}
        ]
        Do not include markdown code blocks (```) in your response.
        """

        try:
            response = model.generate_content(prompt)
            # Clean up response to ensure it's valid JSON
            clean_text = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_text)
        except Exception as e:
            print(f"Gemini Error: {e}")
            return []

# ==========================================
# TELEGRAM BOT DELIVERY (STEP 5: DELIVER)
# ==========================================

beacon = BeaconAgent()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🚦 Welcome to Beacon!\n\n"
        "I am your AI Opportunity Agent. I find, rank, translate, and explain hackathons and internships for you.\n\n"
        "Please tell me about yourself:\n"
        "- Your skills (e.g., Python, UI/UX)\n"
        "- Your background (e.g., rural student, first year)\n"
        "- Your preferred language (e.g., Hindi, Spanish)"
    )
    await update.message.reply_text(welcome_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text("🤖 Beacon is on it! Fetching and processing opportunities...")

    # 1. Set Profile
    beacon.set_profile(user_text)
    
    # 2. Fetch
    raw_opps = beacon.fetch_opportunities()
    
    # 3. Process (Filter, Translate, Explain)
    processed_opps = beacon.process_with_gemini(raw_opps)

    # 4. Deliver
    if not processed_opps:
        await update.message.reply_text("Sorry, I couldn't find any matching opportunities right now.")
        return

    for opp in processed_opps:
        message = (
            f"🎯 *{opp.get('translated_title', 'Opportunity')}*\n\n"
            f"📝 {opp.get('translated_desc', 'No description')}\n\n"
            f"🗓️ *Deadline:* {opp.get('deadline', 'N/A')}\n\n"
            f"💡 *Why it fits you:* {opp.get('why_it_fits', 'Great match!')}"
        )
        await update.message.reply_text(message, parse_mode="Markdown")

def main():
    print("Beacon Telegram Bot is running...")
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot until you press Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()
