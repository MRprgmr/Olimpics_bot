from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from asgiref.sync import sync_to_async

from Bot.models import Olympiad
from keyboards.inline.callback_datas import olympiad_callback, olympiad_register_callback
from keyboards.inline.olympiads import get_olympiads, olympiad_view_buttons
from loader import dp
from states.get_information_states import OlympiadsState


@dp.message_handler(Text(equals=["📑 Olimpiadalar"]), state='*')
async def select_olympiad(message: Message):
    markup = await sync_to_async(get_olympiads)()
    await message.answer("Hozirda ushbu olimpiadalar mavjud:", reply_markup=markup)
    await OlympiadsState.olympiad.set()


@dp.callback_query_handler(olympiad_callback.filter(), state=OlympiadsState.olympiad)
async def get_information(call: CallbackQuery, callback_data: dict):
    olympiad = await sync_to_async(Olympiad.objects.get)(id=callback_data['id'])
    buttons = await sync_to_async(olympiad_view_buttons)(callback_data['id'])
    await call.message.edit_text(text=olympiad.description, reply_markup=buttons)
    await OlympiadsState.view.set()


@dp.callback_query_handler(text="back", state=OlympiadsState.view)
async def back(call: CallbackQuery):
    markup = await sync_to_async(get_olympiads)()
    await call.message.edit_text("Hozirda ushbu olimpiadalar mavjud:", reply_markup=markup)
    await OlympiadsState.olympiad.set()


@dp.callback_query_handler(olympiad_register_callback.filter(), state=OlympiadsState.view)
async def register(call: CallbackQuery, callback_data: dict):
    print(callback_data)
    await call.answer()
