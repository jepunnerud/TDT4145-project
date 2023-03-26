# The user should be able to register in the customer registry. This functionality should be programmed.

import sqlite3

con = sqlite3.connect("trainDB.db")
cursor = con.cursor()


def register_customer():

    # Register customer name and email
    name = input("Name: ")
    while not name:
        print("Name cannot be empty!")
        name = input("Name: ")

    email = input("Email: ")
    while not email:
        print("Email cannot be empty!")
        email = input("Email: ")

    # Register customer phone number. Makes sure the phone number is an integer and that it is unique
    cursor.execute("SELECT PhoneNo FROM Customer")
    phoneNos = cursor.fetchall()
    phoneNos = [str(phoneNo[0]) for phoneNo in phoneNos]
    phoneNo = input("Phone number: ")
    while phoneNo in phoneNos or not phoneNo or not phoneNo.isdigit():
        print("Phone number already registered!") if phoneNo in phoneNos else print(
            "Phone number cannot be empty, and it must be an integer!"
        )
        phoneNo = input("Phone number: ")

    # Check how many customers are already registered
    cursor.execute("SELECT COUNT(*) FROM Customer")
    count = cursor.fetchone()[0]

    # Ddd the new customer to the database
    cursor.execute(
        "INSERT INTO Customer VALUES (?, ?, ?, ?)",
        (count + 1, name, email, int(phoneNo)),
    )
    con.commit()
    print("Customer registered successfully!")
