from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def language_keyboard():
    inline_keyboard =[
        [
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="uz")
            ], 
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="ru")
            ]
        ]
    button = InlineKeyboardMarkup(inline_keyboard)
    return button
