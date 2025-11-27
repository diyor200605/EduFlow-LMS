from typing import Callable, Awaitable, Dict, Any
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from database import register_user


class RegistrationMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
                        event: Message | CallbackQuery,
                        data: Dict[str, Any]) -> Any:
                        if not isinstance(event, Message):
                            if event.text and event.text.startswith("/register"):
                                return await handler(event, data)
                            user_id = event.from_user.id

                            if not await register_user(user_id):
                                if isinstance(event, Message):
                                    await event.answer("Вы не зарегистрированы\n\nДля регистрации нажмите на кнопку /register")
                                
                                elif isinstance(event, CallbackQuery):
                                    await event.answer("Вы не зарегистрированы\n\nДля регистрации нажмите на кнопку /register")
                                return

                            return await handler(event, data)
                                
                                
       
