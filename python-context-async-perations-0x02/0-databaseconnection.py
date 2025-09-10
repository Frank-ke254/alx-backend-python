import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.host = os.getenv("MYSQL_HOST")
        self.user = os.getenv("MYSQL_USER")
        self.password = os.getenv("MYSQL_PASSWORD")
        self.database = os.getenv("MYSQL_NAME")
        self.conn = None

    def __enter__(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()
        return False  
      
with DatabaseConnection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
