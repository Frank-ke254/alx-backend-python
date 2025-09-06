import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def stream_users_in_batches(batch_size):
    connection = mysql.connector.connect(
      
        host=os.getenv("MYSQL_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("MYSQL_USER"),        
        password=os.getenv("MYSQL_PASSWORD")
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break

        yield batch
    cursor.close()
    connection.close()

def batch_processing(batch_size):
    for user_batch in stream_users_in_batches(batch_size):
        for user in user_batch:
            if user and user['age'] > 25:
                print(user)
