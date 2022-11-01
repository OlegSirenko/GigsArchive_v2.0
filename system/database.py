import sqlite3


class DatabaseSubscribers:
    def __init__(self):
        self.conn = sqlite3.connect('./resources/databases/subscribers.db')  # create database for tasks.
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS subscribers(user_id INT PRIMARY KEY);")
        self.conn.commit()

    def set_subscriber(self, userid):
        self.cur.execute(f"INSERT OR IGNORE INTO subscribers(user_id) VALUES({userid});")
        self.conn.commit()

    def get_subscribers(self):
        subscribers = self.cur.execute(f"SELECT * FROM subscribers;").fetchall()
        return subscribers

    def remove_subscriber(self, userid):
        self.cur.execute(f"DELETE FROM subscribers WHERE user_id={userid};")
        self.conn.commit()


class DatabasePosters:
    def __init__(self):
        self.conn = sqlite3.connect('./resources/databases/posts.db')  # create database for tasks.
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS posts(post_id INT PRIMARY KEY, image TEXT, "
                         "datetime TEXT, text TEXT);")
        self.conn.commit()

    def set_post(self, post_id, image, datetime, text):  # datetime здесь это день в который было запощено
        cur = self.conn.cursor()
        cur.execute("INSERT OR IGNORE INTO posts(post_id, image, datetime, text) VALUES(?, ?, ?, ?);",
                    (post_id, image, datetime, text))
        cur.close()
        self.conn.commit()

    def get_post(self, last: bool = False, datetime: str = None):
        if datetime:
            # берем посты за день
            posts = self.cur.execute(f"SELECT * FROM posts WHERE datetime={datetime};").fetchall()
            self.conn.commit()
        elif last:
            posts = self.cur.execute(f"SELECT * FROM posts;").fetchone()
        else:
            # Берем все посты из датабазы
            posts = self.cur.execute(f"SELECT * FROM posts;").fetchall()
        return posts


class DatabaseBanned:
    def __init__(self):
        self.conn = sqlite3.connect('./resources/databases/bad_people.db')  # create database for tasks.
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
                                    userid INT PRIMARY KEY, comment TEXT);""")
        self.conn.commit()

    def set_user(self, uid: int, comment: str):  # add to banned people
        user = (uid, comment)
        self.cur.execute("INSERT INTO users(userid, comment) VALUES(?, ?);", user)
        self.conn.commit()

    def delete_user(self, uid):  # delete from banned people
        self.cur.execute(f"DELETE FROM users WHERE userid={uid}")
        self.conn.commit()

    def update_user(self, uid, comment):
        self.cur.execute(f"UPDATE users SET comment={comment} WHERE userid={uid}")
        self.conn.commit()


class DatabaseGoodPeople:
    def __init__(self):
        self.conn = sqlite3.connect('./resources/databases/good_people.db')  # create database for tasks.
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
                            userid INT PRIMARY KEY, rating INT);""")
        self.conn.commit()

    def set_user(self, uid, rating):
        user = (uid, rating)
        self.cur.execute("INSERT INTO users(userid, rating) VALUES(?, ?);", user)
        self.conn.commit()

    def get_user(self, uid=None, rating=None) -> list:
        if rating is None and uid:  # если только id
            users = self.cur.execute(f"SELECT * FROM users WHERE userid={uid};").fetchall()  # берем юзера
        elif rating and uid is None:  # если только рейтинг
            users = self.cur.execute(
                f"SELECT * FROM users WHERE rating={rating};").fetchall()  # берем юзеров с рейтингом
        else:  # если нет ни айди ни рейтинга
            users = self.cur.execute("SELECT * FROM users;").fetchall()  # получаем список юзеров
        self.conn.commit()
        return users

    def update_user(self, uid, rating):
        self.cur.execute(f"UPDATE users SET rating={rating} WHERE userid={uid}")
        self.conn.commit()
