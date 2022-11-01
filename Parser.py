import datetime
import time
import vk
import logging

from system.database import DatabasePosters, DatabaseSubscribers

token = "084114010841140108411401600b51519e00841084114016ab3c36f1a4e7f2f8a6cff96"

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
logger.info("Starting Parser")
db = DatabasePosters()
db_subscribers = DatabaseSubscribers()


def get_post():
    info = []
    for i in range(5):
        info.append(vk_api.wall.get(access_token=token, owner_id=-82932190, domein='m_news_m',
                                    offset=i+1, count=1, v=5.131))
        time.sleep(0.4)
    print(info, sep='\n')
    users = db_subscribers.get_subscribers()
    print(users, sep='\n')
    for post in info:
        post_text = post['items'][0]['text']
        photo_url = post['items'][0]["attachments"][0]['photo']['sizes'][-1]['url']
        time_date = datetime.date.today() + datetime.timedelta(days=1)
        print(time_date)
        post_id = int(post['items'][0]['id'])
        print(post_id)
        db.set_post(post_id, photo_url, str(time_date), post_text)
        print(db.get_post())


def main():
    # Здесь парсер берет 5 постов
    logger.info("Start saving posts")
    get_post()  # берем 5 постов и заносим их в датабазу


if __name__ == "__main__":
    session = vk.session.API(access_token=token)  # Авторизация
    vk_api = vk.API(session)
    time_now = datetime.datetime.now().hour
    test = datetime.datetime.strptime("21:45", "%H:%M").hour
    start_time = datetime.datetime.strptime("21:15", "%H:%M").hour
    delta = datetime.timedelta(hours=start_time-time_now).seconds
    delta_test = datetime.timedelta(hours=start_time-test).seconds
    print(delta_test)
    while True:
        time_now = datetime.datetime.now().hour
        main()
        logger.info(f"Sleep Until {start_time}")
        time.sleep(86400)

