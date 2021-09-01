from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from asgiref.sync import sync_to_async

from Bot.models import User, Olympiad
from keyboards.inline.callback_datas import olympiad_callback, olympiad_register_callback
from keyboards.inline.olympiads import get_olympiads, olympiad_view_short, olympiad_view_long
from loader import dp
from states.get_information_states import OlympiadsState


def check_and_register(user_id, olympiad_id):
    user = User.objects.get(telegram_id=user_id)
    olympiad = Olympiad.objects.get(id=olympiad_id)
    if user in olympiad.registered_users.all():
        return "already_registered"
    else:
        if user.grade in olympiad.participating_classes.all():
            olympiad.registered_users.add(user)
            olympiad.save()
            return f"success_{olympiad.title}_{olympiad.scheduled_date.strftime('%A, %e-%B')}"
        else:
            return "grade_unavailable"


@dp.message_handler(Text(equals=["📑 Olimpiadalar"]), state='*')
async def select_olympiad(message: Message):
    markup = await sync_to_async(get_olympiads)()
    if markup is None:
        await message.answer("Hozirda hech qanday olimpiada mavjud emas.")
    else:
        await message.answer("Hozirda ushbu olimpiadalar mavjud:", reply_markup=markup)
        await OlympiadsState.olympiad.set()


@dp.callback_query_handler(olympiad_callback.filter(), state=OlympiadsState.olympiad)
async def get_information(call: CallbackQuery, callback_data: dict):
    answer = await sync_to_async(olympiad_view_short)(callback_data['id'])
    await call.message.edit_text(text=answer['text'], reply_markup=answer['button'])
    await OlympiadsState.view.set()


@dp.callback_query_handler(text="back", state=OlympiadsState.view)
async def back(call: CallbackQuery):
    markup = await sync_to_async(get_olympiads)()
    if markup is None:
        await call.message.edit_text("Hozirda hech qanday olimpiada mavjud emas.")
    else:
        await call.message.edit_text("Hozirda ushbu olimpiadalar mavjud:", reply_markup=markup)
        await OlympiadsState.olympiad.set()


@dp.callback_query_handler(Text(startswith='show'), state=OlympiadsState.view)
async def change_view_mode(call: CallbackQuery):
    olympiad_id = call.data.split('_')[2]
    if call.data.startswith('show_long'):
        answer = await sync_to_async(olympiad_view_long)(olympiad_id)
    else:
        answer = await sync_to_async(olympiad_view_short)(olympiad_id)
    await call.message.edit_text(text=answer['text'], reply_markup=answer['button'])


@dp.callback_query_handler(olympiad_register_callback.filter(), state=OlympiadsState.view)
async def register(call: CallbackQuery, callback_data: dict):
    result = await sync_to_async(check_and_register)(user_id=call.message.chat.id, olympiad_id=callback_data['id'])
    if result.startswith('success'):
        await call.answer(
            f"✅ Siz {result.split('_')[1]} olimpiadasiga ro'yxatdan o'tdingiz.\n"
            f"Olimpiada vaqti {result.split('_')[2]} kuni, iltimos kech qolmang!", show_alert=True)
    else:
        if result == "grade_unavailable":
            await call.answer(
                "❗ Kechirasiz ushbu olimpiadaga sizning sinfingiz mos kelmadi, qatnashish uchun iltimos sinfingizni "
                "o'zgartiring.", show_alert=True)
        else:
            await call.answer("❗️ Kechirasiz siz ushbu olimpiadadan oldin ro'yxatdan o'tgansiz.", show_alert=True)
