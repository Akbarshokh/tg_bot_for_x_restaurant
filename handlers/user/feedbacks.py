from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from handlers.user.start import db
from keyboards.inline.user_inline_keyboards import resend_menu_keyboard
from utils.config import answers
from aiogram.filters.command import Command
from states.user import FeedbackStates
from keyboards.default.main_keyboard import get_menu_button

feedback_router= Router()

@feedback_router.message(Command(commands=["feedback"]))
@feedback_router.message(F.text.in_({"Оставить отзыв 💬", "Fikr qoldirish 💬"}))
async def start_feedback_collection(message: types.Message, state: FSMContext):
    """
    Начало сбора отзывов.
    """
    telegram_id = message.from_user.id
    user_language = db.get_user_lang(telegram_id)

    await message.answer(
        text=answers[user_language[0]]["feedback_text"],
        reply_markup=types.ReplyKeyboardRemove()
    )

    # Prompt the user for feedback
    await message.answer(
        text=answers[user_language[0]]["feedback_text"],
        reply_markup=resend_menu_keyboard(user_language[0])
    )

    await state.set_state(FeedbackStates.waiting_for_feedback)


@feedback_router.message(FeedbackStates.waiting_for_feedback)
async def save_feedback(message: types.Message, state: FSMContext):
    """
    Сохранение отзыва в базе данных и возвращение в главное меню.
    """
    telegram_id = message.from_user.id
    db_user_id, username, user_language, phone = db.get_user_data(telegram_id)
    feedback_message = message.text.strip()

    successfully_saved_feedback = db.save_feedback(db_user_id, username, feedback_message)

    if successfully_saved_feedback:
        await message.answer(
            answers[user_language]["feedback_successful"],
            reply_markup=get_menu_button(user_language)
        )
    else:
        await message.answer(
            answers[user_language]["feedback_failed"],
            reply_markup=get_menu_button(user_language)
        )

    await state.clear()