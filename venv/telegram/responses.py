from time import sleep
from telegram import InputMediaPhoto, KeyboardButton, KeyboardButton, PhotoSize, ReplyKeyboardMarkup
import account, card, util, accountxcard
import random

buttons = [
        [KeyboardButton("Spin 🎟️"),KeyboardButton("Spin All 🎟️")],
        [KeyboardButton("Free gem 💎"),KeyboardButton("Shop 🛍️"),KeyboardButton("Voices 🎶")],
        [KeyboardButton("Rewards 🎁"),KeyboardButton("Album 📖"),KeyboardButton("VIP ⛔")],
        [KeyboardButton("Profile 🙍‍♂️"),KeyboardButton("Settings ⚙️"),KeyboardButton("Inventory 🎒")]
        ]

reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True)

def sample_responses(update,input_text):
    user_id = update.message.from_user.id
    user_message = str(input_text).lower()
    
    if user_message in ("spin 🎟️"):
        print("start response")
        if not(account.exist_account(user_id)):
            update.message.reply_text("Please register your account first. Use /signup to signup")
            print("account non presente")
            return -1
        #roll the emoji
        msg = update.message.reply_dice(emoji='🎰')
        account.add_ticket(user_id,-1)
        print("response: emoji")
        #define the card
        id_found = util.generate_card_id(msg.dice.value)
        if not(id_found):
            sleep(1.5)
            #put keyboard
            update.effective_message.reply_text(
            "No card found, retry", reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True))
        else:
            #add card to the account
            accountxcard.create(id_found,user_id)
            #TODO resize image before sending
            #mostrare carta
            path = card.read_full_path(id_found)
            name = card.read_name(id_found)
            file = open(path, 'rb')
            sleep(1.5)
            update.message.reply_photo(file,path[:2] + " " + name)
            #add card to account accountxcard
            #put keyboard
            update.effective_message.reply_text(
                "Lucky!\n", reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True))
        
        return f"Tickets remaining: {account.read_ticket(user_id)}"

    if user_message in ("spin all 🎟️"):
        print("start response")
        spin_to_make = 100
        if not(account.exist_account(user_id)):
            update.message.reply_text("Please register your account first. Use /signup to signup")
            print("account non presente")
            return -1
        
        #array con le immagini
        input_media_array = []
        #array con i nomi delle immagini
        input_media_name_array = []
        #stringa da far vedere all'utente
        drop_string = ""

        account.add_ticket(user_id,-1*spin_to_make)

        for i in range (spin_to_make):
            msg = random.randint(1,64)
            print("response: emoji")

            id_found = util.generate_card_id(msg)
            
            if not(id_found):
                continue
            else:
                accountxcard.create(id_found,user_id)
                path = card.read_full_path(id_found)
                print(path)
                name = card.read_name(id_found)
                file = open(path, 'rb')
                file_name = path[:2] + " " + name
                
                input_media = InputMediaPhoto(file, file_name)
                if file_name not in input_media_name_array:
                    input_media_name_array.append(file_name)
                    input_media_array.append(input_media)
                    drop_string += f"{file_name}\n"

        if(input_media_array):
            update.effective_message.reply_media_group(input_media_array)
        update.effective_message.reply_text(
            drop_string, reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True))
        
        return f"Tickets remaining: {account.read_ticket(user_id)}"

    if user_message in ("album 📖"):
        
        print("start response")
        if not(account.exist_account(user_id)):
            update.message.reply_text("Please register your account first. Use /signup to signup")
            return -1
        else:
            print("else response")
            #TODO get list of cards owned
            owned_cards_amount = card.count()
            album = f"You have {owned_cards_amount} cards\n"
            owned_cards = accountxcard.read_all_id(user_id)
            print("card count", owned_cards_amount, owned_cards)
            for i in range(1,card.count()):
                if i in owned_cards:
                    album += f"n{str(i)}) {card.read_name(i)} Lv {accountxcard.read_amount(user_id,i)}\n"
                    continue
                album += f"n{str(i)}) ?\n"
            
        return album

    if user_message in ("profile 🙍‍♂️"):
        data = account.read_account(update.message.from_user.id)
        if(data):
            return data
        else:
            return "Account not registered"
    
    return "wat?"