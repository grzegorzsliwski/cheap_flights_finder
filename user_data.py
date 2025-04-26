from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


def user_data_json():
    try:
        mydb = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        mycursor = mydb.cursor()
        print("Connected to the database.")

    except mysql.connector.Error as error:
        print("Error while connecting to MySQL:", error)

    else:
        if mydb.is_connected():
            mycursor.execute("SELECT * FROM user_data")
            rows = mycursor.fetchall()

            json_data = []
            for row in rows:
                data = {
                    "min_days": row[0],
                    "max_days": row[1],
                    "from_where": row[2],
                    "final_destination": row[3],
                    "max_stopovers": row[4],
                    "max_price": row[5]
                }
                json_data.append(data)

            mycursor.close()
            mydb.close()
            return json_data
