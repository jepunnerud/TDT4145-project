# The user should be able to register in the customer registry. This functionality should be programmed.

import sqlite3

con = sqlite3.connect("trainDB.db")
cursor = con.cursor()


def register_customer():

    # register customer name, email and phone number
    name = input("Name: ")
    while not name:
        print("Name cannot be empty!")
        name = input("Name: ")

    email = input("Email: ")
    while not email:
        print("Email cannot be empty!")
        email = input("Email: ")

    phoneNo = input("Phone number: ")
    while not phoneNo:
        print("Phone number cannot be empty!")
        phoneNo = input("Phone number: ")

    # check how many customers are already registered
    cursor.execute("SELECT COUNT(*) FROM Customer")
    count = cursor.fetchone()[0]
    # add the new customer to the database
    cursor.execute(
        "INSERT INTO Customer VALUES (?, ?, ?, ?)", (count + 1, name, email, phoneNo)
    )
    con.commit()
    print("Customer registered successfully!")


register_customer()
con.close()
