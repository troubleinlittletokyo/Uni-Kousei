from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_faculty_kb():
    buttons = [
        [InlineKeyboardButton(text="ИКиИН", callback_data="fac_ikiin")],
        [InlineKeyboardButton(text="Экономический", callback_data="fac_eco")],
        [InlineKeyboardButton(text="Юридический", callback_data="fac_law")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)