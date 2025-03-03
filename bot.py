import telebot
import requests
import json
from collections import defaultdict
from config import TELEGRAM_TOKEN, OPENROUTER_API_KEY, SITE_URL, SITE_NAME, MAX_MEMORY_MESSAGES, SYSTEM_PROMPT

bot = telebot.TeleBot(TELEGRAM_TOKEN)
user_conversations = defaultdict(list)

def get_ai_response(user_id, new_message):
    # Construir el historial de mensajes comenzando con el system prompt
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    
    # Agregar el historial de conversación existente
    if user_id in user_conversations:
        messages.extend(user_conversations[user_id])
    
    # Agregar el nuevo mensaje del usuario
    current_message = {"role": "user", "content": new_message}
    messages.append(current_message)
    
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": SITE_URL,
                "X-Title": SITE_NAME,
            },
            json={
                "model": "deepseek/deepseek-chat:free",
                "messages": messages
            }
        )
        
        response.raise_for_status()  # Esto lanzará una excepción si hay error HTTP
        ai_response = response.json()['choices'][0]['message']['content']
        
        # Actualizar el historial de conversación
        user_conversations[user_id].append(current_message)
        user_conversations[user_id].append({"role": "assistant", "content": ai_response})
        
        # Mantener solo los últimos MAX_MEMORY_MESSAGES * 2 mensajes (pregunta + respuesta)
        if len(user_conversations[user_id]) > MAX_MEMORY_MESSAGES * 2:
            user_conversations[user_id] = user_conversations[user_id][-(MAX_MEMORY_MESSAGES * 2):]
        
        return ai_response
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return "Lo siento, hubo un error al procesar tu mensaje."

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_conversations[message.from_user.id] = []  # Limpiar la conversación
    bot.reply_to(message, "¡Hola! Soy un chatbot con IA. ¿En qué puedo ayudarte?")

@bot.message_handler(commands=['clearmemory'])
def clear_memory(message):
    user_conversations[message.from_user.id] = []
    bot.reply_to(message, "He limpiado mi memoria de nuestra conversación anterior.")

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, get_ai_response(message.from_user.id, message.text))

if __name__ == "__main__":
    print("Bot iniciado...")
    bot.polling()
