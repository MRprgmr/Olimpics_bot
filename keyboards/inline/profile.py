from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

edit_profile = InlineKeyboardMarkup(row_width=1,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(
                                                text="🖋 O'zgartirish",
                                                callback_data="register_me"
                                            )
                                        ]
                                    ])
