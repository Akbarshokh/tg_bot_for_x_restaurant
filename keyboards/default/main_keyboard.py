from aiogram.types import  ReplyKeyboardMarkup, KeyboardButton


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