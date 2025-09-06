#!/usr/bin/env python3

import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def stream_user_ages():
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
    )
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:   
        yield age

    cursor.close()
    conn.close()

def calculate_average_age():
    total_age = 0
    count = 0

    for age in stream_user_ages():  
        total_age += age
        count += 1

    average = total_age / count if count else 0
    print(f"Average age of users: {average:.2f}")


if __name__ == "__main__":
    calculate_average_age()
