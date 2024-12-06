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

def resend_otp_keyboard(lang: str, active: bool = True):
    translations = {
        "ru": {
            "resend_otp": "Отправить код повторно.",
            "inactive": "Повторная отправка недоступна."
        },
        "uz": {
            "resend_otp": "Kodni qayta yuborish.",
            "inactive": "Qayta yuborish imkoniyati yo'q."
        }
    }

    t = translations.get(lang, translations["ru"])

    if active:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=t["resend_otp"], callback_data="resend_otp")],
            ]
        )
    else:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=t["inactive"], callback_data="disabled", disabled=True)],
            ]
        )


def settings_keyboard(lang: str):
    translations = {
        "ru": {
            "change_name": "Имя",
            "change_phone": "Телефон",
            "change_language": "Язык",
            "main_menu": "Главное меню"
        },
        "uz": {
            "change_name": "Ism",
            "change_phone": "Telefon",
            "change_language": "Muloqot tili",
            "main_menu": "⬅️ Asosiy menu"
        }
    }
    t = translations.get(lang, translations["ru"])

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t["change_name"], callback_data="change_name")],
            [InlineKeyboardButton(text=t["change_phone"], callback_data="change_phone")],
            [InlineKeyboardButton(text=t["change_language"], callback_data="change_language")],
            [InlineKeyboardButton(text=t["main_menu"], callback_data="main_menu")],
        ]
    )

def resend_name_or_menu_keyboard(lang: str):
    translations = {
        "ru": {
            "retry_name": "Попробовать снова",
            "main_menu": "Главное меню",
        },
        "uz": {
            "retry_name": "Qayta urinib ko'rish",
            "main_menu": "Bosh menyu",
        }
    }

    t = translations.get(lang, translations["ru"])

    return  InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t["retry_name"], callback_data="retry_name")],
            [InlineKeyboardButton(text=t["main_menu"], callback_data="main_menu")],
        ]
    )

def resend_phone_or_menu_keyboard(lang: str):
    translations = {
        "ru": {
            "retry_phone": "Попробовать снова",
            "main_menu": "Главное меню",
        },
        "uz": {
            "retry_phone": "Qayta urinib ko'rish",
            "main_menu": "Bosh menyu",
        }
    }

    t = translations.get(lang, translations["ru"])

    return  InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t["retry_phone"], callback_data="retry_phone")],
            [InlineKeyboardButton(text=t["main_menu"], callback_data="main_menu")],
        ]
    )