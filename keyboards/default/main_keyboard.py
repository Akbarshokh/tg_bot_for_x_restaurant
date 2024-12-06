from aiogram.types import  ReplyKeyboardMarkup, KeyboardButton

def phone_keyboard(lang: str):
    """
    Клавиатура для отправки номера телефона с поддержкой разных языков.
    """
    translations = {
        "ru": "📱 Отправить номер телефона",
        "uz": "📱 Telefon raqamini yuboring"
    }

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=translations.get(lang, "Отправить номер телефона"), request_contact=True)]
        ],
        resize_keyboard=True
    )

def get_menu_button(lang: str):
    """
    Клавиатура для главного меню с поддержкой разных языков.
    """
    translations = {
        "ru": {
            "menu": "Меню 📋",
            "orders": "Мои заказы 🛍️",
            "addresses": "Мои адреса 🏠",
            "feedback": "Оставить отзыв 💬",
            "settings": "Настройки ⚙️"
        },
        "uz": {
            "menu": "Menyu 📋",
            "orders": "Buyurtmalarim 🛍️",
            "addresses": "Manzillarim 🏠",
            "feedback": "Fikr qoldirish 💬",
            "settings": "Sozlamalar ⚙️"
        }
    }

    t = translations.get(lang, translations["ru"])

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t["menu"]), KeyboardButton(text=t["orders"])],
            [KeyboardButton(text=t["addresses"]), KeyboardButton(text=t["feedback"])],
            [KeyboardButton(text=t["settings"])]
        ],
        resize_keyboard=True
    )


def help_keyboard(lang: str):
    """
    Клавиатура для помощи с поддержкой разных языков.
    """
    translations = {
        "ru": "Помощь",
        "uz": "Yordam"
    }

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=translations.get(lang, "Помощь"))]
        ],
        resize_keyboard=True
    )


reply_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Option 1"), KeyboardButton(text="Option 2")],
        [KeyboardButton(text="Option 3")],
    ],
    resize_keyboard=True  # Make buttons smaller
)

async def give_menu(menu):
    rows = [menu[i:i + 3] for i in range(0, len(menu), 3)]
    
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for row in rows:
        keyboard.row(*(KeyboardButton(text=btn) for btn in row))
    
    return keyboard