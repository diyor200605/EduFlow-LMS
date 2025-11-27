from aiogram import Router, F
from aiogram.types import Message, CallbackQuery 
from database.db import (
    add_homework,
    save_schedule,
    is_user_has_schedule,  
    check_user_id,
    is_user_registered,
    get_user_data,
    get_user_schedule,
    add_extra_schedule,
    get_user_extra_schedule,
    add_schedule_individual,
    add_time_schedule
)
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from database.db import add_homework
from datetime import date

from Keyboards.student_kb import (
    day_schedule, 
    confirm_kb, 
    change_schedule as change_schedule_kb,
    get_student_main_menu
)
from states import ScheduleStates
import re


router = Router()

main_menu = {}


github_check = r"^https://github\.com/[A-Za-z0-9_-]+/[A-Za-z0-9._-]+/?$"



def is_github_repo(link: str) -> bool:
    return re.match(github_check, link) is not None


@router.message(F.text == "Домашние задания📋")
async def homework(message: Message, state: FSMContext):
    await state.set_state("send_hw")
    await message.answer("Отправьте ссылку на ваш GitHub репозиторий:")

@router.message(StateFilter("send_hw"))
async def send_hw(message: Message, state: FSMContext):
    link = message.text
    if is_github_repo(link):
        add_homework(message.from_user.id, link, date.today())
        await state.clear()
        await message.answer("Ты успешно отправил домашнее задание учителю!✔️")
    else:
        await message.answer(
        "❌ Неверный формат ссылки!\n\n"
        "Пример правильной ссылки:\n"
        "https://github.com/username/repository"
        )
    await state.clear()
        


@router.message(F.text == "Мое расписание⏰")
async def users_schedule(message: Message):
    user_id = message.from_user.id
    
    schedule_days = get_user_schedule(user_id)
    extra_schedule = get_user_extra_schedule(user_id)

    if not schedule_days and not extra_schedule:
        return await message.answer(
            "У вас еще нет расписания.\n"
            "Создайте его через кнопку «Составить расписание📅»"
        )


    msg = "Ваше расписание:\n\n"

    if schedule_days:
        msg += f"Основные дни: {schedule_days} ⏰\n"
    else:
        msg += "Основные дни: не указаны ❌\n"

    if extra_schedule:
        msg += f"Дополнительные уроки: {extra_schedule} ⏰\n"
    else:
        msg += "Дополнительные уроки: не добавлены ❌\n"

    await message.answer(msg)




