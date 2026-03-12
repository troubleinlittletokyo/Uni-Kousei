from aiogram import Router, types, F
from aiogram.filters import Command
from bot.keyboards import get_faculty_kb
from db.queries import get_or_create_user

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    user, created = await get_or_create_user(message.from_user.id)
    
    text = "Давай настроим твой профиль. Выбери свой факультет:"
    await message.answer(text, reply_markup=get_faculty_kb())

@router.callback_query(F.data.startswith("fac_"))
async def process_faculty(callback: types.CallbackQuery):
    faculty_name = callback.data.split("_")[1]
    
    await callback.message.edit_text(f"Твой факультет: {faculty_name.upper()}. Теперь выбери курс...")
    await callback.answer()