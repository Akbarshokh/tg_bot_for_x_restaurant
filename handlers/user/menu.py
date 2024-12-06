from oauth2client.service_account import ServiceAccountCredentials
from utils.config import KEY,SHEET_ID
import gspread as gd
import pandas as pd
from handlers.user.start import router
from aiogram import types
from keyboards.default.main_keyboard import give_menu


def get_google_sheet_datas():
    SCOPE = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(KEY, SCOPE)
    gc = gd.authorize(credentials)
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
    df = pd.read_csv(url)
    return df


@router.message(lambda message: message.text.lower() in ["Меню 📋", "Menyu 📋"])
async def resend_code(message: types.Message):
    if message.text == "Меню 📋":
        language = "ru"
    else:
        language = "uz"
    data = get_google_sheet_datas()
    categories = data["Категории"].unique().tolist()
    keyboard = await give_menu(categories)
    await message.answer("choose", reply_markup=keyboard)


