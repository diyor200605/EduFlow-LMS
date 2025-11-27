from aiogram import Router, F
from aiogram.types import Message 
from database.db import (get_count_students,
                        get_all_students_ordered,
                        get_all_users_schedule)


from Keyboards.teacher_kb import (get_student_keyboard,
                                    get_homework_check_keyboard)


from aiogram.types import CallbackQuery



router = Router()

@router.message(F.text == "Проверить Домашние задания📋")
async def check_homework(message: Message): 
    keyboard = get_student_keyboard()
    await message.answer("Выберите ученика", reply_markup=keyboard)

@router.callback_query(F.data.startswith("student_hw_"))
async def show_student_homeworks(callback: CallbackQuery):
    user_id = int(callback.data.split("_")[-1])

    keyboard = get_homework_check_keyboard(user_id)

    if not keyboard.inline_keyboard:
        await callback.message.answer("У этого студента пока нет домашек.")
        return

    await callback.message.answer(
        f"Домашние задания студента:",
        reply_markup=keyboard
    )


@router.message(F.text == "Количество учеников👥")
async def count_students(message: Message):
    count = get_count_students()
    students = get_all_students_ordered()

    text = f"Количество учеников: {count}\n\n"
    
    if count == 0:
        text += "Учеников пока нет"

    else:
        for i, (username,) in enumerate(students, start=1):
            text += f"{i}. {username}\n"
    await message.answer(text)

@router.message(F.text == "Расписания⏰")
async def show_schedule(message: Message):

    teacher_schedule = get_all_users_schedule()  

    if not teacher_schedule:
        await message.answer("Учеников пока нет")
        return

    schedule_list = []
    for i, (username, schedule, extra_schedule) in enumerate(teacher_schedule, start=1):
        main_schedule = schedule if schedule else "не составлено"
        extra = extra_schedule if extra_schedule else "доп. уроки не добавлены"
        schedule_list.append(
            f"{i}. {username}:\n"
            f"   Основное расписание: {main_schedule}\n"
            f"   Дополнительные уроки: {extra}"
        )

    text = "\n\n".join(schedule_list)
    await message.answer(text)




@router.message(F.text == "Обзор📝")
async def overview(message: Message):
    cout = get_count_students()
    
    text = f'Количество учеников: {cout}\n\nЛидер:\n\nОбщий доход:\n\nСегодняшние расписания:'

    await message.answer(text)

            
 

    

