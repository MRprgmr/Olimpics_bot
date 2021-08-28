from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from asgiref.sync import sync_to_async

from Bot.models import User
from keyboards.default.main_menu import main_menu_user
from loader import dp


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    await dp.current_state().finish()
    user, created = await sync_to_async(User.objects.update_or_create) \
        (telegram_id=message.from_user.id,
         defaults={'name': message.from_user.first_name, 'username': message.from_user.username})
    await sync_to_async(user.save)()
    await message.answer(f"Assalomu alaykum, {message.from_user.first_name}", reply_markup=main_menu_user)

