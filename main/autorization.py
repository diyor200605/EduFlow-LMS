from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from states import Registration, Login
from database.db import (
    is_user_registered,
    username_check,
    register_user,
    password_check
)

from Keyboards.student_kb import phone_number, reg_lessons, reg_hours, reg_lessons_week

router = Router()


@router.message(Command("register"))
async def cmd_register(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        return await message.answer("Вы уже зарегистрированы! Используйте /login для входа.")
    
    await message.answer("Введите свой username:")
    await state.set_state(Registration.register_for_name)



@router.message(Registration.register_for_name)
async def register_for_name(message: Message, state: FSMContext):
    username = message.text.strip()

    if username_check(username):
        return await message.answer("Такой username уже существует, введите другой username:")
    
    await state.update_data(username=username)
    await message.answer("Введите свой пароль:")
    await state.set_state(Registration.register_for_password)



@router.message(Registration.register_for_password)
async def register_for_password(message: Message, state: FSMContext):
    password = message.text.strip()
    

    await state.update_data(password=password)

    await message.answer(
        "Нажмите кнопку, чтобы отправить номер телефона:",
        reply_markup=phone_number()
    )
    await state.set_state(Registration.register_for_phone)



@router.message(StateFilter(Registration.register_for_phone))
async def register_for_phone(message: Message, state: FSMContext):


    if not message.contact:
        return await message.answer("Пожалуйста, используйте кнопку, чтобы отправить телефон ☝️", reply_markup=phone_number())

    phone = message.contact.phone_number
    await state.update_data(phone=phone)

    await message.answer("Выберите количество уроков:", reply_markup=reg_lessons())
    await state.set_state(Registration.register_for_lessons)


@router.callback_query(Registration.register_for_lessons)
async def register_for_lessons(callback: CallbackQuery, state: FSMContext):
    lesson = callback.data

    await state.update_data(lesson=lesson)
    await callback.message.answer("Выберите количество часов:", reply_markup=reg_hours())
    await state.set_state(Registration.register_lessons_week)


@router.callback_query(Registration.register_lessons_week)
async def register_lessons_week(callback: CallbackQuery, state: FSMContext):
    lessons_week = callback.data

    await state.update_data(lessons_week=lessons_week)
    await callback.message.answer("Выберите уроков в неделю:", reply_markup=reg_lessons_week())
    await state.set_state(Registration.register_for_hours)


@router.callback_query(Registration.register_for_hours)
async def register_for_hours(callback: CallbackQuery, state: FSMContext):
    hours = callback.data
    await state.update_data(hours=hours)
    
    data = await state.get_data()
    username = data["username"]
    password = data["password"]
    phone = data["phone"]
    lesson = data["lesson"]
    lessons_week = data["lessons_week"]
    hours = data["hours"]


    register_user(
        callback.from_user.id,
        username,
        password,
        phone,
        lesson,
        lessons_week,
        hours
    )


    await callback.message.answer(
        f"🎉 *Регистрация завершена!*\n\n"
        f"Ваши данные:\n"
        f"👤 Username: *{username}*\n"
        f"🔑 Password: *{password}*\n"
        f"📱 Телефон: *{phone}*\n"
        f"📘 Уроки: *{lesson}*\n"
        f"⏳ Уроков в неделю: *{lessons_week}*\n"
        f"⏳ Часы: *{hours}*\n\n"
        f"Пожалуйста, сохраните эти данные.\n\n"
        f"После этого вы можете использовать команды /student и /teacher",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove()
    )

    await state.clear()















    





@router.message(Command("login"))
async def cmd_login(message: Message, state: FSMContext):
    if not is_user_registered(message.from_user.id):
        return await message.answer("Вы не зарегистрированы! Сначала используйте /register.")
    
    await message.answer("Введите свой username:")
    await state.set_state(Login.login_for_name)

@router.message(Login.login_for_name)
async def login_for_name(message: Message, state: FSMContext):
    username = message.text
    if not username_check(username):
        return await message.answer("Такого username не существует. Попробуйте снова:")
    
    await state.update_data(username=username)
    await message.answer("Введите пароль:")
    await state.set_state(Login.login_for_password)

@router.message(Login.login_for_password)
async def login_for_password(message: Message, state: FSMContext):
    data = await state.get_data()
    username = data["username"]
    password = message.text
    
    if not password_check(username, password):
        return await message.answer("Неверный пароль, попробуйте снова:")
    await state.clear()
    await message.answer("Вход выполнен успешно!\n\nТеперь вы можете использовать команды /student и /teacher")
