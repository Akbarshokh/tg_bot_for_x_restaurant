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
