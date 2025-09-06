import mysql.connector
from mysql.connector import errorcode
import csv
import uuid
import os 
from dotenv import load_dotenv

load_dotenv()
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",        
            password=MYSQL_PASSWORD
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("ALX_prodev database is ready.")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    finally:
        cursor.close()


def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=MYSQL_PASSWORD,
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_table(connection):
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        age DECIMAL NOT NULL,
        INDEX (user_id)
    )
    """
    try:
        cursor.execute(create_table_query)
        print("Table user_data is ready.")
    except mysql.connector.Error as err:
        print(f"Failed creating table: {err}")
    finally:
        cursor.close()


def insert_data(connection, data):
    cursor = connection.cursor()
    insert_query = """
    INSERT IGNORE INTO user_data (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    """
    try:
        cursor.executemany(insert_query, data)
        connection.commit()
        print(f"{cursor.rowcount} rows inserted (or ignored if duplicate).")
    except mysql.connector.Error as err:
        print(f"Failed inserting data: {err}")
    finally:
        cursor.close()


def load_csv(filepath="user_data.csv"):
    rows = []
    with open(filepath, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append((
                str(uuid.uuid4()),  
                row["name"],
                row["email"],
                row["age"]
            ))
    return rows


def row_generator(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row
    cursor.close()

if __name__ == "__main__":
    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close()

    prodev_conn = connect_to_prodev()
    if prodev_conn:
        create_table(prodev_conn)

        data = load_csv("user_data.csv")
        insert_data(prodev_conn, data)

        print("\Printing rows from user_data:")
        for row in row_generator(prodev_conn):
            print(row)

        prodev_conn.close()
