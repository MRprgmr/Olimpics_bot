from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Bot.models import Olympiad
from keyboards.inline.callback_datas import olympiad_callback, olympiad_register_callback


def get_olympiads():
    olympiads = InlineKeyboardMarkup()
    data = Olympiad.objects.filter(status=True)
    if len(data) == 0:
        return None
    for olympiad in data:
        olympiads.add(
            InlineKeyboardButton(
                text=olympiad.title,
                callback_data=olympiad_callback.new(
                    title=olympiad.title, id=olympiad.id),
            ))
    return olympiads


def olympiad_view_short(id_olympiad):
    olympiad = Olympiad.objects.get(id=id_olympiad)
    olympiad: Olympiad
    participating_classes = olympiad.participating_classes.all()
    text = "\n".join([f"<b>📌 Nomi:</b>   {olympiad.title}\n",
                      f"<b>📖 Fani:</b>   {olympiad.subject.name}\n",
                      f"<b>📆 Sanasi:</b>   {olympiad.scheduled_date.strftime('%A, %e-%B, %Y')}\n",
                      f"<b>Qatnashuvchi sinflar:</b>",
                      ] + [f"    <code>{grade.name}</code>" for grade in participating_classes])
    button = InlineKeyboardMarkup(row_width=1,
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
                                          ),
                                          InlineKeyboardButton(
                                              text="↓ Ko'rish",
                                              callback_data="show_long_" + id_olympiad,
                                          )
                                      ]
                                  ])
    return {'text': text, 'button': button}


def olympiad_view_long(id_olympiad):
    olympiad = Olympiad.objects.get(id=id_olympiad)
    olympiad: Olympiad
    text = olympiad.description
    button = InlineKeyboardMarkup(row_width=1,
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
                                          ),
                                          InlineKeyboardButton(
                                              text="↑ Yopish",
                                              callback_data="show_less_" + id_olympiad,
                                          )
                                      ]
                                  ])
    return {'text': text, 'button': button}