@router.message(F.text == "Составить расписание📅")
async def schedule(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        await message.answer("Выберите дни занятие:", reply_markup=day_schedule())
    else:
        await message.answer("Вы не зарегистрированы\n\nДля регистрации нажмите на кнопку /register\n\nДля входа нажмите на кнопку /login")





@router.message(F.text.in_({"Пн-Ср-Пт", "Вт-Чт-Сб"}))
async def schedule_selection(message: Message, state: FSMContext):
    current_state = await state.get_state()


    if current_state != ScheduleStates.change_mode.state:
        if is_user_has_schedule(message.from_user.id):
            return await message.answer(
                "Вы уже составили расписание\n\n"
                "Если хотите изменить расписание, нажмите на кнопку ниже👇",
                reply_markup=change_schedule_kb()
            )


    user_data = get_user_data(message.from_user.id)
    if not user_data:
        return await message.answer("Пользователь не найден в базе!😕")

    username, phone = user_data
    schedule_text = message.text
    schedule_type = 1 if schedule_text == "Пн-Ср-Пт" else 2

    await message.answer(
        f"Проверьте расписание:\n\n"
        f"Имя: {username}\n"
        f"Номер телефона: {phone}\n"
        f"Дни: {schedule_text}\n\n"
        f"Нажмите кнопку *ПОДТВЕРДИТЬ*, если все верно👇",
        reply_markup=confirm_kb(schedule_type),
        parse_mode="Markdown"
    )



@router.callback_query(F.data.startswith("confirm_"))
async def confirm_schedule(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_data(user_id)
    if not user_data:
        return await callback.answer("Пользователь не найден в базе!😕", show_alert=True)

    username = user_data[0]

    if callback.data == "confirm_1":
        selected_schedule = "Пн-Ср-Пт"
    elif callback.data == "confirm_2":
        selected_schedule = "Вт-Чт-Сб"
    else:
        return await callback.answer("Неизвестный тип расписания", show_alert=True)

    save_schedule(user_id, username, selected_schedule)
    await callback.message.answer(f"Расписание {selected_schedule} сохранено✅")
    await callback.answer()



@router.callback_query(F.data == "change_schedule")
async def change_schedule_start(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id

    if not check_user_id(user_id):
        return await callback.message.answer("Такого пользователя нет")

    await state.set_state(ScheduleStates.change_mode)
    await callback.message.answer(
        "Выберите новые дни занятия:",
        reply_markup=day_schedule()
    )



@router.callback_query(F.data == 'schedule_1')
async def change_schedule_mon_wed_fri(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    user_data = get_user_data(user_id)
    if not user_data:
        return await callback.message.answer("Пользователь не найден в базе!")

    username = user_data[0]
    save_schedule(user_id, username, "Пн-Ср-Пт")

    await callback.message.answer("Расписание изменено на Пн-Ср-Пт✅")
    await state.clear()



@router.callback_query(F.data == 'schedule_2')
async def change_schedule_tue_thu_sat(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    user_data = get_user_data(user_id)
    if not user_data:
        return await callback.message.answer("Пользователь не найден в базе!")

    username = user_data[0]
    save_schedule(user_id, username, "Вт-Чт-Сб")

    await callback.message.answer("Расписание изменено на Вт-Чт-Сб✅")
    await state.clear()


@router.message(F.text == "Индивидуальное📝")
async def individual(message: Message, state: FSMContext):
    await message.answer(
        "Напишите свое индивидуальное расписание\n\n"
        "Например:\n"
        "Пн-Ср-Пт\n"
        "Вт-Чт-Сб"
    )
    await state.set_state("send_days_individual")


@router.message(StateFilter("send_days_individual"))
async def send_days_individual(message: Message, state: FSMContext):
    user_id = message.from_user.id
    individual_schedule = message.text

    add_schedule_individual(user_id, individual_schedule)

    await state.update_data(individual_schedule=individual_schedule)

    await message.answer(
        "Дни добавлены✅\n\n"
        "Теперь напишите в какое время вы хотите заниматься\n\n"
        "Например:\n"
        "12:00"
    )
    await state.set_state("send_time_individual")


@router.message(StateFilter("send_time_individual"))
async def send_time_individual(message: Message, state: FSMContext):
    user_id = message.from_user.id
    time_schedule = message.text

    add_time_schedule(user_id, time_schedule)

    data = await state.get_data()
    individual_schedule = data.get("individual_schedule")

    await state.clear()

    await message.answer(
        "Время добавлено✅\n\n"
        "Вы создали расписание под себя!\n\n"
        f"Дни: {individual_schedule}\n"
        f"Время: {time_schedule}"
    )




@router.message(F.text == "Дополнительные уроки📅")
async def extra_lessons(message: Message, state: FSMContext):
    await message.answer("Напишите дни недели дополнительного урока\n\n"
    "Напрмер:\n"
    "Пн-Ср-Пт\n"
    "Вт-Чт-Сб")
    await state.set_state("send_extra_lessons")


@router.message(StateFilter("send_extra_lessons"))
async def send_extra_lessons(message: Message, state: FSMContext):

    user_id = message.from_user.id
    extra_schedule = message.text 

    add_extra_schedule(user_id, extra_schedule)

    await state.clear()
    await message.answer("Дополнительные уроки добавлены✅")

    
@router.message(F.text == "Назад🔙")
async def back(message: Message):
    user_id = message.from_user.id
    if user_id in main_menu:
        await message.answer("Выберите действие:", reply_markup=main_menu[user_id])
    else:
        await message.answer("Выберите действие:", reply_markup=get_student_main_menu())


@router.message(F.text == "Статус оплаты💳")
async def payment_status(message: Message):
    if is_user_registered(message.from_user.id):
        await message.answer("Статус оплаты")
    else:
        await message.answer("Вы не зарегистрированы\n\nДля регистрации нажмите на кнопку /register\n\nДля входа нажмите на кнопку /login")
