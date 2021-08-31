from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

cancel_registration = ReplyKeyboardMarkup(resize_keyboard=True,
                                          keyboard=[
                                              [
                                                  KeyboardButton(
                                                      text="❌ Bekor qilish"),
                                              ]
                                          ])

send_number = request_contract = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📞 Yuborish", request_contact=True),
        ],
    ],
    resize_keyboard=True,
)
