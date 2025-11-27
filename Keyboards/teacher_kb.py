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
            KeyboardButton(text="Количество учеников👥"),
            KeyboardButton(text="Проверить Домашние задания📋")
        ],
        [
            KeyboardButton(text="Оплаты💳"),
            KeyboardButton(text="Расписания⏰")
        ],
     
        ]
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)



def get_student_keyboard() -> InlineKeyboardMarkup:
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

    
    




  
        
    