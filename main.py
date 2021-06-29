from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, KeyboardButton, replymarkup, update 
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
import logging
import telegram
from  keys import API_TOKEN
from connector import *
from datetime import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
FIRST_NAME, LAST_NAME, PHONE, MAIN_MENU, SETTINGS, ORDERS, PRODUCTS, SUPPORT, CART, MYNAME, MYINFO, CHANGE, \
CONTACT, BIRTHDAY, MYAGE = range(15)

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    result = cursor.execute(
        "SELECT telegram_id, first_name, last_name, user_name from registration WHERE telegram_id = '{}'".format(chat_id)
    ).fetchall()
    print(result)

    if len(result) == 0:
        cursor.execute("INSERT INTO registration(telegram_id, first_name, last_name, user_name) VALUES('{}', '{}', '{}', '{}')"
        .format(chat_id, update.effective_user.first_name, update.effective_user.last_name, update.effective_user.username))
        connector.commit()
        context.bot.send_message(chat_id, text='Hi! My name is Test Bot.', reply_markup=ReplyKeyboardRemove())
        request_first_name(update, context)
        return FIRST_NAME
    else:
        print("user exists")
        main_menu(update, context)
        return MAIN_MENU


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
        if last_name[0].isupper():
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
    birthday = update.message.text
    if birthday == ('%Y.%m.%d'):
        cursor.execute("UPDATE registration SET birthday = '{}' WHERE telegram_id = '{}'"
        .format(birthday, update.message.chat_id))
        connector.commit()
        cursor.execute("UPDATE registration SET age = CAST(round(strftime(CURRENT_DATE) - strftime(birthday)) as INT)")
        connector.commit()
        request_phone(update, context)
        return PHONE
    else:
        update.message.reply_text("Please enter your birthday in the given format!")


def request_phone(update, context):
    buttons = [
        [KeyboardButton('My number', request_contact=True)]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    update.message.reply_text('Now, send me your phone number 📞', reply_markup=reply_markup)
    return PHONE


def get_phone(update, context):
    phone = update.message.contact.phone_number
    cursor.execute("UPDATE registration SET phone_number = '{}' WHERE telegram_id = '{}'"
    .format(phone, update.message.chat_id))
    connector.commit()
    update.message.reply_text("Great, now let's see the main menu")
    print(phone)
    main_menu(update, context)
    return MAIN_MENU


def main_menu(update, context):
    buttons = [
        [KeyboardButton('Order')],
        [KeyboardButton('Settings'), KeyboardButton('Support')],
        [KeyboardButton('My info')]
    ]
    reply_markup1 = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    update.message.reply_text('Main menu: ', reply_markup=reply_markup1)

    return MAIN_MENU


def back_to_main_menu(update, context):
    main_menu(update, context)
    return MAIN_MENU


def orders(update, context):
    buttons = [
        [KeyboardButton('My cart')],
        [KeyboardButton('Back')]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    update.message.reply_text('Orders is opened', reply_markup=reply_markup)
    return ORDERS


def cart(update, context):
    update.message.reply_text('This is what you have ordered so far:',
                              reply_markup=ReplyKeyboardMarkup(
                                  [
                                      ['Back']
                                  ], resize_keyboard=True
                              ))
    return CART


def settings(update, context):
    buttons = [
        [KeyboardButton('Change')],
        [KeyboardButton('Back')]
    ]
    update.message.reply_text('Settings is opened',
                              reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
    return SETTINGS


def support(update, context):
    buttons = [
        [KeyboardButton('Contact')],
        [KeyboardButton('Back')]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    update.message.reply_text('Support is opened', reply_markup=reply_markup)
    return SUPPORT


def contact(update, context):
    update.message.reply_text("This is Javlon's number!")
    context.bot.send_contact(chat_id=update.message.chat_id,
                             phone_number='+998946904113',
                             first_name='Javlon', reply_markup=ReplyKeyboardMarkup(
            [
                ['Back']
            ], resize_keyboard=True
        ))
    return CONTACT


def change(update, context):
    update.message.reply_text('You changed something.',
                              reply_markup=ReplyKeyboardMarkup(
                                  [
                                      ['Back']
                                  ], resize_keyboard=True
                              ))
    return CHANGE


def my_info(update, context):
    buttons = [
        [KeyboardButton('My name')],
        [KeyboardButton('My age')],
        [KeyboardButton('Back')]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    update.message.reply_text('My info is opened', reply_markup=reply_markup)
    return MYINFO


def my_name(update, context):
    full_name = cursor.execute("SELECT first_name, last_name FROM registration WHERE telegram_id='{}'"
    .format(update.effective_chat.id)).fetchall()[0]
    update.message.reply_text(full_name[0] + " " + full_name[1], reply_markup=ReplyKeyboardMarkup(
        [
            ['Back']
        ], resize_keyboard=True
    ))
    connector.commit()
    return MYNAME

def my_age(update, context):
    try:
        age = cursor.execute("SELECT age FROM registration WHERE telegram_id = '{}'".format(update.effective_chat.id)).fetchall()[0][0]
        update.message.reply_text(age, reply_markup = ReplyKeyboardMarkup(
            [
                ['Back']
            ], resize_keyboard=True
        ))
        connector.commit()
        return MYAGE
    except telegram.error.BadRequest:
        update.message.reply_text("You haven't provided your birthday!")


def cancel(update, context):
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main():
    updater = Updater(token=API_TOKEN)
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            FIRST_NAME: [
                MessageHandler(Filters.text, get_first_name)
            ],
            LAST_NAME: [
                MessageHandler(Filters.text, get_last_name)
            ],
            BIRTHDAY: [
                MessageHandler(Filters.text, get_birthday)
            ],
            PHONE: [
                MessageHandler(Filters.contact, get_phone)
            ],
            MAIN_MENU: [
                MessageHandler(Filters.regex('Order'), orders),
                MessageHandler(Filters.regex('Settings'), settings),
                MessageHandler(Filters.regex('Support'), support),
                MessageHandler(Filters.regex('My info'), my_info)
            ],
            SETTINGS: [
                MessageHandler(Filters.regex('Change'), change),
                MessageHandler(Filters.regex('Back'), back_to_main_menu)
            ],
            ORDERS: [
                MessageHandler(Filters.regex('My cart'), cart),
                MessageHandler(Filters.regex('Back'), back_to_main_menu)
            ],
            CART: [
                MessageHandler(Filters.regex('Back'), orders)
            ],
            MYINFO: [
                MessageHandler(Filters.regex('My name'), my_name),
                MessageHandler(Filters.regex('My age'), my_age),
                MessageHandler(Filters.regex('Back'), back_to_main_menu)
            ],

            MYNAME: [
                MessageHandler(Filters.regex('Back'), my_info)
            ],

            MYAGE: [
                MessageHandler(Filters.regex('Back'), my_info)
            ],
            CHANGE: [
                MessageHandler(Filters.regex('Back'), settings)
            ],
            SUPPORT: [
                MessageHandler(Filters.regex('Contact'), contact),
                MessageHandler(Filters.regex('Back'), back_to_main_menu)
            ],
            CONTACT: [
                MessageHandler(Filters.regex('Back'), support)
            ]

        },
        fallbacks=[]
    )
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

