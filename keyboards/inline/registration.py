from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Bot.models import Class
from keyboards.inline.callback_datas import grade_callback

profile_buttons = InlineKeyboardMarkup(row_width=1,
                                       inline_keyboard=[
                                           [
                                               InlineKeyboardButton(
                                                   text="📝 To'ldirish",
                                                   callback_data="register_me"
                                               )
                                           ]
                                       ])


def grades_markup():
    grades = InlineKeyboardMarkup()
    data = Class.objects.all()
    for grade in data:
        grades.add(
            InlineKeyboardButton(
                text=grade.name,
                callback_data=grade_callback.new(
                    name=grade.name, id=grade.id),
            ))
    return grades


confirmation_buttons = InlineKeyboardMarkup(row_width=2,
                                            inline_keyboard=[
                                                [
                                                    InlineKeyboardButton(
                                                        text="✅ Tasdiqlash",
                                                        callback_data="confirm",
                                                    )
                                                ],
                                                [
                                                    InlineKeyboardButton(
                                                        text="🔄 Qayta to'ldirish",
                                                        callback_data="register_me",
                                                    )
                                                ]
                                            ])

is_poorly_supplied_buttons = InlineKeyboardMarkup(row_width=2,
                                                  inline_keyboard=[
                                                      [
                                                          InlineKeyboardButton(
                                                              text="✅ Ha",
                                                              callback_data="yes",
                                                          )
                                                      ],
                                                      [
                                                          InlineKeyboardButton(
                                                              text="❌ Yo'q",
                                                              callback_data="no",
                                                          )
                                                      ]
                                                  ])
