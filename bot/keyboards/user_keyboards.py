from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def language_keyboard():
    """
    Клавиатура для выбора языка.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Русский 🇷🇺", callback_data="set_lang:ru")],
            [InlineKeyboardButton(text="O‘zbekcha 🇺🇿", callback_data="set_lang:uz")],
        ]
    )

def phone_keyboard():
    """
    Клавиатура для отправки номера телефона.
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отправить номер телефона", request_contact=True)]
        ],
        resize_keyboard=True
    )
