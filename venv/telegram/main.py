import random
from telegram import InputMediaPhoto, KeyboardButton, PhotoSize, ReplyKeyboardMarkup
import constants as keys
from telegram.ext import MessageHandler, Updater, CommandHandler, Filters, CallbackContext
import responses as r
import db, account, card, util, accountxcard
from telegram.ext.dispatcher import run_async

#, then decorate the function with @run_async
#telegram.constants.DICE_SLOT_MACHINE
buttons = [
        [KeyboardButton("Spin 🎟️"),KeyboardButton("Spin All 🎟️")],
        [KeyboardButton("Free gem 💎"),KeyboardButton("Shop 🛍️"),KeyboardButton("Voices 🎶")],
        [KeyboardButton("Rewards 🎁"),KeyboardButton("Album 📖"),KeyboardButton("VIP ⛔")],
        [KeyboardButton("Profile 🙍‍♂️"),KeyboardButton("Settings ⚙️"),KeyboardButton("Inventory 🎒")]
        ]

#region DB Connection Test
print("Bot started...")
print("DB Stuff")
conn = db.connect('ro')
if conn:
    print("Connection to DB: OK")
    conn.close()
else:
    if not(db.generate()):
        print("Generating DB: Failed")
        exit
    else:
        print("Generating DB: OK")

#endregion

def add_tickets(context: CallbackContext):
    account.add_tickets(10)
    return 1

def start_command(update, context):
    update.message.reply_text('Type something to start')
    update.effective_message.reply_text(
        "start", reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
    )

def help_command(update, context):
    update.message.reply_text('Google is your friend')

def signup_command(update, context):
    signup_id               = update.message.from_user.id
    signup_is_bot           = update.message.from_user.is_bot
    signup_first_name       = update.message.from_user.first_name
    signup_last_name        = update.message.from_user.last_name
    signup_username         = update.message.from_user.username
    signup_language_code    = update.message.from_user.language_code
    #data = [signup_id,signup_is_bot,signup_first_name,signup_last_name,signup_username,signup_language_code]
    if(account.create_account(
        id=signup_id,
        bot=signup_is_bot,
        first_name=signup_first_name,
        last_name=signup_last_name,
        username=signup_username,
        lang=signup_language_code)):
        update.message.reply_text("Account registrato")
    else:
        update.message.reply_text("Account già presente")

def profile_command(update, context):
    pass

def deleteme_command(update, context):
    deleted = account.delete_account(update.message.from_user.id)
    if(deleted):
        update.message.reply_text("Account removed. Hope to see you soon, faggot")
    else:
        update.message.reply_text("Account not registered")

def get_my_cards(update, context):
    user_id = update.message.from_user.id
    data = account.read_account(user_id)
    if(data):
        update.message.reply_text(accountxcard.read_from_account(user_id))

def spin_command(update, context):
    pass

def insert_card_command(update, context):
    card.create(data=['common','cold',str(random()*100),'image.jpg'])
    update.message.reply_text(card.read(1))

def spin_all_command(update, context):
    pass

def handle_message(update, context):
    text = str(update.message.text).lower()
    print(text)
    response = r.sample_responses(update,text)
    print("response",response)
    update.effective_message.reply_text(response,reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True))

def error(update, context):
    print(f"Update {update} caused error {context.error}")

def main():
    updater = Updater(keys.API_KEY, use_context=True)
    #add job queue
    jq = updater.job_queue
    jq.run_repeating(add_tickets,interval=60, first=10)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("signup", signup_command))
    dp.add_handler(CommandHandler("profile", profile_command))
    dp.add_handler(CommandHandler("deleteme", deleteme_command))
    dp.add_handler(CommandHandler("spin", spin_command))
    dp.add_handler(CommandHandler("spinAll", spin_all_command))
    dp.add_handler(CommandHandler("album", get_my_cards))
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling(2)
    updater.idle()

main()
