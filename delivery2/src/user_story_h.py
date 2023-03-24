# retrieve information about all tickets purchased by a customer

import sqlite3

con = sqlite3.connect("trainDB.db")
cursor = con.cursor()


def get_customer():
    # Get customer id from phone number
    phoneNo = input("Phone number: ")
    while not phoneNo or not phoneNo.isdigit():
        print("Phone number cannot be empty, and it must be an integer!")
        phoneNo = input("Phone number: ")
    cursor.execute("SELECT CustomerNo FROM Customer WHERE PhoneNo = ?", (int(phoneNo),))
    customerID = cursor.fetchone()
    if not customerID:
        print("No customer found with phone number", phoneNo)
        return
    return customerID[0]


def get_purchases():
    # Get customer id. This uses the get_customer function, asking if the user wants to try again if no customer id is found from a certain phone number.
    customerID = get_customer()
    tryAgain = True
    while tryAgain:
        if not customerID:
            tryAgain = input("Try again? (y/n) ").lower() == "y"
            if tryAgain:
                customerID = get_customer()
        else:
            tryAgain = False

    # Get all customer orders by the customer with customerID
    cursor.execute(
        "SELECT * FROM CustomerOrder WHERE CustomerID = ?", (int(customerID),)
    )
    orders = cursor.fetchall()
    if not orders:
        print("No orders found for customer ID", customerID)
    else:
        print("Orders found for customer ID", customerID)
        for order in orders:
            print(order)

    # get all tickets purchased by the customer
    # cursor.execute(
    #     "SELECT * FROM Ticket WHERE CustomerID = ?", (int(customerID),)
    # )
    # tickets = cursor.fetchall()
    # if not tickets:
    #     print("No tickets found for customer ID", customerID)
    # else:
    #     print("Tickets found for customer ID", customerID)
    #     for ticket in tickets:
    #         print(ticket)
    print(customerID)


get_purchases()
con.close()
