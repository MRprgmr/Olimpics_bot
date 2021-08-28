from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_menu_user = ReplyKeyboardMarkup(resize_keyboard=True,
                                     keyboard=[
                                         [
                                             KeyboardButton(
                                                 text="📑 Olimpiadalar"),
                                         ],
                                         [
                                             KeyboardButton(
                                                 text="👤 Profil",
                                             )
                                         ]
                                     ])
