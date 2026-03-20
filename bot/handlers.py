from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.states import Registration
from bot.keyboards import get_registration_kb, get_main_menu_kb, get_settings_kb
from db.queries import *
from core.services import format_schedule
from datetime import datetime
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


router = Router()


#COMMANDS--------------------------------------------------------------------------------

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await get_or_create_user(message.from_user.id)
    unis = ["АмГУ", "БГПУ", "ДальГау", "АГМА"]
    await message.answer("Добро пожаловать в Uni-Kousei! Выбери свой университет:", reply_markup=get_registration_kb(unis, "uni"))
    await state.set_state(Registration.choosing_university)

@router.message(Command("reset"))
async def cmd_reset(message: types.Message, state: FSMContext):
    await state.clear()
    await cmd_start(message, state)

#BOTTONS---------------------------------------------------------------------------------

@router.message(F.text == "Расписание на сегодня")
async def show_today_schedule(message: types.Message):
    today = datetime.now().date()
    data = [
        {"time": "08:15", "subject": "Математический анализ", "room": "003"},
        {"time": "09:55", "subject": "Математический анализ", "room": "525"},
    ]
    #parser
    #await message.answer("Запрашиваю расписание на сегодня. . .")
    text = format_schedule(data, today)
    await message.answer(text, parse_mode="Markdown")

@router.message(F.text == "Расписание на завтра")
async def show_tomorrow_schedule(message: types.Message):
    #parser
    await message.answer("Запрашиваю расписание на завтра. . .")

@router.message(F.text == "Настройки")
async def open_settings(message: types.message):
    user = await get_or_create_user(message.from_user.id)
    await message.answer(
        "Настройки профиля\n\n"
        "Здесь можно управлять своими данными и временем напоминаний",
        reply_markup=get_settings_kb(user.daily_schedule, user.notifications_lessons),
        parse_mode="HTML"
    )

@router.message(F.text == f"Заглушить уведомления {(datetime.now()).strftime("%d.%m")}")
async def cancel_notification(message: types.message):
    await message.answer("Сегодня оповещений о занятиях не будет.")

#REGISTRATION----------------------------------------------------------------------------

@router.callback_query(Registration.choosing_university, F.data.startswith("uni_"))
async def process_uni(callback: types.CallbackQuery, state: FSMContext): 
    uni = callback.data.split("_")[1]
    await state.update_data(university=uni)

    faculties = ["ИКиИН", "ФДиТ", "ФилФак", "ЭнергоФак", "ФСН", "ЮрФак", "Эконом", "ФМО", "ФСПО"]
    await callback.message.edit_text("Теперь выбери факультет:", reply_markup=get_registration_kb(faculties, "fac"))
    await state.set_state(Registration.choosing_faculty)

@router.callback_query(Registration.choosing_faculty, F.data.startswith("fac_"))
async def process_fac(callback: types.CallbackQuery, state: FSMContext): 
    fac = callback.data.split("_")[1]
    await state.update_data(faculty=fac)

    courses = ["1", "2", "3", "4", "5", "Магистратура"]
    await callback.message.edit_text("Теперь укажи свой курс:", reply_markup=get_registration_kb(courses, "course"))
    await state.set_state(Registration.choosing_course)

@router.callback_query(Registration.choosing_course, F.data.startswith("course_"))
async def process_course(callback: types.CallbackQuery, state: FSMContext): 
    course = callback.data.split("_")[1]
    await state.update_data(course=course)

    await callback.message.edit_text("Напиши название своей группы (например, 5110-ос):")
    await state.set_state(Registration.choosing_group)

@router.message(Registration.choosing_group)
async def process_group(message: types.Message, state: FSMContext):
    await state.update_data(group_name=message.text)
    
    await message.answer(
        f"Группа <b>{message.text}</b> принята.\n\n"
        "Теперь введи номер своей <b>подгруппы</b> (только число).\n"
        "Если деления нет, отправь <b>0</b>.",
        parse_mode="HTML"
    )
    
    await state.set_state(Registration.choosing_subgroup)

@router.message(Registration.choosing_subgroup)
async def process_subgroup(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введи номер подгруппы цифрами (например, 1, 2 или 0).")
        return

    subgroup = int(message.text)
    user_data = await state.get_data()
    
    try:
        await update_user(
            message.from_user.id, 
            university=user_data.get('university'),
            faculty=user_data.get('faculty'),
            course=user_data.get('course'),
            group_name=user_data.get('group_name'),
            subgroup=subgroup
        )
        
        sub_info = "Весь поток" if subgroup == 0 else f"{subgroup}-я подгруппа"
        
        await message.answer(
            f"✅ Регистрация успешно завершена!\n\n"
            f"<b>Группа:</b> {user_data.get('group_name')}\n"
            f"<b>Подгруппа:</b> {sub_info}",
            reply_markup=get_main_menu_kb(),
            parse_mode="HTML"
        )
        
        await state.clear()
        
    except Exception as e:
        await message.answer(f"❌ Ошибка при сохранении данных: {e}")
        print(f"Ошибка БД: {e}")

#SETTINGS

@router.callback_query(F.data == "toggle_daily_schedule")
async def toggle_daily(callback: types.CallbackQuery):
    user = await get_or_create_user(callback.from_user.id)
    new_status = not user.daily_schedule

    await update_user_daily_schedule(callback.from_user.id, new_status)

    await callback.message.edit_reply_markup(
        reply_markup=get_settings_kb(new_status, user.daily_schedule)
    )
    await callback.answer("Статус рассылки изменен")

@router.callback_query(F.data == "toggle_notification")
async def toggle_notification(callback: types.CallbackQuery):
    user = await get_or_create_user(callback.from_user.id)
    new_status = not user.daily_schedule

    await update_user_notification(callback.from_user.id, new_status)

    await callback.message.edit_reply_markup(
        reply_markup=get_settings_kb(new_status, user.notifications_lessons)
    )
    await callback.answer("Статус оповещений о занятиях изменен")

@router.callback_query(F.data == "re_register")
async def start_re_registration(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Начнем заново. Введи название своего ВУЗа:")
    await state.set_state(Registration.choosing_university)
    await callback.answer()



 