import telegram
from telegram.ext import Updater, CommandHandler
from products import products

# Define the /start command handler
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to LocalShopBot! Type /products to see the list of available products.")

# Define the /products command handler
def products_command(update, context):
    message = "Here are the available products:\n\n"
    for name, data in products.items():
        price = data['price']
        description = data['description']
        message += f"{name}: ${price:.2f}\n{description}\n\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# Set up the Telegram bot
TOKEN = '5704204348:AAExAGZhx-sdgCcTVnkOtXXfdUC7kvL10aQ'
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('products', products_command))

# Start the bot
updater.start_polling()