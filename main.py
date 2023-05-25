import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from products import products

# Define the /start command handler
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to LocalShopBot! Type /help to see the list of available commands.")

# Define the /help command handler
def help_command(update, context):
    message = "Here are the available commands:\n\n"
    message += "/start - Start the bot and see the welcome message.\n"
    message += "/help - See the list of available commands.\n"
    message += "/products - See the list of available products.\n"
    message += "/cart - View your current cart.\n"
    message += "/add - Add a product to your cart. Type the name of the product and the quantity, separated by a space.\n"
    message += "/remove - Remove a product from your cart. Type the name of the product and the quantity, separated by a space.\n"
    message += "/clear - Clear your cart.\n"
    message += "/confirm - Confirm your order and see the total cost.\n"
    message += "/accept - Accept your order and place the order with the store owner.\n"
    message += "/decline - Decline your order and cancel the order.\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# Define the /look command handler
def look_command(update, context):
    message_text = update.message.text
    product_name = message_text.split(' ')[1]
    if product_name in products:
        product = products[product_name]
        message = f"{product_name}\nPrice: {product['price']:.2f}\nRemaining Qty: {product['remaining_qty']}\nWeight: {product['weight']}\nType: {product['type']}\nBrand: {product['brand']}\nDescription: {product['description']}"
    else:
        message = "That product is not available."
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# Define the /review command handler
def review_command(update, context):
    message = "Please fill out the review form:\n\nhttps://docs.google.com/forms/d/e/1FAIpQLSem_UiisiFp2RDq5bbT0oqpCoj28_nf35Cuu-VraPMjLGI7wg/viewform?usp=sf_link"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# Define the /products command handler
def products_command(update, context):
    message = "Here are the available products:\n\n"
    for name, data in products.items():
        price = data['price']
        remaining_qty = data['remaining_qty']
        weight = data['weight']
        product_type = data['type']
        brand = data['brand']
        description = data['description']
        message += f"{name}\nPrice: {price:.2f}\nRemaining Qty: {remaining_qty}\nWeight: {weight}\nType: {product_type}\nBrand: {brand}\nDescription: {description}\n\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# Define the /order command handler
def order_command(update, context):
    message = "To order a product, type the name of the product and the quantity, separated by a space. For example:\n\nToothpaste 2\n\nType /confirm to see the total cost and confirm your order."
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# Define the /cart command handler
def cart_command(update, context):
    user_id = update.effective_chat.id
    cart = context.user_data.get('cart', {})
    if not cart:
        context.bot.send_message(chat_id=user_id, text="Your cart is empty.")
        return
    message = "Your cart:\n\n"
    total_cost = 0
    for name, data in cart.items():
        price = data['price']
        qty = data['qty']
        cost = price * qty
        total_cost += cost
        message += f"{name} x {qty} - {price:.2f} each - Total: {cost:.2f}\n"
    message += f"\nTotal cost: {total_cost:.2f}.\n\nType /confirm to confirm your order, or /clear to clear your cart."
    context.bot.send_message(chat_id=user_id, text=message)

# Define the /add command handler
def add_command(update, context):
    user_id = update.effective_chat.id
    message = "To add a product to your cart, type the name of the product and the quantity, separated by a space. For example:\n\nToothpaste 2"
    context.user_data['add_mode'] = True
    context.bot.send_message(chat_id=user_id, text=message)

# Define the /remove command handler
def remove_command(update, context):
    user_id = update.effective_chat.id
    message = "To remove a product from your cart, type the name of the product and the quantity, separated by a space. For example:\n\nToothpaste 2"
    context.user_data['remove_mode'] = True
    context.bot.send_message(chat_id=user_id, text=message)

# Define the /clear command handler
def clear_command(update, context):
    user_id = update.effective_chat.id
    context.user_data['cart'] = {}
    context.bot.send_message(chat_id=user_id, text="Your cart has been cleared.")

# Define the /confirm command handler
def confirm_command(update, context):
    user_id = update.effective_chat.id
    cart = context.user_data.get('cart', {})
    if not cart:
        context.bot.send_message(chat_id=user_id, text="Your cart is empty.")
        return
    message = "Your order:\n\n"
    total_cost = 0
    for name, data in cart.items():
        price = data['price']
        qty = data['qty']
        cost = price * qty
        total_cost += cost
        message += f"{name} x {qty} - {price:.2f} each - Total: {cost:.2f}\n"
    message += f"\nTotal cost: {total_cost:.2f}.\n\nType /accept to accept the order, or /decline to cancel the order."
    context.user_data['total_cost'] = total_cost
    context.bot.send_message(chat_id=user_id, text=message)

