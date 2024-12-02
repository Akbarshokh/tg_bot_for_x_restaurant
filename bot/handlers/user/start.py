from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from bot.states.user import Registration
from bot.services.database import save_user
from bot.services.sms import send_sms

router = Router()

# Переводы сообщений
translations = {
    "choose_language": {
        "ru": "Выберите язык:",
        "uz": "Tilni tanlang:"
    },
    "enter_name": {
        "ru": "Введите ваше имя:",
        "uz": "Ismingizni kiriting:"
    },
    "enter_phone": {
        "ru": "Отправьте ваш номер телефона:",
        "uz": "Telefon raqamingizni yuboring:"
    },
    "verify_code": {
        "ru": "Мы отправили вам код подтверждения. Введите его:",
        "uz": "Tasdiqlash kodini yubordik. Uni kiriting:"
    },
    "registration_complete": {
        "ru": "Регистрация завершена! Добро пожаловать!",
        "uz": "Ro'yxatdan o'tish tugallandi! Xush kelibsiz!"
    }
}

def get_translation(key, language):
    return translations.get(key, {}).get(language, key)

# Начало регистрации - выбор языка
@router.message(F.text == "/start", state=default_state)
async def start_registration(message: Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Русский", callback_data="lang_ru"),
             InlineKeyboardButton(text="O‘zbek", callback_data="lang_uz")]
        ]
    )
    await message.answer("Выберите язык / Tilni tanlang:", reply_markup=keyboard)
    await state.set_state(Registration.language)

# Обработка выбора языка
@router.callback_query(Registration.language)
async def set_language(callback_query, state: FSMContext):
    language = callback_query.data.split("_")[1]  # Получаем "ru" или "uz"
    await state.update_data(language=language)
    await callback_query.message.answer(get_translation("enter_name", language))
    await state.set_state(Registration.name)

# Ввод имени
@router.message(Registration.name)
async def enter_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if len(name) < 2 or len(name) > 50:
        language = (await state.get_data()).get("language", "ru")
        await message.answer(get_translation("enter_name", language))
        return

    await state.update_data(name=name)
    language = (await state.get_data()).get("language", "ru")
    await message.answer(get_translation("enter_phone", language))
    await state.set_state(Registration.phone)

# Ввод номера телефона
@router.message(Registration.phone, F.contact)
async def enter_phone(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    await state.update_data(phone=phone)

    # Отправка SMS
    otp_code = await send_sms(phone)
    if not otp_code:
        await message.answer("Не удалось отправить SMS. Попробуйте снова позже.")
        return

    await state.update_data(otp=otp_code)
    language = (await state.get_data()).get("language", "ru")
    await message.answer(get_translation("verify_code", language))
    await state.set_state(Registration.confirmation)

# Подтверждение телефона
@router.message(Registration.confirmation)
async def verify_phone(message: Message, state: FSMContext):
    user_otp = message.text.strip()
    data = await state.get_data()

    if user_otp != data["otp"]:
        language = data.get("language", "ru")
        await message.answer(get_translation("verify_code", language))
        return

    # Сохраняем пользователя в базу данных
    await save_user(
        telegram_id=message.from_user.id,
        name=data["name"],
        phone=data["phone"],
        language=data["language"]
    )
    await state.clear()

    language = data["language"]
    await message.answer(get_translation("registration_complete", language))
