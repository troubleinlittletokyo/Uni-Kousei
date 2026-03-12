import asyncio
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from aiogram import Bot, Dispatcher
from bot.handlers import router
from db.database import init_db

load_dotenv()

# Инициализация бота и диспетчера
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Глобальный флаг, чтобы не подключать роутер дважды
if not dp.sub_routers:
    dp.include_router(router)

# СОВРЕМЕННЫЙ СПОСОБ: Lifespan вместо on_event
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Действия при запуске
    print("=== ПОДГОТОВКА БАЗЫ ДАННЫХ ===")
    await init_db()
    
    print("--- ЗАПУСК БОТА ---")
    polling_task = asyncio.create_task(dp.start_polling(bot))
    
    yield  # Здесь приложение "живет"
    
    # Действия при выключении
    print("--- ОСТАНОВКА БОТА ---")
    polling_task.cancel()
    await bot.session.close()

app = FastAPI(title="AmSU Student Assistant", lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "online", "bot_running": True}

if __name__ == "__main__":
    import uvicorn
    # Запускаем без reload=True внутри кода, чтобы избежать конфликтов при разработке в VS Code
    # Или запускай через терминал: uv run uvicorn main:app --reload
    uvicorn.run(app, host="127.0.0.1", port=8000)