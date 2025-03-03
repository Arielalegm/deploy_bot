from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
SITE_URL = "https://github.com/Arielalegm/deploy_bot"  # Actualizada a una URL real
SITE_NAME = "DeepSeekBot"
MAX_MEMORY_MESSAGES = 5
SYSTEM_PROMPT = """solo puedes hablar de gatos, habla solo sobre los gatos.
1. las respuestas deben ser breves y concisas."""
