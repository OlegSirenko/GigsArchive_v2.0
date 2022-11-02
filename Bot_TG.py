import asyncio
import datetime
import logging

import aioschedule
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from config.admin_info import admins
from system.additional_functions import bot_main
from config import text_messages
from system.additional_functions import create_keyboard, fast_posting, send_photo, check_user_in_db
from system.database import DatabaseGoodPeople, DatabasePosters, DatabaseSubscribers

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
logger.info("Starting bot")

dp = Dispatcher()
db_good = DatabaseGoodPeople()  # import database of good people
db_posters = DatabasePosters()  # import database of posts
db_subscribers = DatabaseSubscribers()  # import database of subscribers


@dp.message(Command(commands=['start', 'help']))
async def start(message: types.Message, bot: Bot):
    print(message.chat.id)
    bot_commands = [
        types.BotCommand(command="/help", description="А как? Что? Зачем?"),
        types.BotCommand(command="/tomorrow", description="А что там по мероприятиям на завтра?"),
        types.BotCommand(command='/today', description="А что там по мероприятиям на сегодня?")
    ]
    await bot.set_my_commands(bot_commands)
    await message.answer(text_messages.start_messages["greeting"])
    await message.answer_photo(photo=types.FSInputFile("resources/images/image_tg.jpg"),
                               caption=text_messages.start_messages['description'])
    await message.answer(text_messages.start_messages["posting"])
    await message.answer(text_messages.start_messages["additional"])


@dp.message(Command(commands=["tomorrow"]))
async def tomorrow(message: types.Message):
    date = str(datetime.date.today()+datetime.timedelta(days=1)).replace('-', '')
    print(date)
    posters = db_posters.get_post(datetime=date)
    print(posters)
    if posters:
        await message.answer(text_messages.poster_status_messages["on_poster_tomorrow"])
        for post in posters:
            await message.answer_photo(caption=post[3], photo=types.URLInputFile(post[1]))
    else:
        await message.answer(text_messages.poster_status_messages["on_poster_tomorrow_error"])


@dp.message(Command(commands=["today"]))
async def today(message: types.Message):
    date = str(datetime.date.today()).replace('-', '')
    print(date)
    posters = db_posters.get_post(datetime=date)
    print(posters)
    if posters:
        await message.answer(text_messages.poster_status_messages["on_poster_today"])
        for post in posters:
            await message.answer_photo(caption=post[3], photo=types.URLInputFile(post[1]))
    else:
        await message.answer(text_messages.poster_status_messages["on_poster_today_error"])


@dp.message()  # функция для обработки новых афиш
async def poster(message: types.Message, bot: Bot):
    if message.caption and '#афиша' in str(message.caption).lower() or '#poster' in str(message.caption).lower():
        rating = check_user_in_db(db_good, int(message.from_user.id))[1]
        # если отправляет админ или юзер с высоким рейтингом, то можно кидать сразу в канал.
        if int(message.from_user.id) in admins or rating > 2:  #
            await fast_posting(bot, message)
            send_photo(caption=message.caption)
            return
        await message.reply(text=text_messages.new_poster_messages['on_moderation'])
        buttons = {"Ok": f"Ok/{message.from_user.id}", "Not Ok": f"Nok/{message.from_user.id}"}
        keyboard = create_keyboard(buttons=buttons, inline=True)
        await message.send_copy(540929323, reply_markup=keyboard.as_markup(resize_keyboard=True))  # на модерации
    elif int(message.chat.id) > 0:
        # дополнительная проверка на чат, чтобы не тригеролось на сообщения в канале.
        await message.reply(text=text_messages.error_messages['user_error'])


@dp.callback_query()
async def get_moderator_answer(callback: types.InlineQuery, bot: Bot):
    answer, user_id = str(callback.data).split('/')
    if "N" not in answer:  # если это Ок, то отправляем
        await callback.message.answer(text_messages.poster_status_messages['message_ok'])
        await bot.edit_message_reply_markup(callback.from_user.id, callback.message.message_id, reply_markup=None)
        await bot.download(callback.message.photo[-1], destination='resources/images/image_tg.jpg')
        # в релизе поменять АЙДИЧАТА!!!
        await bot.send_photo(-1001812728287, types.FSInputFile("resources/images/image_tg.jpg"),
                             callback.message.caption)
        rating = db_good.get_user(user_id)[0][1]
        db_good.update_user(user_id, rating + 1)
        send_photo(caption=callback.message.caption)
        text = text_messages.poster_status_messages['answer_ok']
        await bot.send_message(user_id, text=text)
    else:
        await bot.edit_message_reply_markup(callback.from_user.id, callback.message.message_id, reply_markup=None)
        await callback.message.answer(text_messages.poster_status_messages['message_nok'])
        await bot.send_message(user_id, text=text_messages.poster_status_messages['answer_not_ok'])


def main():
    bot = bot_main
    dp.run_polling(bot)


if __name__ == "__main__":
    main()




