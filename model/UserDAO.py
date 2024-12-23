import pymysql
import sys
sys.path.append(sys.path[0]+'/security')
from security import sql
from security import config

class UserDAO:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = pymysql.connect(host=config.DATABASE['HOST'], user=config.DATABASE['USER'], passwd=config.DATABASE['PASSWORD'], db=config.DATABASE['DATABASE'], charset='utf8')
        self.cursor = self.conn.cursor()


    def signin(self, id, password):
        self.connect()
        vals = (id)
        self.cursor.execute(sql.signin_sql(), vals)
        row = self.cursor.fetchone()
        self.conn.close()
        if row is None:
            return False
        else:
            print(password)
            print(row)
            if row[0] == password:
                return True
            else:
                return False


    def signup(self, userid, password, email, name, age, phone):
        self.connect()
        print(password)
        vals = (userid, password, email, name, age, phone, 0)
        self.cursor.execute(sql.signup_sql(), vals)
        self.conn.commit()
        self.conn.close()

    def checkid(self, userid):
        self.connect()
        vals = userid
        self.cursor.execute(sql.check_id_sql(), vals)
        row = self.cursor.fetchone()
        if row is None:
            return False
        else:
            return True

    def checkEmail(self, eamil):
        self.connect()
        vals = eamil
        self.cursor.execute(sql.check_id_sql(), vals)
        row = self.cursor.fetchone()
        if row is None:
            return False
        else:
            return True

    def movie_save(self, movie_name, movie_path, movie_emotion):
        self.connect()
        vals = (movie_name, movie_path, movie_emotion)
        self.cursor.execute(sql.save_movie_sql(), vals)
        self.conn.commit()
        self.conn.close()

    def get_movie(self):
        self.connect()
        self.cursor.execute(sql.get_movie_sql())
        row = self.cursor.fetchall()
        print(row)

    def get_movie_path(self):
        self.connect()
        self.cursor.execute(sql.get_movie_path_sql())
        row = self.cursor.fetchall()
        return row