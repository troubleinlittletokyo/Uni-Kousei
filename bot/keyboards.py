from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime

def get_registration_kb(items: list, prefix: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in items:
        builder.button(text=str(item), callback_data=f"{prefix}_{item}")
    builder.adjust(2)
    return builder.as_markup()

def get_main_menu_kb() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text="Расписание на сегодня"),
            KeyboardButton(text="Расписание на Завтра"),   
        ],
        [
            KeyboardButton(text="Настройки"),
            KeyboardButton(text=f"Заглушить уведомления {(datetime.now()).strftime("%d.%m")}")
        ]
    ]

    return ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выбери действие из меню"
    )

def get_settings_kb(daily_schedule: bool, notif_lessons: bool):
    builder = InlineKeyboardBuilder()

    schedule_text = "Ежедневная рассылка расписания: ВКЛ" if daily_schedule else "Ежедневная рассылка расписания: ВЫКЛ"
    builder.button(text=schedule_text, callback_data="toggle_daily_schedule")
    builder.button(text="Время рассылки:", callback_data="set_daily_schedule_time")

    notif_text = "Напоминание о занятиях: ВКЛ" if notif_lessons else "Напоминание о занятиях: ВЫКЛ"
    builder.button(text=notif_text, callback_data="toggle_notification")
    builder.button(text="Время до пары:", callback_data="set_notification_time")

    builder.button(text="Сменить данные студента (ВУЗ, Факультет и т.п.)", callback_data="re_register")

    builder.adjust(1, 1, 1, 1, 1)
    return builder.as_markup()