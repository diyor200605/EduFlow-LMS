from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    register_for_name = State()
    register_for_password = State()
    register_for_phone = State()
    register_for_lessons = State()
    register_for_hours = State()
    register_lessons_week = State()

class Login(StatesGroup):
    login_for_name = State()
    login_for_password = State()
    
class Schedule(StatesGroup):
    schedule_for_day = State()
    schedule_for_time = State()

class ScheduleStates(StatesGroup):
    change_mode = State()