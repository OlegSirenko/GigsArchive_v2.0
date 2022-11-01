import datetime
from PIL.Image import Image
from aiogram import types, Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from vk_maria.upload import Upload
from vk_maria import Vk
from config.tokens import telegram_token, vk_token
from PIL import Image
import requests
import time


vk = Vk(access_token=vk_token)
token = telegram_token

bot_main = Bot(token, parse_mode="HTML")
# db = DatabaseGoodPeople()


# функция для создания клавиатуры в телеграм боте.
def create_keyboard(buttons: dict = None,  # конструктор клавиатуры
                    inline: bool = True) -> InlineKeyboardBuilder | ReplyKeyboardBuilder:
    if buttons is None:
        buttons = {"1": "1", "2": "2"}
    if inline:
        builder = InlineKeyboardBuilder()
        for button in buttons.keys():
            builder.add(types.InlineKeyboardButton(text=button, callback_data=buttons[button]))
    else:
        builder = ReplyKeyboardBuilder()
        for button in buttons.keys():
            builder.add(types.ReplyKeyboardButton(text=button))
    return builder


# функция для людей с высоким социальным рейтингом или админов
async def fast_posting(bot: Bot, message: types.Message):
    await bot.download(message.photo[-1], destination='resources/images/image_tg.jpg')
    await message.send_copy(-1001812728287)
    await message.reply("Ваша афиша уже отправлена в канал и беседу!\nСпасибо, что пользуетесь нашим ботом!")


async def send_photo_tg(bot: Bot, caption, url=None, user=None):
    if url is None and user is None:
        await bot.send_photo(-1001812728287, types.FSInputFile("resources/images/image_vk.jpg"),
                             caption)  # в релизе поменять АЙДИЧАТА!!!
    else:
        await bot.send_photo(chat_id=user, caption=caption, photo=types.URLInputFile(url))


def send_photo(caption: str):
    upload = Upload(vk)
    photo = upload.photo('resources/images/image_tg.jpg')
    vk.messages_send(chat_id=2, attachment=photo, message=caption)


def check_user_in_db(db, user_id: int):
    user = db.get_user(uid=user_id)
    if not user:
        print("Setting New User!!!!")
        db.set_user(uid=user_id, rating=0)
        user = [(user_id, 0)]
    return user[0]


def download_image(url, filename=None):
    filename = "image_parser" if filename else "image_vk"
    im = Image.open(requests.get(url, stream=True).raw)
    im.save(f"resources/images/{filename}.jpg")


def convert_to_bytes(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data



