import telebot

# Telegram Bot token
bot = telebot.TeleBot("6093935724:AAGfNU6wtbJjebBhFGj3HjnI4oy2JDcxxPQ")
# Store Owner chat id
chat_id= "859792093"
# Define a dictionary to hold the inventory items and their prices
our_inventory = {
    "ashirvad atta": 299,
    "patanjali oil": 119,
    "basmati rice": 399,
    "regular rice": 249,
    "arhar dal": 170,
    "maggie": 52,
    "surfexcel": 890,
    "dettol": 40,
    "cocacola": 40,
    "hakka noodles": 85
}

# Define a dictionary to hold the user's cart and their quantities
cart = {}

# Define a handler for the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello, this is Hrs Store's bot. I will help you choose the item of your choice.\nTo view our inventory use: /inventory\nFor any help use: /help")

# Define a handler for /inventory command
@bot.message_handler(commands=['inventory'])
def send_inventory(message):
    bot.reply_to(message,'Welcome to Hrs Store! Here is the list of our inventory items:\n\n'
                 
                '1. Ashirvad Chakki Fresh Atta - 5 kg - ₹299 - 10 remaining\n'
                '2. Patanjali Kacchi Ghani Oil - 1 lit - ₹109 - 25 remaining\n'
                '3. India Gate Basmati Rice - 5 kg - ₹399 - 8 remaining\n'
                '4. India Gate Regular Rice - 5 kg- ₹299 - 3 remaining\n'
                '5. Tata Sampann Toor/Arhar Dal - 1 kg - ₹170 - 15 remaining\n'
                '6. Maggie Noodles Family Pack (280 gm) - ₹52 - 25 remaining\n'
                '7. Surf Excel Detergent (Jasmine & Rose) - 6kg - ₹890 - 7 remaining\n'
                '8. Dettol Antiseptic Liquid - 60 ml - ₹40 - 18 remaining\n'
                '9. CocaCola - 750 ml - ₹40 - 6 remaining\n'
                '10. Chings Hakka Noodles (280gm) - ₹80 - 9 remaining\n\n'
                'We also deliver fresh dairy products on demand (min order value ₹99)\n\n'
                'To order please use: /order'
                )

# Define a handler for the /order command
@bot.message_handler(commands=['order'])
def order(message):
    bot.reply_to(message, "What would you like to order?\n" + "\n".join([item + " - ₹" + str(price) for item, price in our_inventory.items()]) + "\n\nAdd items in your cart.\nWe are trying to improve day-by-day, kindly add one item at a time.\nTo place an order use: /checkout")

# Define a handler for the /help command
@bot.message_handler(commands=['help'])
def order(message):
    bot.reply_to(message, "Here is the list of commands you may use:\n\n"
                 '1. Use /start : To start a new chat\n'
                 '2. Use /inventory : To view items in our inventory\n'
                 '3. Use /order : To add items in your cart\n'
                 '4. Use /checkout : To place your order\n'
                 '5. Use /offers: To know daily offers and discount\n'
                 '5. Use /feedback : To provide your feedback\n\n'
                 'For further help, feel free to contact us at +91-9876543210 or write us at thehrsstore@gmail.com')

# Define a handler for the /offers command
@bot.message_handler(commands=['offers'])
def order(message):
    bot.reply_to(message, "Here is the list of today's offer.\n\n"
                 '1. Get 1kg Toor Dal @49 for orders above ₹699\n'
                 '2. Buy 3 bottles of Soft-drink and get 1 free (200ml)')

# Define a handler for user messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.lower() in our_inventory:
        # Add the item to the user's cart
        if message.text in cart:
            cart[message.text.lower()] += 1
        else:
            cart[message.text.lower()] = 1
        bot.reply_to(message, "Added " + message.text.lower() + " to your cart!")
    elif message.text.lower() == "/checkout":

        # Function to Calculate the total and generate the bill
        total = sum([our_inventory[item] * quantity for item, quantity in cart.items()])
        bill = "Here is your bill:\n\n" + "\n".join([item + " x " + str(quantity) + " - ₹" + str(our_inventory[item] * quantity) for item, quantity in cart.items()]) + "\n\nTotal: ₹" + str(total) + "\n\nWe also offer Cash on Delivery on orders above ₹199\n\nYour feedback is valuable to us, to tell us your experience please use: /feedback\nThankYou!"
        bot.reply_to(message, bill)
        send_order_to_owner(message)
        cart.clear()

    elif message.text.lower() == "/feedback":
        bot.send_message(message.chat.id, "Tell us your experience:")
        # Set the handler function to get the user's feedback
        bot.register_next_step_handler(message, get_user_feedback)
    else:
        bot.reply_to(message, "Sorry, I didn't understand that.")

# Define a function to get user feedback
def get_user_feedback(message):
    feedback = message.text
    # Send feedback message to the admin chat
    bot.send_message(chat_id, f'New feedback from {message.chat.first_name} ({message.chat.username}): \n{feedback}')
    # Send confirmation message to the user
    bot.reply_to(message, 'Thank you for your feedback!')

# Define a function to send a message to the store owner with the order details
def send_order_to_owner(message):
    # Create a message with the order details
    order_details = f"New order received from {message.chat.first_name} ({message.chat.username}) \n\n" + "\n".join([item + " x " + str(quantity) for item, quantity in cart.items()]) + "\n\nTotal: ₹" + str(sum([our_inventory[item] * quantity for item, quantity in cart.items()]))
    # Send the message to the owner
    bot.send_message(chat_id, order_details)
    #send final status to user
    final_status = "Your order has been received and will be delivered soon. Thank you for shopping with us!"
    bot.send_message(message.chat.id, final_status)
# Start the bot
bot.polling()
 