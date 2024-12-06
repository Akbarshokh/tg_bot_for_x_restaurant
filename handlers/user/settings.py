from aiogram import  types
from aiogram.fsm.context import FSMContext

from handlers.user.start import router,db, dp
from keyboards.inline.user_inline_keyboards import settings_keyboard, resend_name_or_menu_keyboard, language_keyboard
from keyboards.default.main_keyboard import get_menu_button
from utils.config import answers

# dp.include_router(router)

@router.message(commands=["settings"])
async def show_settings(message: types.Message):
    telegram_id = message.from_user.id
    user_data = db.get_user_data(telegram_id)
    users_name, users_language, users_phone = user_data

    if user_data:
        settings_text = (
            f"{answers[users_language]['settings_title']}\n\n"
            f"{answers[users_language]['name']}: {users_name}\n"
            f"{answers[users_language]['phone']}: {users_phone}\n"
            f"{answers[users_language]['language']}: {users_language}\n\n"
            f"{answers[users_language]['choose_action']}"
        )

        await message.answer(settings_text, reply_markup=settings_keyboard(users_language))
    else:
        await message.answer(
            answers[users_language]["no_user_data"] if users_language in answers else answers["ru"]["no_user_data"]
        )

@router.callback_query(lambda call: call.data == "change_name")
async def change_name(call: types.CallbackQuery, state: FSMContext):
    telegram_id = call.from_user.id
    user_language = db.get_user_lang(telegram_id)

    await call.message.edit_text(
        answers[user_language]["enter_new_name"]
    )
    await state.set_state("change_name")

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@router.message(state="change_name")
async def set_new_name(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    user_language = db.get_user_lang(telegram_id)
    new_name = message.text.strip()

    if 2 <= len(new_name) <= 50:
        db.update_user_name(message.from_user.id, new_name)

        await message.answer(
            answers[user_language]["name_successfully_changed"],
            reply_markup=types.ReplyKeyboardRemove()
        )
        await state.clear()
    else:
        await message.answer(
            answers[user_language]["name_validation"],
            reply_markup=resend_name_or_menu_keyboard(user_language)
        )

@router.callback_query(lambda call: call.data == "retry_name")
async def retry_name(call: types.CallbackQuery, state: FSMContext):
    user_language = db.get_user_lang(call.from_user.id)
    await call.message.edit_text(
        answers[user_language]["set_new_name"]
    )
    await state.set_state("change_name")


@router.callback_query(lambda call: call.data == "change_phone")
async def change_phone(call: types.CallbackQuery, state: FSMContext):
    user_language = db.get_user_lang(call.from_user.id)
    await call.message.edit_text(answers[user_language]["set_new_phone"])
    await state.set_state("change_phone")

@router.message(state="change_phone")
async def set_new_phone(message: types.Message, state: FSMContext):
    user_language = db.get_user_lang(message.from_user.id)

    if message.contact and message.contact.phone_number:
        new_phone = message.contact.phone_number
        db.update_user_phone(message.from_user.id, new_phone)
        await message.answer(
            answers[user_language]["phone_successfully_changed"],
            reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
    else:
        await message.answer(
            answers[user_language]["phone_validation"],
            reply_markup=resend_name_or_menu_keyboard(user_language)
        )

@router.callback_query(lambda call: call.data == "retry_phone")
async def retry_phone(call: types.CallbackQuery, state: FSMContext):
    user_language = db.get_user_lang(call.from_user.id)
    await call.message.edit_text(
        answers[user_language]["set_new_phone"]
    )
    await state.set_state("change_phone")


@router.callback_query(lambda call: call.data == "change_language")
async def change_language(call: types.CallbackQuery):
    await call.message.edit_text("Пожалуйста, выберите язык / Iltimos, tilni tanlang:", reply_markup=language_keyboard())
    await call.message.delete()

@router.callback_query(lambda c: c.data in ["ru", "uz"])
async def set_language(call: types.CallbackQuery):
    lang = call.data
    db.update_user_language(call.from_user.id, lang)
    await call.message.edit_text(answers[lang]["lang_successfully_changed"])

@router.callback_query(lambda call: call.data == "main_menu")
async def main_menu(call: types.CallbackQuery):
    user_language = db.get_user_lang(call.from_user.id)
    await call.message.edit_text(
        answers[user_language]["main_menu_text"],
        reply_markup=get_menu_button(user_language)
    )