from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
from dotenv import load_dotenv
import os
from keyboards import *
from database import *
import requests
import hashlib


load_dotenv()

TOKEN = os.getenv('TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
DEEPL_API_KEY = os.getenv('DEEPL_API_KEY')


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

user_step = {}
user_data = {}

def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


@dp.message_handler(commands=['start'])
async def start(message: Message):
    user_id = int(message.from_user.id)

    user = get_user(user_id)
    if user:
        await message.answer('Welcome back!', reply_markup=main_menu_keyboard())

    else:
        user_step[user_id] = 'phone'
        await message.answer('📱Send phone number',reply_markup=phone_keyboard())



@dp.message_handler(text='❌Cancel')
async def phone(message: Message):
    user_id = int(message.from_user.id)

    user_data.pop(user_id, None)
    user_step.pop(user_id, None)

    await message.answer("❌Canceled", reply_markup=remove_keyboard())


@dp.message_handler(content_types=['contact'])
async def get_phone(message: Message):
    user_id = int(message.from_user.id)

    if user_step.get(user_id) != 'phone':
        return

    user_data[user_id] = {'phone': message.contact.phone_number}
    user_step[user_id] = 'name'

    await message.answer("Send your full name", reply_markup=cancel_keyboard())




# Botni ozi

@dp.message_handler()
async def message_handler(message: Message):
    user_id = int(message.from_user.id)
    text = message.text

    step = user_step.get(user_id)

    #------------------------------------------------------------------------------------------------------------------
    # create password
    if step == 'name':
        user_data[user_id]['name'] = text
        user_step[user_id] = 'password'

        await message.answer("🔒 Create a password (min 6): ", reply_markup=cancel_keyboard())
        return

    # ------------------------------------------------------------------------------------------------------------------
    # check password
    if step == 'password':
        password = text
        if len(password) < 6:
            await message.answer("⚠️ password is too short", reply_markup=cancel_keyboard())
            return

        data = user_data[user_id]

        create_user(
            user_id,
            data['name'],
            data['phone'],
            hash_password(text)
        )

        user_data.pop(user_id, None)
        user_step.pop(user_id, None)

        await message.answer("✅ Registered", reply_markup=main_menu_keyboard())
        return

    # ------------------------------------------------------------------------------------------------------------------
    # review to my bot
    if step == 'review':
        user = get_user(user_id)

        if user:
            save_review(user[0], text)

        await bot.send_message(ADMIN_ID,
                               f"Review from {user_id}:\n{text}")

        user_step[user_id] = 'menu'

        await message.answer("✅Sent", reply_markup=main_menu_keyboard())
        return

    # ------------------------------------------------------------------------------------------------------------------
    # main menu
    if text == "💬 Review":
        user_step[user_id] = 'review'
        await message.answer("✏️ Send review to admin", reply_markup=cancel_keyboard())
        return


    if text == "🌐 Translate":
        user_step[user_id] = 'translate'
        await message.answer("✏️ Send text to translate")
        return

    if text == "ℹ️ Help":
        await message.answer("Send text in english 🇬🇧 it will translate to russian 🇷🇺")
        return

    # ------------------------------------------------------------------------------------------------------------------
    # translate

    if step == 'translate':
        try:
            response = requests.post(
                "https://api-free.deepl.com/v2/translate",
                headers={
                    "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}"
                },
                data={
                    "text": text,
                    "target_lang": "RU"
                }
            )

            result = response.json()

            if "translations" not in result:
                await message.answer(f"❌ API Error: {result}")
                return

            translation = result['translations'][0]['text']

            user = get_user(user_id)

            if user:
                save_translation(user[0], text, translation)

                await message.answer(
                    f"🌐 <b>Translation:</b> {translation}", parse_mode="HTML"
                )


        except Exception as e:

            print(e)

            await message.answer(f"❌Error: {e}")

        return

    # ------------------------------------------------------------------------------------------------------------------
    # na vsyakiy sluchay
    if not get_user(user_id):
        await message.answer("⚠️ Send /start first")
    else:
        await message.answer("Use menu 👇", reply_markup=main_menu_keyboard())







if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)