from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from asgiref.sync import sync_to_async

from Bot.models import User
from keyboards.inline.register import profile_buttons
from loader import dp


@dp.message_handler(Text(equals=['👤 Profil']), state='*')
async def profile(message: Message):
    user = await sync_to_async(User.objects.get)(telegram_id=message.from_user.id)
    if not user.is_registered:
        await message.answer("⚠️ Sizda hali ma'lumotlar to'ldirilmagan", reply_markup=profile_buttons)


@dp.callback_query_handler(text="close")
async def home(call: CallbackQuery):
    await call.message.delete()
