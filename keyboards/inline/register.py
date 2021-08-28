from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

profile_buttons = InlineKeyboardMarkup(row_width=1,
                                       inline_keyboard=[
                                           [
                                               InlineKeyboardButton(
                                                   text="📝 To'ldirish",
                                                   callback_data="register_me"
                                               )
                                           ],
                                           [
                                               InlineKeyboardButton(
                                                   text="❌ Yopish",
                                                   callback_data="close",
                                               )
                                           ]
                                       ])
