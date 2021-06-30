from telegram import ReplyKeyboardMarkup, KeyboardButton
from connector import *
from datetime import *
from constants import *
from callbacks.main_menu import *

def request_first_name(update, context):
    update.message.reply_text("What is your first name?")
    return FIRST_NAME


def get_first_name(update, context):
    first_name_spliter = update.effective_message
    print(first_name_spliter)
    a = first_name_spliter.text.split()
    first_name = update.message.text
    if len(a) == 1 and len(first_name) < 20:
        if first_name[0].isupper() and first_name[1:].islower():
            cursor.execute("UPDATE registration SET first_name = '{}' WHERE telegram_id = '{}'".format(first_name, update.message.chat_id))
            connector.commit()
            request_last_name(update, context)
            return LAST_NAME
        else:
             update.message.reply_text("First letter of name must be capitalised and the rest in lower case")
    elif len(a) == 2 and len(first_name) < 20:
        if (a[0][0].isupper() and a[1][0].isupper()) and (a[0][1:].islower() and a[1][1:].islower()):
            cursor.execute("UPDATE registration SET first_name = '{}' WHERE telegram_id = '{}'"
            .format(first_name, update.message.chat_id))
            connector.commit()
            request_last_name(update, context)
            return LAST_NAME
        else:
             update.message.reply_text("First letters of your name must be capitalised and the rest in lower case")
    else:
        update.message.reply_text("Wrong format. Enter only your first name, and make sure it does not exceed 20 characters!")

def request_last_name(update, context):
    update.message.reply_text("What is your last name?")
    return LAST_NAME

def get_last_name(update, context):
    last_name_spliter = update.effective_message
    last_name = update.message.text
    a = last_name_spliter.text.split()
    if len(a) == 1 and len(last_name) < 20:
        if last_name[0].isupper() and last_name[1:].islower():
            request_birthday(update, context)
            cursor.execute("UPDATE registration SET last_name = '{}' WHERE telegram_id = '{}'"
            .format(last_name, update.message.chat_id))
            connector.commit()
            return BIRTHDAY
        else:
            update.message.reply_text("Surname must be capitalised!")
    else:
        update.message.reply_text("Wrong format. Surname can only consist of one word and not exceed 20 characters!")

def request_birthday(update, context):
    current_date = datetime.today().strftime('%Y.%m.%d')
    update.message.reply_text(f"Send your birthday in this format: <b>{current_date}</b>", 
    parse_mode="HTML")
    return BIRTHDAY

def get_birthday(update, context):
    try:
        birthday = update.message.text
        year, month, day = [i for i in birthday.split(".")]
        if len(year) == 4 and len(month) == 2 and len(day) == 2:
            if int(year) <= 2016:
                if  int(year) >= 1940:
                    if int(month) in list(range(1,13)):
                        if int(day) in list(range(1,32)):
                            cursor.execute("UPDATE registration SET birthday = '{}' WHERE telegram_id = '{}'"
                            .format(birthday, update.message.chat_id))
                            connector.commit()
                            cursor.execute("UPDATE registration SET age = CAST(round(strftime(CURRENT_DATE) - strftime(birthday)) as INT)")
                            connector.commit()
                            request_phone(update, context)
                            return PHONE
                        else:
                            update.message.reply_text('Please use proper birth day!')
                    else:
                        update.message.reply_text('Please use proper birth month!')    
                else:
                    update.message.reply_text('Please use proper birth year!')
            else:
                update.message.reply_text('You must be over 5 years old!')
        else:
            update.message.reply_text("Please enter your birthday in the given format!")
    except ValueError:
        update.message.reply_text('Please enter your birthday in the given format!')

def request_phone(update, context):
    buttons = [
        [KeyboardButton('My number', request_contact=True)]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    update.message.reply_text('Now, send me your phone number 📞', reply_markup=reply_markup)
    return PHONE


def get_phone(update, context):
    phone = update.message.contact.phone_number
    phone_as_text = update.message.text
    try:
        if phone_as_text[0:4] == '+998' or phone_as_text[0:3] == '998' or update.message.contact.phone_number:
            if len(phone_as_text) == 13 or len(phone_as_text) == 12:  
                cursor.execute("UPDATE registration SET phone_number = '{}' WHERE telegram_id = '{}'"
                .format(phone or phone_as_text, update.message.chat_id))
                connector.commit()
                update.message.reply_text("Great, now let's see the main menu")
                print(phone)
                main_menu(update, context)
                return MAIN_MENU
            else: 
                update.message.reply_text('NUmber of characters must be 12 or 13')
        else:
            update.message.reply_text('Incorrect country code')
    except ValueError:
        update.message.reply_text("Send your phone number in this format: +998********")
