from aiogram import Router, F
from aiogram.types import Message 
from database.db import (get_count_students,
                        get_all_students_ordered,
                        get_all_users_schedule,
                        get_user_profile,
                        get_student_schedule,
                        decrement_remaining_lessons,
                        confirm_payment)


from Keyboards.teacher_kb import (get_student_homeworks_keyboard,
                                    get_homework_check_keyboard,
                                    get_all_students_keyboard,
                                    get_confirm_lesson_keyboard,
                                    get_all_payments_keyboard)


from aiogram.types import CallbackQuery



router = Router()

@router.message(F.text == "Проверить Домашние задания📋")
async def check_homework(message: Message): 
    keyboard = get_student_homeworks_keyboard()
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


@router.message(F.text == "Обзор учеников👥")
async def count_students(message: Message):
    count = get_count_students()
    students = get_all_students_ordered()

    text = f"Количество учеников: {count}\n\n"
    
    if count == 0:
        text += "Учеников пока нет"

    else:
        for i, (username,) in enumerate(students, start=1):
            text += f"{i}. {username}\n"
    await message.answer(text, reply_markup=get_all_students_keyboard())



@router.callback_query(F.data.startswith("student_"))
async def show_student_profile(callback: CallbackQuery):
    user_id = int(callback.data.split("_")[-1])
    student_profile = get_user_profile(user_id)
    if not student_profile:
        await callback.message.answer("Пользователь не найден в базе!😕")
        return

    name, phone, lesson, hours, week, remaining_lessons, payments = student_profile

    if remaining_lessons is None:
        remaining_lessons = lesson

    student_schedule = get_student_schedule(user_id)
    if student_schedule is not None:
        main_schedule, extra_schedule = student_schedule
    else:
        main_schedule = "не составлено"
        extra_schedule = "не добавлено"

    text = (
    f"👤 Имя: {name}\n"
    f"📞 Телефон: {phone}\n\n"
    f"📘 Уроки в месяц: {lesson}\n"
    f"⏰ Часы в день: {hours}\n"
    f"📅 Неделя: {week}\n\n"
    f"📕 Основное расписание: {main_schedule}\n"
    f"📗 Дополнительные уроки: {extra_schedule}\n\n"
    f"📉 Оставшиеся уроки: {remaining_lessons}\n"
    f"💰 Оплаты: {payments}\n"
)
    await callback.message.answer(text)



@router.message(F.text == "Подтвердить урок✅")
async def confirm_lesson(message: Message):
    await message.answer(
        "Выберите какого ученика урок подтвердить",
        reply_markup=get_confirm_lesson_keyboard()
    )

@router.callback_query(F.data.startswith("lesson_"))
async def confirm_lesson_callback(callback: CallbackQuery):
    user_id = int(callback.data.split("_")[-1])

    username = get_user_profile(user_id)[0]
    remaining = decrement_remaining_lessons(user_id)

    if remaining is None:
        await callback.message.answer("Пользователь не найден в базе!😕")
        return
    await callback.message.answer(
        f"Урок ученика {username} подтверждён ✅\n"
        f"Оставшиеся уроки у ученика: {remaining}"
    )





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
            f"   Основное расписание: {main_schedule}⏰\n"
            f"   Дополнительные уроки: {extra}📚\n"
        )

    text = "\n\n".join(schedule_list)
    await message.answer(text)




            
 
@router.message(F.text == "Оплаты💳")
async def show_payments(message: Message):
    await message.answer("Выберите ученика котоого хотите подтвердить оплату:", reply_markup=get_all_payments_keyboard())

@router.callback_query(F.data.startswith("payments_"))
async def confirm_payment_callback(callback: CallbackQuery):
    user_id = int(callback.data.split("_")[-1])

    status = confirm_payment(user_id)
    username = get_user_profile(user_id)[0]

    if status is None:
        await callback.message.answer("Ошибка: пользователь не найден 😕")
        return

    await callback.message.answer(
        f"💳 Оплата ученика {username} подтверждена!\n\n"
        f"Статус оплаты: {status}"
    )
