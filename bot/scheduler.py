import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.services import get_schedule, format_schedule 
from db.queries import get_users_by_time 

async def send_daily_notifications(bot):
    now = datetime.datetime.now()
    now_time = datetime.datetime.now().strftime("%H:%M")

    cur_weekday = now.weekday()
    if cur_weekday == 6:
        return
    
    users = await get_users_by_time(now_time)
    
    today = datetime.datetime.now().date()
    
    for user in users:
        try:
            raw_data = await get_schedule(user.tg_id, today)

            if not raw_data:
                continue
            
            final_text = format_schedule(raw_data, today)
            
            await bot.send_message(
                user.tg_id, 
                final_text, 
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Ошибка рассылки для {user.tg_id}: {e}")

def setup_scheduler(bot):
    scheduler = AsyncIOScheduler(timezone="Asia/Yakutsk") 
    scheduler.add_job(send_daily_notifications, "interval", minutes=1, args=[bot])
    return scheduler