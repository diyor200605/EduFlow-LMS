from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from database.db import is_user_registered
from Keyboards.student_kb import get_student_main_menu
from Keyboards.teacher_kb import get_teacher_main_menu

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот\n\nЕсли ты ученик, нажми на кнопку /student\nЕсли ты учитель, нажми на кнопку /teacher"
    )

@router.message(Command("student"))
async def cmd_student(message: Message):
    if not is_user_registered(message.from_user.id):
        return await message.answer("Сначала зарегистрируйтесь через /register")
    
    await message.answer("Привет! Ты ученик", reply_markup=get_student_main_menu())

@router.message(Command("teacher"))
async def cmd_teacher(message: Message):
    if not is_user_registered(message.from_user.id):
        return await message.answer("Сначала зарегистрируйтесь через /register")

    await message.answer("Привет! Ты учитель", reply_markup=get_teacher_main_menu())



