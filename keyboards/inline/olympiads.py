from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Bot.models import Olympiad
from keyboards.inline.callback_datas import olympiad_callback, olympiad_register_callback


def get_olympiads():
    olympiads = InlineKeyboardMarkup()
    data = Olympiad.objects.all()
    for olympiad in data:
        olympiads.add(
            InlineKeyboardButton(
                text=olympiad.title,
                callback_data=olympiad_callback.new(
                    title=olympiad.title, id=olympiad.id),
            ))
    return olympiads


def olympiad_view_buttons(id_olympiad):
    back_button = InlineKeyboardMarkup(row_width=1,
                                       inline_keyboard=[
                                           [
                                               InlineKeyboardButton(
                                                   text="📨 Ro'yxatdan o'tish",
                                                   callback_data=olympiad_register_callback.new(
                                                       id=id_olympiad,
                                                   )
                                               )
                                           ],
                                           [
                                               InlineKeyboardButton(
                                                   text="« ortga",
                                                   callback_data="back",
                                               )
                                           ]
                                       ])
    return back_button
