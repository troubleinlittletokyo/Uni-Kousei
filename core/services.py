import datetime

async def get_schedule(tg_id: int, date: datetime.date):
    #parser
    schedule_data = [
        {"time": "08:15", "subject": "Математический анализ", "room": "003"},
        {"time": "09:55", "subject": "Математический анализ", "room": "525"},
    ]
    return schedule_data

def format_schedule(data: list, date: datetime.date) -> str:
    if not data:
        return "Пар нет!"
    
    text = f"Расписание на *{date.strftime("%d.%m")}*\n\n"
    text += "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n"

    for item in data:
        text += f" `{item["time"]}` - *{item["subject"]}*\n"
        text += f" Аудитория: {item["room"]}\n\n"
    
    return text
