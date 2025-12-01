import asyncio
from aiogram.types import Message



async def recommend_schedule(message: Message, package: int, hours_per_day: int, lessons_week: int):
    monthly_actual = lessons_week * hours_per_day * 4   
    weekly_need = package // 4  


    if monthly_actual == package:
        await message.answer("✔️ Отлично! Ваш выбор идеально подходит.")
        return True


    if monthly_actual < package:
        need_hours = 2 if hours_per_day == 1 else hours_per_day
        await message.answer(
            "❌ Нагрузка недостаточная.\n"
            f"Чтобы соответствовать пакету *{package}*, нужно примерно *{weekly_need} занятий в неделю*.\n"
            f"Рекомендация: *{need_hours} часа в день*.",
            parse_mode="Markdown"
        )
        return False


    if monthly_actual > package:
        await message.answer(
            "⚠️ Нагрузка слишком высокая.\n"
            f"Для пакета *{package}* хватит *1 часа в день*.",
            parse_mode="Markdown"
        )
        return False
