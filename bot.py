import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

TELEGRAM_BOT_TOKEN = "8014258134:AAFRi5jhsgMGMXklkybX85XKvVZqBy-xE2o"

MISTRAL_API_KEY = "dxRJjk2L1x6WPpQWfnWG16gg5lNso6rf"

MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

def generate_ai_response(mode, user_prompt):
    mode_prompts = {
        "mafia": f"Answer like a wise and intimidating mafia boss: {user_prompt}",
        "dadjoke": f"Answer with a classic dad joke style: {user_prompt}",
        "sarcastic": f"Give a highly sarcastic and funny response: {user_prompt}",
        "roast": f"Give a savage roast in response to: {user_prompt}"
    }
    
    ai_prompt = mode_prompts.get(mode, user_prompt)
    
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "mistral-tiny",
        "messages": [{"role": "user", "content": ai_prompt}]
    }
    
    response = requests.post(MISTRAL_API_URL, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    
    return "Oops! The AI fell asleep. Try again later! 😆"

async def ai_response(update: Update, context: CallbackContext):
    if len(context.args) < 2:
        await update.message.reply_text("Use: /ask [mode] [question]. Example: /ask mafia What is the meaning of life?")
        return
    
    mode = context.args[0].lower()
    user_prompt = " ".join(context.args[1:])
    ai_reply = generate_ai_response(mode, user_prompt)
    await update.message.reply_text(ai_reply)

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("ask", ai_response))

    application.run_polling()

if __name__ == "__main__":
    main()
