from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from handlers.user.start import db
from keyboards.inline.user_inline_keyboards import settings_keyboard, resend_name_or_menu_keyboard, language_keyboard, \
    language_change_keyboard
from keyboards.default.main_keyboard import get_menu_button, phone_keyboard
from utils.config import answers
from aiogram.filters.command import Command
from states.user import Settings

settings_router = Router()

@settings_router.message(Command(commands=["settings"]))
@settings_router.message(F.text.in_({"Настройки ⚙️", "Sozlamalar ⚙️"}))
async def show_settings(message: types.Message):
    telegram_id = message.from_user.id
    user_data = db.get_user_data(telegram_id)
    db_user_id, users_name, users_language, users_phone = user_data

    if user_data:
        settings_text = (
            f"{answers[users_language]['settings_title']}\n\n"
            f"{answers[users_language]['name']}: {users_name}\n"
            f"{answers[users_language]['phone']}: {users_phone}\n"
            f"{answers[users_language]['language']}: {users_language}\n\n"
        )

        await message.answer(
            settings_text,
            reply_markup=types.ReplyKeyboardRemove()
        )

        await message.answer(
            text=answers[users_language]['choose_action'],
            reply_markup=settings_keyboard(users_language)
        )
    else:
        await message.answer(
            answers[users_language]["no_user_data"] if users_language in answers else answers["ru"]["no_user_data"],
            reply_markup=types.ReplyKeyboardRemove()
        )

@settings_router.callback_query(lambda call: call.data == "change_name")
async def change_name(call: types.CallbackQuery, state: FSMContext):
    telegram_id = call.from_user.id
    user_language = db.get_user_lang(telegram_id)

    await call.message.answer(
        text=answers[user_language[0]]["set_new_name"],
        reply_markup=None,
    )
    await state.set_state(Settings.change_name)
    await call.message.delete()


@settings_router.message(Settings.change_name)
async def set_new_name(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    user_language = db.get_user_lang(telegram_id)
    new_name = message.text.strip()

    if 2 <= len(new_name) <= 50:
        db.update_user_name(message.from_user.id, new_name)

        await message.answer(
            answers[user_language[0]]["name_successfully_changed"],
            reply_markup=get_menu_button(user_language[0]),
        )
        await state.clear()
    else:
        await message.answer(
            answers[user_language]["name_validation"],
            reply_markup=resend_name_or_menu_keyboard(user_language)
        )

@settings_router.callback_query(lambda call: call.data == "retry_name")
async def retry_name(call: types.CallbackQuery, state: FSMContext):
    user_language = db.get_user_lang(call.from_user.id)
    await call.message.answer(
        answers[user_language[0]]["set_new_name"]
    )
    await state.set_state(Settings.change_name)


@settings_router.callback_query(lambda call: call.data == "change_phone")
async def change_phone(call: types.CallbackQuery, state: FSMContext):
    user_language = db.get_user_lang(call.from_user.id)
    await call.message.answer(
        text=answers[user_language[0]]["set_new_phone"],
        reply_markup=phone_keyboard(user_language[0]))

    await state.set_state(Settings.change_phone)
    await call.message.delete()

@settings_router.message(Settings.change_phone)
async def set_new_phone(message: types.Message, state: FSMContext):
    user_language = db.get_user_lang(message.from_user.id)

    if message.contact and message.contact.phone_number:
        new_phone = message.contact.phone_number
        db.update_user_phone(message.from_user.id, new_phone)

        await message.answer(
            answers[user_language[0]]["phone_successfully_changed"],
            reply_markup=get_menu_button(user_language[0]),)
        await state.clear()
    else:
        await message.answer(
            answers[user_language[0]]["phone_validation"],
            reply_markup=resend_name_or_menu_keyboard(user_language)
        )

@settings_router.callback_query(lambda call: call.data == "retry_phone")
async def retry_phone(call: types.CallbackQuery, state: FSMContext):
    user_language = db.get_user_lang(call.from_user.id)
    await call.message.edit_text(
        answers[user_language[0]]["set_new_phone"]
    )
    await state.set_state(Settings.change_phone)


@settings_router.callback_query(lambda call: call.data == "change_language")
async def change_language(call: types.CallbackQuery):
    await call.message.answer(
        "Пожалуйста, выберите язык / Iltimos, tilni tanlang:",
        reply_markup=language_change_keyboard())
    await call.message.delete()


@settings_router.callback_query(lambda c: c.data in ["change_ru", "change_uz"])
async def set_language(call: types.CallbackQuery):
    lang_mapping = {"change_ru": "ru", "change_uz": "uz"}
    lang = lang_mapping[call.data]
    db.update_user_language(call.from_user.id, lang)

    await call.message.answer(
        answers[lang]["lang_successfully_changed"],
        reply_markup=get_menu_button(lang),
    )
    await call.message.delete()

@settings_router.callback_query(lambda call: call.data == "main_menu")
async def main_menu(call: types.CallbackQuery):
    user_language = db.get_user_lang(call.from_user.id)
    await call.message.answer(
        answers[user_language[0]]["main_menu_text"],
        reply_markup=get_menu_button(user_language)
    )
    await call.message.delete()