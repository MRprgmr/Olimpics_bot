from aiogram.dispatcher.storage import FSMContext
import qrcode
from aiogram.types.callback_query import CallbackQuery
from loader import dp
import io

def image_to_byte_array(image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format=image.format)
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr


@dp.callback_query_handler(text='qr_me', state='*')
async def get_qr(call: CallbackQuery, state: FSMContext):
    await state.finish()  
    qr_img = qrcode.make(f"id_{call.message.chat.id}")
    await call.message.delete()
    await call.message.answer_photo(photo=image_to_byte_array(qr_img), caption="💳 Sizning Qr idingiz.")