# Define the /accept command handler
def accept_command(update, context):
    user_id = update.effective_chat.id
    total_cost = context.user_data.get('total_cost')
    if not total_cost:
        context.bot.send_message(chat_id=user_id, text="You have not confirmed your order yet.")
        return
    context.user_data['cart'] = {}
    context.user_data['total_cost'] = None
    context.bot.send_message(chat_id=user_id, text="Your order has been placed with the store owner. Thank you for shopping with us!")

# Define the /decline command handler
def decline_command(update, context):
    user_id = update.effective_chat.id
    context.user_data['total_cost'] = None
    context.bot.send_message(chat_id=user_id, text="Your order has been cancelled. Type /order to start a new order.")

# Define the /rate command handler
def rate_command(update, context):
    user_id = update.effective_chat.id
    message = "Rate the store on a scale of 1-5. For example:\n\n3"
    context.user_data['rate_mode'] = True
    context.bot.send_message(chat_id=user_id, text=message)

# Define the /points command handler
def points_command(update, context):
    user_id = update.effective_chat.id
    points = context.user_data.get('points', 0)
    message = f"You have {points} loyalty points."
    context.bot.send_message(chat_id=user_id, text=message)

# Define the message handler
def message_handler(update, context):
    user_id = update.effective_chat.id
    message_text = update.message.text
    cart = context.user_data.get('cart', {})
    if context.user_data.get('add_mode'):
        try:
            name, qty = message_text.split(' ')
            qty = int(qty)
            if name in products:
                if qty <= 0:
                    context.bot.send_message(chat_id=user_id, text="The quantity must be a positive number.")
                elif qty > products[name]['remaining_qty']:
                    context.bot.send_message(chat_id=user_id, text="There is not enough stock of that product.")
                else:
                    if name in cart:
                        cart[name]['qty'] += qty
                    else:
                        cart[name] = {'price': products[name]['price'], 'qty': qty}
                    products[name]['remaining_qty'] -= qty
                    context.user_data['cart'] = cart
                    context.bot.send_message(chat_id=user_id, text=f"{qty} {name}(s) have been added to your cart.")
            else:
                context.bot.send_message(chat_id=user_id, text="That product is not available.")
        except ValueError:
            context.bot.send_message(chat_id=user_id, text="Please enter the name of the product and the quantity, separated by a space.")
        context.user_data['add_mode'] = False
    elif context.user_data.get('remove_mode'):
        try:
            name, qty = message_text.split(' ')
            qty = int(qty)
            if name in cart:
                if qty <= 0:
                    context.bot.send_message(chat_id=user_id, text="The quantity must be a positive number.")
                elif qty > cart[name]['qty']:
                    context.bot.send_message(chat_id=user_id, text="There are not that many items of that product in your cart.")
                else:
                    cart[name]['qty'] -= qty
                    if cart[name]['qty'] == 0:
                        del cart[name]
                    products[name]['remaining_qty'] += qty
                    context.user_data['cart'] = cart
                    context.bot.send_message(chat_id=user_id, text=f"{qty} {name}(s) have been removed from your cart.")
            else:
                context.bot.send_message(chat_id=user_id, text="That product is not in your cart.")
        except ValueError:
            context.bot.send_message(chat_id=user_id, text="Invalid rating. Please rate the store on a scale of 1-5.")
            context.user_data['rate_mode'] = False
    else:
        context.bot.send_message(chat_id=user_id, text="Invalid command. Type /help to see the list of available commands.")

# Create the updater and dispatcher
updater = Updater(token='5704204348:AAExAGZhx-sdgCcTVnkOtXXfdUC7kvL10aQ', use_context=True)
dispatcher = updater.dispatcher

# Add the handlers to the dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help_command))
dispatcher.add_handler(CommandHandler('products', products_command))
dispatcher.add_handler(CommandHandler('order', order_command))
dispatcher.add_handler(CommandHandler('cart', cart_command))
dispatcher.add_handler(CommandHandler('add', add_command))
dispatcher.add_handler(CommandHandler('remove', remove_command))
dispatcher.add_handler(CommandHandler('clear', clear_command))
dispatcher.add_handler(CommandHandler('confirm', confirm_command))
dispatcher.add_handler(CommandHandler('accept', accept_command))
dispatcher.add_handler(CommandHandler('decline', decline_command))
dispatcher.add_handler(CommandHandler('rate', rate_command))
dispatcher.add_handler(CommandHandler('points', points_command))
dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
dispatcher.add_handler(CommandHandler('look', look_command))
dispatcher.add_handler(CommandHandler('review', review_command))

# Start the bot
updater.start_polling()                                    