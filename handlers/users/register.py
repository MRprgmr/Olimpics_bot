import re

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, ContentType, ContentTypes, ReplyKeyboardRemove
from asgiref.sync import sync_to_async

from Bot.models import User, Class
from keyboards.default.main_menu import main_menu_user
from keyboards.default.registration import cancel_registration, send_number
from keyboards.inline.callback_datas import grade_callback
from keyboards.inline.registration import profile_buttons, grades_markup, confirmation_buttons
from loader import dp
from states.register_states import Registration


@dp.message_handler(Text(equals=['👤 Profil']), state='*')
async def profile(message: Message):
    user = await sync_to_async(User.objects.get)(telegram_id=message.from_user.id)
    if not user.is_registered:
        await message.answer("⚠️ Sizda hali ma'lumotlar to'ldirilmagan", reply_markup=profile_buttons)


@dp.callback_query_handler(text="register_me")
async def start_registration(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer("1. Familiya ismingizni ketma-ket kiriting, masalan:\n\n<b>👉   Alisherov Valisher</b>",
                              reply_markup=cancel_registration)
    await Registration.full_name.set()


@dp.message_handler(Text(equals=['❌ Bekor qilish']), state=Registration)
async def cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Bosh menu", reply_markup=main_menu_user)


@dp.message_handler(content_types=ContentType.TEXT, state=Registration.full_name)
async def get_full_name(message: Message, state: FSMContext):
    if re.match(r"[A-Za-z]{3,}\s[A-Za-z]{3,}", message.text) is not None:
        await state.update_data(full_name=message.text)
        await message.answer(text="2. Sinfingizni tanlang:", reply_markup=(await sync_to_async(grades_markup)()))
        await Registration.grade.set()
    else:
        await message.answer("❗️ Familiya ism noto'g'ri formatda kiritildi,\n iltimos qayta kiriting:")


@dp.callback_query_handler(grade_callback.filter(), state=Registration.grade)
async def get_grade(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await state.update_data(grade=callback_data)
    await call.message.delete()
    await call.message.answer(
        "3. Telefon raqamingizni kiritish uchun:\n\n<b>📞 Yuborish</b> tugmasini bosing yoki boshqa raqamni quyidagi "
        "ko'rinishda yozing!\n\n👉 +998901234567", reply_markup=send_number)
    await Registration.phone_number.set()


@dp.message_handler(state=Registration.phone_number, content_types=ContentTypes.TEXT | ContentTypes.CONTACT)
async def get_number(message: Message, state: FSMContext):
    if message.content_type == 'contact':
        phone_number = message.contact.phone_number
    else:
        phone_number = message.text
    if phone_number[0] != '+':
        phone_number = '+' + phone_number

    if re.match(r"\+998(?:33|93|94|97|90|91|98|99|95|88)\d\d\d\d\d\d\d", phone_number) is not None:
        await state.update_data(phone_number=phone_number)
        data = await state.get_data()
        fn = data['full_name'].split()
        answer = "\n".join([
            f"<b>Familiya:</b>   {fn[0]}",
            f"<b>Ism:</b>   {fn[1]}",
            f"<b>Sinfi:</b>   {data['grade']['name']}",
            f"<b>Telefon:</b>   {phone_number}\n",
            "Ma'lumotlarni tasdiqlaysizmi ?",
        ])
        msg = await message.answer("🔄", reply_markup=ReplyKeyboardRemove())
        await msg.delete()
        await message.answer(text=answer, reply_markup=confirmation_buttons)
        await Registration.confirmation.set()
    else:
        await message.answer("❗️ Telefon nomeri xato kiritildi, iltimos qayta kiriting:")


@dp.callback_query_handler(state=Registration.confirmation)
async def confirm_user_information(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    if call.data == 'confirm':
        data = await state.get_data()
        user = await sync_to_async(User.objects.get)(telegram_id=call.message.chat.id)
        grade = await sync_to_async(Class.objects.get)(id=data['grade']['id'])
        user: User
        user.full_name = data['full_name']
        user.grade = grade
        user.phone_number = data['phone_number']
        user.is_registered = True
        await sync_to_async(user.save)()
        await call.message.delete()
        await call.message.answer(text='\n'.join([
            "   ✅  ✅  ✅ \n",
            "Tabriklaymiz siz muvaffaqiyatli ro‘yxatdan o‘tdingiz,",
            "endi olimpiadalardan ro'yxatdan o'tishingiz mumkin.\n",
        ]), reply_markup=main_menu_user)
        await state.finish()
