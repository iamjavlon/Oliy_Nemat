from constants import MAIN_MENU
from telegram import ReplyKeyboardMarkup, KeyboardButton
def main_menu(update, context):
    buttons = [
        [KeyboardButton('Order')],
        [KeyboardButton('Settings'), KeyboardButton('Support')],
        [KeyboardButton('My info')]
    ]
    reply_markup1 = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    update.message.reply_text('Main menu: ', reply_markup=reply_markup1)

    return MAIN_MENU
