import random
from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from states.user import Registration
from utils.db import PgConn
from datetime import datetime, timedelta
from sqlalchemy import text
from aiogram.filters import CommandStart
from keyboards.default.main_keyboard import phone_keyboard
from keyboards.inline.user_inline_keyboards import language_keyboard

from loader import dp
router = Router()
dp.include_router(router)
db = PgConn()

@router.message(CommandStart())
async def start_registration(message: types.Message):
    await message.answer("Пожалуйста, выберите язык / Iltimos, tilni tanlang:", reply_markup=language_keyboard())

@router.callback_query(lambda c: c.data in ["ru", "uz"])
async def set_language(call : types.CallbackQuery, state: FSMContext):
    lang = call.data
    await state.update_data(language=lang)
    await call.message.answer("Введите ваше имя / Ismingizni kiriting:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Registration.name)
    await call.message.delete()

@router.message(Registration.name)
async def set_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    if 2 <= len(name) <= 50:
        await state.update_data(name=name)
        keyboard = phone_keyboard()
        await message.answer("Пожалуйста, отправьте ваш номер телефона:", reply_markup=keyboard)
        await state.set_state(Registration.phone)
    else:
        await message.answer("Имя должно содержать от 2 до 50 символов. Попробуйте снова.")

@router.message(Registration.phone)
async def set_phone(message: types.Message, state: FSMContext):
    if message.contact and message.contact.phone_number:
        phone = message.contact.phone_number
        otp = str(random.randint(100000, 999999))
        expires_at = datetime.now() + timedelta(minutes=5)

        # код--временно
        print(otp)

        # Сохраняем SMS-код в базе данных
        success = db.generate_otp(phone, otp, expires_at)

        if success:
            await state.update_data(phone=phone)
            await message.answer(f"Мы отправили SMS с кодом на номер {phone}. Введите код:")
            await state.set_state(Registration.confirmation)
        else:
            await message.answer("Произошла ошибка при отправке SMS.")
    else:
        await message.answer("Пожалуйста, отправьте корректный номер телефона.")

@router.message(Registration.confirmation)
async def verify_code(message: types.Message, state: FSMContext):
    phone = (await state.get_data()).get("phone")
    entered_code = message.text

    # Checking code from DB
    otp_record = db.get_otp_by_phone(phone)

    if otp_record:
        db_otp, expires_at, is_verified = otp_record

        if is_verified:
            await message.answer("Этот код уже был использован.")
        elif datetime.now() > expires_at:
            await message.answer("Срок действия кода истёк. Попробуйте заново.")
        elif db_otp == entered_code:
            success_otp = db.verify_otp(phone, entered_code)

            if success_otp:
                user_data = {
                    "telegram_id": message.from_user.id,
                    "phone": phone,
                    "name": (await state.get_data()).get("name"),
                    "language": (await state.get_data()).get("language")
                }

                # Saving user data into DB
                success_user_save = db.save_user(user_data)
                if success_user_save == "inserted":
                    await message.answer("Регистрация успешно завершена! Добро пожаловать!")
                    await state.clear()
                elif success_user_save == "updated":
                    await message.answer("Регистрация успешно завершена! Добро пожаловать!")
                    await state.clear()
                elif success_user_save == "already_registered":
                    await message.answer("Регистрация успешно завершена! Добро пожаловать!")
                    await state.clear()
                elif isinstance(success_user_save, tuple) and success_user_save[0] =="error":
                    await message.answer("Что-то пошло не так 🥴")
        else:
            await message.answer("Неверный код. Попробуйте снова.")
    else:
        await message.answer("Код не найден. Попробуйте ещё раз или запросите новый.")


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
