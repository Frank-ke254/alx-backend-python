import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def stream_users():
    try:
        with mysql.connector.connect(
            host=MYSQL_HOST,
            database=DB_NAME,
            user=MYSQL_USER,        
            password=MYSQL_PASSWORD
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
