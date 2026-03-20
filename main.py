import asyncio
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from aiogram import Bot, Dispatcher
from bot.handlers import router
from db.database import init_db

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

if not dp.sub_routers:
    dp.include_router(router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    
    polling_task = asyncio.create_task(dp.start_polling(bot))
    
    yield  
    
    polling_task.cancel()
    await bot.session.close()

app = FastAPI(title="Uni-Kousei", lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "online", "bot_running": True}

if __name__ == "__main__":

    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

