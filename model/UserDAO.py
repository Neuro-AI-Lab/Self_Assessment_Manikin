import pymysql
import sys
sys.path.append(sys.path[0]+'/security')
from security import sql
from security import config
from random import shuffle

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
            if row[0] == password:
                return True
            else:
                return False


    def signup(self, userid, password, email, name, age, phone):
        self.connect()
        vals = (userid, password, email, name, age, phone, 0)
        self.cursor.execute(sql.signup_sql(), vals)
        self.conn.commit()
        self.conn.close()

    def checkid(self, userid):
        self.connect()
        vals = userid
        self.cursor.execute(sql.check_id_sql(), vals)
        row = self.cursor.fetchone()
        self.conn.close()
        if row is None:
            return False
        else:
            return True

    def checkEmail(self, eamil):
        self.connect()
        vals = eamil
        self.cursor.execute(sql.check_id_sql(), vals)
        row = self.cursor.fetchone()
        self.conn.close()
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
        self.conn.close()
        return row

    def get_movie_path(self):
        self.connect()
        self.cursor.execute(sql.get_movie_path_sql())
        row = self.cursor.fetchall()
        self.conn.close()
        return row

    def get_movie_path_without_success(self, userid):
        self.connect()
        vals = userid
        self.cursor.execute(sql.get_user_success_movie_sql(), vals)
        row_success = list(self.cursor.fetchall())
        self.conn.close()
        row_all = list(self.get_movie())
        remove_path = []
        for all_name in row_all:
            for success_name in row_success:
                if all_name[0] == success_name[0]:
                    remove_path.append(all_name)
        path = list(set(row_all) - set(remove_path))
        success_len = len(row_success)
        final_path = []
        final_video_name = []
        for name in path:
            final_path.append(name[1])
            final_video_name.append(name[0])
        shuffle(final_path)
        return final_path, final_video_name, success_len

    def save_movie_assessment(self, assessment_id, userid, movie_name, valance, arousal, dominance, liking, familiarity, emotion):
        self.connect()
        vals = (assessment_id, userid, movie_name, valance, arousal, dominance, liking, familiarity, emotion)
        self.cursor.execute(sql.save_movie_assessment_sql(), vals)
        self.conn.commit()
        self.conn.close()