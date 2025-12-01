from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from database.db import get_all_students, get_homeworks_all_users


def get_teacher_main_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [
            KeyboardButton(text="Обзор учеников👥"),
            KeyboardButton(text="Проверить Домашние задания📋"),
            KeyboardButton(text="Подтвердить урок✅")
        ],
        [

            KeyboardButton(text="Расписания⏰")
        ],
        [
            KeyboardButton(text="Оплаты💳")
        ]
     
        ]
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)



def get_student_homeworks_keyboard() -> InlineKeyboardMarkup:
    all_users = get_all_students()

    keyboard = []

    for user_id, username in all_users:
        keyboard.append([InlineKeyboardButton(text=f"{username}", callback_data=f"student_hw_{user_id}")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_homework_check_keyboard(user_id: int):
    rows = get_homeworks_all_users()
    keyboard = []

    for username, url, send_time in rows:
        keyboard.append([InlineKeyboardButton(text=f"{username} Дата отправки: {send_time}", url=url)])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

    
    
def get_all_students_keyboard():
    all_users = get_all_students()
    keyboard = []
    for user_id, username in all_users:
        keyboard.append([InlineKeyboardButton(text=f"{username}", callback_data=f"student_{user_id}")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)




def get_confirm_lesson_keyboard():
    all_users = get_all_students()
    keyboard = []
    for user_id, username in all_users:
        keyboard.append([InlineKeyboardButton(text=username, callback_data=f"lesson_{user_id}")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
    


def get_all_payments_keyboard():
    all_users = get_all_students()
    keyboard = []
    for user_id, username in all_users:
        keyboard.append([InlineKeyboardButton(text=f"{username}", callback_data=f"payments_{user_id}")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)