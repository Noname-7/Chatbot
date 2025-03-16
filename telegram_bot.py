from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# OpenAI client
client = OpenAI(
    base_url="https://api.aimlapi.com/v1",
    api_key="7acbc4aebf1e4d8eb8bfb61ae0c44e82",  # Replace with your actual API key
)

# Chatbot name
chatbot_name = "Luna"  # You can use any name you like (e.g., Luna, Chandra, etc.)

# Function to handle chatbot logic
def chatbot_response(user_input):
    # Check if the user is asking for the chatbot's name
    if "your name" in user_input.lower() or "who are you" in user_input.lower():
        return f"My name is {chatbot_name}!"

    # Check if the user is asking who created the chatbot
    if "who made you" in user_input.lower() or "who created you" in user_input.lower():
        return "I was created by a developer named Ajay!"

    # Send the user's input to OpenAI
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"You are an AI assistant named {chatbot_name}."},
            {"role": "user", "content": user_input},
        ],
    )
    return response.choices[0].message.content

# Command handler for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Hello! I am {chatbot_name}, your AI assistant. How can I help you today?")

# Message handler for regular messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text  # Get the user's message
    bot_response = chatbot_response(user_input)  # Get the chatbot's response
    await update.message.reply_text(bot_response)  # Send the response back to the user

# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

# Main function to start the bot
if __name__ == "__main__":
    # Replace 'YOUR_TELEGRAM_BOT_TOKEN' with the token you got from BotFather
    app = Application.builder().token("7415577983:AAFHxmGkvRdHCIQOxXGqJ_169ydAQqelino").build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_error_handler(error)

    # Start the bot
    print("Bot is running...")
    app.run_polling()