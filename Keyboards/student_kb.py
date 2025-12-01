from aiogram.types import(
    InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton
)



def get_student_main_menu() -> ReplyKeyboardMarkup:

    keyboard = [
        [
           KeyboardButton(text="Домашние задания📋"),
           KeyboardButton(text="Мое расписание⏰")
        ],
        [
            KeyboardButton(text="Составить расписание📅"),
            KeyboardButton(text="Дополнительные уроки📅")
        ],
        [
            KeyboardButton(text="Статус оплаты💳")
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def change_schedule() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="Изменить расписание🖊️", callback_data="change_schedule")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard, resize_keyboard=True)



def day_schedule() ->ReplyKeyboardMarkup:
    keyboard = [
        [
            KeyboardButton(text="Пн-Ср-Пт"),
            KeyboardButton(text="Вт-Чт-Сб")
        ],
        [
            KeyboardButton(text="Индивидуальное📝")
        ],
        [
            KeyboardButton(text="Назад🔙")
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def phone_number() -> ReplyKeyboardMarkup:
    keyboard = [
        [
            KeyboardButton(text="Отправить номер телефона📞", request_contact=True)
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)



def confirm_kb(schedule_type: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Подтвердить✅",
                    callback_data=f"confirm_{schedule_type}"
                )
            ]
        ]
    )

    
def reg_lessons() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="12", callback_data="12"),
            InlineKeyboardButton(text="24", callback_data="24")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard, resize_keyboard=True)


def reg_hours() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="1", callback_data="1"),
            InlineKeyboardButton(text="2", callback_data="2")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard, resize_keyboard=True)



def reg_lessons_week() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="3", callback_data="3")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard, resize_keyboard=True)

