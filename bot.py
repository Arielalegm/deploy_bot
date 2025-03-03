import telebot
import requests
import json
from collections import defaultdict
from config import TELEGRAM_TOKEN, OPENROUTER_API_KEY, SITE_URL, SITE_NAME, MAX_MEMORY_MESSAGES, SYSTEM_PROMPT

bot = telebot.TeleBot(TELEGRAM_TOKEN)
user_conversations = defaultdict(list)

def get_ai_response(user_id, new_message):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    
    if user_id in user_conversations:
        messages.extend(user_conversations[user_id])
    
    current_message = {"role": "user", "content": new_message}
    messages.append(current_message)
    
    try:
        print("Enviando solicitud a OpenRouter...")
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "HTTP-Referer": SITE_URL,
                "X-Title": SITE_NAME,
                "Authorization": f"Bearer {OPENROUTER_API_KEY.strip()}",  # Asegurarse de que no hay espacios
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-ai/deepseek-chat-1.3b",  # Actualizado el nombre del modelo
                "messages": messages
            }
        )
        
        print(f"Estado de respuesta: {response.status_code}")
        print(f"Respuesta completa: {response.text}")  # Añadido para debug
        
        if response.status_code != 200:
            print(f"Error en la API: {response.text}")  # Debug log
            return "Lo siento, hubo un error en la comunicación con la IA."
            
        response_data = response.json()
        ai_response = response_data['choices'][0]['message']['content']
        
        # Actualizar conversación
        user_conversations[user_id].append(current_message)
        user_conversations[user_id].append({"role": "assistant", "content": ai_response})
        
        if len(user_conversations[user_id]) > MAX_MEMORY_MESSAGES * 2:
            user_conversations[user_id] = user_conversations[user_id][-(MAX_MEMORY_MESSAGES * 2):]
        
        return ai_response
        
    except requests.exceptions.RequestException as e:
        print(f"Error de red: {str(e)}")
        return "Lo siento, hubo un error de conexión."
    except json.JSONDecodeError as e:
        print(f"Error al procesar JSON: {str(e)}")
        return "Lo siento, hubo un error al procesar la respuesta."
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return "Lo siento, ocurrió un error inesperado."

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
