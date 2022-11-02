from vk_maria import types
from vk_maria.dispatcher import Dispatcher
from vk_maria.dispatcher.filters import AbstractFilter
from vk_maria.types import EventType
import asyncio
from system.additional_functions import vk, bot_main, download_image
from system.additional_functions import send_photo_tg


# coroutine
async def send_photo(bot, caption):
    await send_photo_tg(bot, caption)


# FILTERS
class DirectPhotoFilter(AbstractFilter):  # фильтр на прямую отправку фото
    def check(self, event: types.Message):
        check_on_command = "#афиша" in event.message.text
        check_on_photo = False
        if event.message.attachments:
            check_on_photo = event.message.attachments[-1].type == "photo"
        return event.chat_id == 2 and check_on_command and check_on_photo


class FromWallPhotoFilter(AbstractFilter):  # фильтр на отправку поста
    def check(self, event: types.Message):
        check_on_command = "#афиша" in event.message.text
        check_on_photo = False
        if event.message.attachments:
            check_on_photo = event.message.attachments[-1].type == "wall"
        return event.chat_id == 2 and check_on_command and check_on_photo


def main():
    dp = Dispatcher(vk)
    # эта хуйня будет ругаться в любом случае, если кто-нить знает, как сделать для данной задачи,
    # так, чтобы не ругалось, то помогите
    loop = asyncio.get_event_loop()

    @dp.event_handler(EventType.MESSAGE_NEW, DirectPhotoFilter)
    def echo(event: types.Message):  # Функция для обработаки афиш из беседы
        url = event.message.attachments[-1].photo.sizes[-1].url
        download_image(url)
        text = event.message.text
        coroutine = send_photo_tg(bot_main, text)
        loop.run_until_complete(coroutine)

    @dp.event_handler(EventType.MESSAGE_NEW, FromWallPhotoFilter)
    def echo(event: types.Message):  # Функция для обработки афиш из записей
        text = event.message.text
        text += event.message.attachments[-1].wall.text
        url = event.message.attachments[-1].wall.attachments[-1].photo.sizes[-1].url
        download_image(url)

    dp.start_polling(debug=True)


if __name__ == "__main__":
    main()
