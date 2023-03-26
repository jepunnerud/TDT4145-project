from constants import con

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


def get_orders():
    # Get customer id. This uses the get_customer function, asking if the user wants to try again if no customer id is found from a certain phone number.
    customerID = get_customer()
    tryAgain = True
    while tryAgain:
        if not customerID:
            tryAgain = input("Try again? (y/n) ").lower() == "y"
            if not tryAgain:
                return []
            customerID = get_customer()
        else:
            tryAgain = False

    # Get all customer orders by the customer with customerID
    cursor.execute(
        "SELECT OrderNo, orderDateTime FROM CustomerOrder WHERE CustomerID = ?",
        (int(customerID),),
    )
    orders = cursor.fetchall()
    if not orders:
        print("No orders found for customer ID", customerID)
        return []
    orders = [list(order) for order in orders]
    print(orders)
    return orders


def get_tickets(order):
    # Get all tickets for the order with orderID
    cursor.execute("SELECT * FROM SeatTicket WHERE OrderNo = ?", (order[0],))
    seat_tickets = cursor.fetchall()
    cursor.execute("SELECT * FROM BedTicket WHERE OrderNo = ?", (order[0],))
    bed_tickets = cursor.fetchall()
    if not (seat_tickets or bed_tickets):
        print("No tickets found for order ID", order[0])
        return []
    tickets = [list(ticket) for ticket in seat_tickets.extend(bed_tickets)]
    return tickets


def print_all_tickets():
    orders = get_orders()
    for order in orders:
        print("Order number:", order[0])
        print("Order date and time:", order[1])
        print("Tickets:")
        tickets = get_tickets(order)
        (print(ticket) for ticket in tickets)
        print()
