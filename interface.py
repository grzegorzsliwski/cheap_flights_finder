from tkinter import *
from tkinter import ttk
import mysql.connector
from search import search
from display_user_data import display_user_data



class Interface:
    def __init__(self):
        self.min_days = 0
        self.max_days = 0
        self.from_where = ""
        self.final_destination = ""
        self.max_stopovers = 0
        self.max_price = 0

    def save_to_database(self):
        global mydb, mycursor
        self.min_days = min_days_combobox.get()
        self.max_days = max_days_combobox.get()
        self.from_where = from_where_entry.get()
        self.final_destination = final_destination_entry.get()
        self.max_stopovers = max_stopovers_combobox.get()
        self.max_price = max_price_entry.get()

        try:
            mydb = mysql.connector.connect(
                host=os.getenv("MYSQL_HOST"),
                user=os.getenv("MYSQL_USER"),
                password=os.getenv("MYSQL_PASSWORD"),
                database=os.getenv("MYSQL_DATABASE")
            )

            mycursor = mydb.cursor()

            sql = ("INSERT INTO user_data (min_days, max_days, from_where, final_destination, max_stopovers, "
                   "max_price) VALUES (%s, %s, %s, %s, %s, %s)")
            values = (
                self.min_days, self.max_days, self.from_where, self.final_destination, self.max_stopovers,
                self.max_price)

            mycursor.execute(sql, values)

            mydb.commit()

            print("Data has been saved to the database.")

        except mysql.connector.Error as error:
            print("Error while inserting data into MySQL:", error)

        finally:
            if mydb.is_connected():
                mycursor.close()
                mydb.close()
                print("Database connection closed.")

    def create_interface(self):
        window = Tk()

        window.title("Cheap Flights Search")
        window.minsize(700, 700)
        window.config(padx=50, pady=50, bg='white')

        title_label = Label(text="Track Cheap Flights", font=("Arial", 24), bg='white', fg='black')
        title_label.grid(column=0, row=0, columnspan=3, padx=10, pady=10)

        min_days_label = Label(text="Minimal stay duration (days):", bg="white")
        min_days_label.grid(row=1, column=0)

        max_days_label = Label(text="Maximal stay duration (days):", bg="white")
        max_days_label.grid(row=2, column=0)

        from_where_label = Label(text="Departure city (in English):", bg="white")
        from_where_label.grid(row=3, column=0)

        final_destination_label = Label(text="Destination city (in English):", bg="white")
        final_destination_label.grid(row=4, column=0)

        max_stopovers_label = Label(text="Max stopovers (round trip):", bg="white")
        max_stopovers_label.grid(row=5, column=0)

        max_price_label = Label(text="Max price of interest (in PLN, e.g., 1000):", bg="white")
        max_price_label.grid(row=6, column=0)

        # Entries
        days = tuple(range(1, 31))
        global min_days_combobox
        min_days_combobox = ttk.Combobox(window, values=days)
        min_days_combobox.set("1")
        min_days_combobox.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

        global max_days_combobox
        max_days_combobox = ttk.Combobox(window, values=days)
        max_days_combobox.set("1")
        max_days_combobox.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

        global from_where_entry
        from_where_entry = Entry(window, width=21)
        from_where_entry.grid(row=3, column=1, padx=10, pady=10, columnspan=2)

        global final_destination_entry
        final_destination_entry = Entry(window, width=21)
        final_destination_entry.grid(row=4, column=1, padx=10, pady=10, columnspan=2)

        stopover_days = tuple(range(0, 7))
        global max_stopovers_combobox
        max_stopovers_combobox = ttk.Combobox(window, values=stopover_days)
        max_stopovers_combobox.set("0")
        max_stopovers_combobox.grid(row=5, column=1, columnspan=2, padx=10, pady=10)

        global max_price_entry
        max_price_entry = Entry(window, width=21)
        max_price_entry.grid(row=6, column=1, padx=10, pady=10, columnspan=2)

        # Buttons
        add_to_database_button = Button(window, text="Add to database", command=self.save_to_database)
        add_to_database_button.grid(row=7, column=0, columnspan=1, pady=10)

        display_button = Button(window, text="Display User Data", command=display_user_data)
        display_button.grid(row=7, column=1, columnspan=1, pady=10)

        search_button = Button(window, text="Search for flights", command=search)
        search_button.grid(row=7, column=2, columnspan=1, pady=10)
        window.mainloop()


# Create instance of Interface and start the GUI
interface = Interface()
interface.create_interface()


