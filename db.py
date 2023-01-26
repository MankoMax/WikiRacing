import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host=os.getenv('POSTGRES_HOST'),
            port=os.getenv('POSTGRES_PORT'),
            database=os.getenv('POSTGRES_DB')
        )
        self.cursor = self.conn.cursor()
        self.create_table()
        
    def __del__(self):
        return self.conn.close()
        
    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS wiki (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            parent_id INT NULL
            )""")
        self.conn.commit()
        
    def add_title(self, title, parent_id=None):
        self.cursor.execute("""INSERT INTO wiki (title, parent_id) VALUES (%s, %s)""", (title, parent_id))
        self.conn.commit()
        self.cursor.execute("""SELECT * FROM wiki WHERE title=%s AND parent_id=%s""", (title, parent_id))
        return self.cursor.fetchone()
        
    def get_title(self, title):
        self.cursor.execute("""SELECT * FROM wiki WHERE title=%s""", (title,))
        return self.cursor.fetchone()
    
    def get_children(self, parent_id):
        self.cursor.execute("""SELECT * FROM wiki WHERE parent_id='%s'""", (parent_id, ))
        return self.cursor.fetchall()
    
    def get_first_200(self):
        self.cursor.execute("""SELECT * FROM wiki LIMIT 200""")
        return self.cursor.fetchall()