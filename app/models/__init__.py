import psycopg2
import os


configs = {
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_DATABASE'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

class DatabaseConnect:
    @classmethod
    def get_conn_cur(cls):
        cls.conn = psycopg2.connect(**configs)
        cls.cur = cls.conn.cursor()
        
    @classmethod
    def commit_and_close(cls, commit = False):
        if commit:
            cls.conn.commit()
        cls.cur.close()
        cls.conn.close()