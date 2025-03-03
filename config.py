from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv('7522148561:AAFNUN_qD-oCjRs3BGM084AJPBwyN1T2HCQ')
OPENROUTER_API_KEY = os.getenv('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')
SITE_URL = "https://yoursiteurl.com"
SITE_NAME = "DeepSeekBot"
MAX_MEMORY_MESSAGES = 5
SYSTEM_PROMPT = """solo puedes hablar de gatos, habla solo sobre los gatos.
1. las respuestas deben ser breves y concisas."""
