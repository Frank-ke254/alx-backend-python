import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def stream_users():
    try:
        with mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("MYSQL_USER"),        
            password=os.getenv("MYSQL_PASSWORD")
        ) as connection:  
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM user_data")
                while True:
                    row = cursor.fetchone()
                    if row is None:
                        break
                    yield row
                    
    except Error as e:
        print(f"Error: {e}")
