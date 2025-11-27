import asyncio
from aiogram import Bot, Dispatcher
from config import API_TOKEN
from aiogram import Router
from main.commands import router as commands_router
from main.autorization import router as autorization_router
from handlers.student import router as student_router
from database.db import init_db
from handlers.teacher import router as teacher_router
from aiogram.types import BotCommand

router = Router()

bot = Bot(token=API_TOKEN)

async def set_commands():
    commamds = [
        BotCommand(command="start", description="Начать работу с ботом"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="student", description="Регистрация ученика"),
        BotCommand(command="teacher", description="Регистрация учителя")
    ]
    await bot.set_my_commands(commamds)
async def main():
    init_db()
    print("База данных инициализирована")


    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(autorization_router)
    dp.include_router(commands_router)
    dp.include_router(student_router)
    dp.include_router(teacher_router)
    await set_commands()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
