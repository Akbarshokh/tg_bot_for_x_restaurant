import random
from aiogram import Router, types
from aiogram.types import  ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from states.user import Registration
from utils.db import PgConn
from datetime import datetime, timedelta
from sqlalchemy import text
from aiogram.filters import CommandStart

from loader import dp
router = Router()
dp.include_router(router)
db = PgConn()

@router.message(CommandStart())
async def start_registration(message: types.Message):
    kb_list = [
        [KeyboardButton(text="🇷🇺 Русский")],
        [KeyboardButton(text="🇺🇿 O'zbekcha")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    await message.answer("Пожалуйста, выберите язык / Iltimos, tilni tanlang:", reply_markup=keyboard)
    # await state.set_state(Registration.language)

@router.message(Registration.language)


async def set_language(message: types.Message, state: FSMContext):
    lang = "ru" if message.text == "Русский" else "uz"
    await state.update_data(language=lang)
    await message.answer("Введите ваше имя / Ismingizni kiriting:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Registration.name)

@router.message(Registration.name)
async def set_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    if 2 <= len(name) <= 50:
        await state.update_data(name=name)
        kb_list =[
           [KeyboardButton(text="📱 Отправить номер телефона", request_contact=True, one_time_keyboard=True)]
        ]
        keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)
        await message.answer("Пожалуйста, отправьте ваш номер телефона:", reply_markup=keyboard)
        await state.set_state(Registration.phone)
    else:
        await message.answer("Имя должно содержать от 2 до 50 символов. Попробуйте снова.")

# @router.message(content_types=types.ContentType.CONTACT, state=Registration.phone)
@router.message(Registration.phone)
async def set_phone(message: types.Message, state: FSMContext):
    if message.contact and message.contact.phone_number:
        phone = message.contact.phone_number
        otp = str(random.randint(100000, 999999))
        expires_at = datetime.now() + timedelta(minutes=5)

        # код--временно
        print(otp)

        # Сохраняем SMS-код в базе данных
        db.conn.execute(
            text("INSERT INTO sms_verifications (phone, otp, expires_at) VALUES (:phone, :otp, :expires_at)"),
            {"phone": phone, "otp": otp, "expires_at": expires_at}
        )

        await state.update_data(phone=phone, otp=otp)
        await message.answer(f"Мы отправили SMS с кодом на номер {phone}. Введите код:")
        await state.set_state(Registration.phone)
    else:
        await message.answer("Пожалуйста, отправьте корректный номер телефона.")

@router.message(Registration.phone)
async def verify_code(message: types.Message, state: FSMContext):
    data = await state.get_data()
    otp = data.get('otp')

    if message.text == otp:
        user_data = {
            "telegram_id": message.from_user.id,
            "name": data['name'],
            "phone": data['phone'],
            "language": data['language']
        }

        # Сохранение пользователя в базу данных
        db.conn.execute(
            text("INSERT INTO users (telegram_id, name, phone, language) VALUES (:telegram_id, :name, :phone, :language)"),
            user_data
        )

        await message.answer("Регистрация успешно завершена! Добро пожаловать!")
        await state.clear()
    else:
        await message.answer("Неверный код. Попробуйте снова.")


@router.message(lambda message: message.text.lower() in ["повторить код", "повторная отправка"])
async def resend_code(message: types.Message, state: FSMContext):
    data = await state.get_data()
    phone = data.get('phone')
    otp = str(random.randint(100000, 999999))
    expires_at = datetime.now() + timedelta(minutes=5)

    # Обновляем код в базе данных
    db.conn.execute(
        text("UPDATE sms_verifications SET otp=:otp, expires_at=:expires_at WHERE phone=:phone"),
        {"otp": otp, "expires_at": expires_at, "phone": phone}
    )

    await message.answer(f"Новый код отправлен на номер {phone}. Проверьте SMS.")
