from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

def main_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row(KeyboardButton("🌐 Translate"), KeyboardButton("💬 Review"))
    keyboard.add("ℹ️ Help")
    return keyboard

def phone_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton('Share phone number📱', request_contact=True))
    return keyboard

def cancel_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton("❌Cancel"))
    return keyboard


def remove_keyboard():
    keyboard = ReplyKeyboardRemove()
    return keyboard