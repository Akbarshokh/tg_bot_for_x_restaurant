from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def language_keyboard():
    """
    Клавиатура для выбора языка.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Русский 🇷🇺", callback_data="ru")],
            [InlineKeyboardButton(text="O‘zbekcha 🇺🇿", callback_data="uz")],
        ]
    )
