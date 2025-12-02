from aiogram.types import Message
from database.db import check_payment_status
from database.db import get_user_name
from aiogram import Router

router = Router()

@router.message()
async def check_payment(message: Message):
    user_id = message.from_user.id
    status = check_payment_status(user_id)
    username = get_user_name(user_id)
    
    if status == "не оплачено":
        await message.bot.send_message(
            chat_id=-5049926092,
            text=f"❗ Срок уроков истёк у {username}.\nПора оплатить обучение!"
        )