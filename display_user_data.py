from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

def display_user_data():
    try:
        mydb = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )

        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM user_data")
        rows = mycursor.fetchall()

        # Create a new window to display the data
        display_window = Toplevel()
        display_window.title("User Data")
        display_window.config(bg="white")

        # Create a Treeview widget to display the data
        tree = ttk.Treeview(display_window, columns=(
            "Min Days", "Max Days", "From Where", "Final Destination", "Max Stopovers", "Max Price"))
        tree.heading("Min Days", text="Min Days")
        tree.heading("Max Days", text="Max Days")
        tree.heading("From Where", text="From Where")
        tree.heading("Final Destination", text="Final Destination")
        tree.heading("Max Stopovers", text="Max Stopovers")
        tree.heading("Max Price", text="Max Price")

        for row in rows:
            tree.insert("", "end", text=row[0], values=(row[0], row[1], row[2], row[3], row[4], row[5]))

        tree.pack()

    except mysql.connector.Error as error:
        print("Error while fetching data from MySQL:", error)

    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
            print("Database connection closed.")


def display_messages_sent():
    messagebox.showinfo("Messages sent!", "Messages sent! All the information about cheap flights "
                                          "to the destinations you are interested in are sent via SMS.")


def failed_to_send_messages():
    messagebox.showinfo("No messages sent!", "Unfortunately there are some problems sending messages "
                                             "to the destinations you are interested in. Either you entered wrong "
                                             "data, or there are no flights meeting your requirements.")

