import re

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, ContentType, ContentTypes, ReplyKeyboardRemove
from asgiref.sync import sync_to_async

from Bot.models import User, Class
from keyboards.default.main_menu import main_menu_user
from keyboards.default.registration import cancel_registration, send_number
from keyboards.inline.callback_datas import grade_callback
from keyboards.inline.profile import edit_profile
from keyboards.inline.registration import profile_buttons, grades_markup, confirmation_buttons, \
    is_poorly_supplied_buttons
from loader import dp
from states.register_states import Registration


def make_profile_text(user):
    user: User
    fn = user.full_name.split()
    answer = "\n".join([
        f"<b>Familiya:</b>   {fn[0]}",
        f"<b>Ism:</b>   {fn[1]}",
        f"<b>Sinfi:</b>   {user.grade.name}",
        f"<b>Telefon:</b>   {user.phone_number}\n",
    ])
    return answer


# Profile button clicked
@dp.message_handler(Text(equals=['👤 Profil']), state='*')
async def profile(message: Message, state: FSMContext):
    await state.finish()
    user = await sync_to_async(User.objects.get)(telegram_id=message.from_user.id)
    if not user.is_registered:
        await message.answer("⚠️ Sizda hali ma'lumotlar to'ldirilmagan", reply_markup=profile_buttons)
    else:
        answer_text = await sync_to_async(make_profile_text)(user)
        await message.answer(text=answer_text, reply_markup=edit_profile)


# register callback returned
@dp.callback_query_handler(text="register_me", state='*')
async def start_registration(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer("1. Familiya ismingizni ketma-ket kiriting, masalan:\n\n<b>👉   Alisherov Valisher</b>",
                              reply_markup=cancel_registration)
    await Registration.full_name.set()


# cancel button clicked while registration
@dp.message_handler(Text(equals=['❌ Bekor qilish']), state=Registration)
async def cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Bosh menu", reply_markup=main_menu_user)


# full name was sent by user
@dp.message_handler(content_types=ContentType.TEXT, state=Registration.full_name)
async def get_full_name(message: Message, state: FSMContext):
    response = message.text.split()
    if len(response) == 2 and response[0].isalpha() and response[1].isalpha():
        await state.update_data(full_name=message.text)
        await message.answer(text="2. Sinfingizni tanlang:", reply_markup=(await sync_to_async(grades_markup)()))
        await Registration.grade.set()
    else:
        await message.answer("❗️ Familiya ism noto'g'ri formatda kiritildi,\n iltimos qayta kiriting:")


# grade selected by user
@dp.callback_query_handler(grade_callback.filter(), state=Registration.grade)
async def get_grade(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await state.update_data(grade=callback_data)
    await call.message.delete()
    await call.message.answer(
        "3. Telefon raqamingizni kiritish uchun:\n\n<b>📞 Yuborish</b> tugmasini bosing yoki boshqa raqamni quyidagi "
        "ko'rinishda yozing!\n\n👉 +998901234567", reply_markup=send_number)
    await Registration.phone_number.set()


# phone number was sent by user
@dp.message_handler(state=Registration.phone_number, content_types=ContentTypes.TEXT | ContentTypes.CONTACT)
async def get_number(message: Message, state: FSMContext):
    if message.content_type == 'contact':
        phone_number = message.contact.phone_number
    else:
        phone_number = message.text
    if phone_number[0] != '+':
        phone_number = '+' + phone_number

    if re.match(r"\+998(?:33|93|94|97|90|91|98|99|95|88)\d\d\d\d\d\d\d", phone_number) is not None:
        msg = await message.answer('🔄', reply_markup=ReplyKeyboardRemove())
        await msg.delete()
        await state.update_data(phone_number=phone_number)
        await message.answer(
            "4. Siz kam ta'minlangan o'quvchilar ro'yxatiga kirasizmi?\n\n ☝️ <i>Iltimos so'rovga to'g'ri javob "
            "bering❗</i>️", reply_markup=is_poorly_supplied_buttons)
        await Registration.is_poorly_supplied.set()
    else:
        await message.answer("❗️ Telefon nomeri xato kiritildi, iltimos qayta kiriting:")


# answer yes or no to know is user poorly supplied
@dp.callback_query_handler(state=Registration.is_poorly_supplied)
async def get_yes_or_no(call: CallbackQuery, state: FSMContext):
    if call.data in ['yes', 'no']:
        if call.data == 'yes':
            await state.update_data(is_poorly_supplied=True)
        else:
            await state.update_data(is_poorly_supplied=False)
        data = await state.get_data()
        fn = data['full_name'].split()
        answer = "\n".join([
            f"<b>Familiya:</b>   {fn[0]}",
            f"<b>Ism:</b>   {fn[1]}",
            f"<b>Sinfi:</b>   {data['grade']['name']}",
            f"<b>Telefon:</b>   {data['phone_number']}\n",
            "Ma'lumotlarni tasdiqlaysizmi ?",
        ])
        await call.message.edit_text(text=answer, reply_markup=confirmation_buttons)
        await Registration.confirmation.set()


# completion of registration
@dp.callback_query_handler(state=Registration.confirmation)
async def confirm_user_information(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    if call.data == 'confirm':
        data = await state.get_data()
        user = await sync_to_async(User.objects.get)(telegram_id=call.message.chat.id)
        grade = await sync_to_async(Class.objects.get)(id=data['grade']['id'])
        user: User
        user.is_poorly_supplied = data['is_poorly_supplied']
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
