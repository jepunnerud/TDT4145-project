# Registered customers should be able to find available tickets for
# a desired train route and purchase the tickets they would like.
# This functionality should be programmed.
#
# Make sure to only sell available seats.

import sqlite3
from user_story_h import get_customer
from user_story_c import get_train_route
from datetime import datetime

con = sqlite3.connect("trainDB.db")
cursor = con.cursor()


def purchase_ticket():
    create_order = input("Do you want to place a new order? (yes/no): ")
    if create_order == "yes":
        customerID = get_customer()
        place_order = True
        date = input("Which date would you like to travel? (yyyy-mm-dd): ")
        if customerID:
            cursor.execute("SELECT COUNT(*) FROM CustomerOrder")
            OrderNo = cursor.fetchone()[0] + 1
            cursor.execute(
                "INSERT INTO CustomerOrder(OrderNo, CustomerID, orderDateTime) VALUES (?,?,?)",
                (
                    OrderNo,
                    customerID,
                    date,
                ),
            )
            con.commit()
            while place_order:
                ticket_type = input(
                    "Would you like to order a bed or a seat? (bed/seat): "
                )
                if ticket_type == "bed":
                    handle_bed_purchase(OrderNo, date)
                if ticket_type == "seat":
                    handle_seat_purchase(OrderNo, date)
                else:
                    print(
                        "Something went wrong. Make sure to type either 'seat' or 'bed'"
                    )
                    try_again = input("Would you like to try again?: (yes/no): ")
                    if try_again.lower() == "no":
                        place_order = False

                order_another = input("Would you like to order another?: (yes/no): ")
                if order_another.lower() == "no":
                    place_order = False


def find_available_seat(train_route, date):

    print(train_route)
    cursor.execute(
        """SELECT ChairCar.CarID, Seat.SeatNo FROM Seat
        LEFT JOIN ChairCar ON Seat.CarID = ChairCar.CarID
        LEFT JOIN CarInArrangement ON ChairCar.CarID = CarInArrangement.CarID
        LEFT JOIN TrainRoute ON TrainRoute.ArrangementID = CarInArrangement.ArrangementID
        LEFT JOIN TrainOccurence ON TrainOccurence.RouteID = TrainRoute.TrainRouteID
        WHERE TrainRoute.TrainRouteID = ? AND TrainOccurence.RouteDate = ? 
        AND NOT EXISTS (SELECT SeatTicket.SeatNo FROM SeatTicket """,
        (train_route, date),
    )
    seats = cursor.fetchall()

    cursor.execute(
        """SELECT SeatTicket.CarID, SeatTicket.SeatNo, SeatTicket.TicketStart, SeatTicket.TicketEnd FROM SeatTicket
                                    INNER JOIN CustomerOrder ON CustomerOrder.OrderNo = SeatTicket.OrderNo
                                    WHERE SeatTicket.OrderNo = CustomerOrder.OrderNo"""
    )
    occupied = cursor.fetchall()

    free_seats = []
    for seat in seats:
        if seat[0] * seat[1] != occupied[0] * occupied[1]:
            free_seats.append(seat)

    for seat in free_seats:
        print(f"Car number: {seat[0]} - Seat number: {seat[1]}")


def find_available_bed(train_route, date):

    available_beds = cursor.execute(
        """SELECT SleepingCar.CarID, Bed.CompartmentNo, Bed.BedNo FROM Bed
        LEFT JOIN SleepingCar ON Bed.CarID = SleepingCar.CarID
        LEFT JOIN CarInArrangement ON SleepingCar.CarID = CarInArrangement.CarID
        LEFT JOIN TrainRoute ON TrainRoute.ArrangementID = CarInArrangement.ArrangementID
        LEFT JOIN TrainOccurence ON TrainOccurence.RouteID = TrainRoute.TrainRouteID
        WHERE TrainRoute.TrainRouteID = ? AND TrainOccurence.RouteDate = ?""",
        (train_route, date),
    )

    available_beds = list(available_beds)
    for bed in available_beds:
        print(
            f"Ticket number: {available_beds.index(bed)} Car number: {bed[0]} Compartment {bed[1]} - Bed: {bed[2]}"
        )


def handle_seat_purchase(OrderNo, date):
    start = input("Where to where would you like to travel from? (Station): ")
    end = input("Where to where would you like to travel to? (Station): ")
    get_train_route(start, date_to_weekday(date))
    train_route = input("Which route would you like to travel on? (Route number): ")
    find_available_seat(int(train_route), date)
    seat_number = input("Which seat would you like to purchase? (Seat number): ")
    cursor.execute("SELECT COUNT(*) FROM SeatTicket")
    seat_ticketNo = cursor.fetchone()[0] + 1
    cursor.execute(
        """INSERT INTO SeatTicket VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            seat_ticketNo,
            OrderNo,
            start,
            end,
            train_route,
            date,
            int(seat_number),
        ),
    )
    con.commit()


def handle_bed_purchase(OrderNo, date):
    start_end = input("From where to where would you like to travel? (Start, End): ")
    start_end.split(",")
    start_end[1].strip()
    train_route = get_train_route(start_end[0], date_to_weekday(date))[0]
    find_available_bed(train_route, date)
    order = input("Would you like to purchase a bed ticket? (yes/no): ")
    if order.lower() == "yes":
        bed_number = input("Which bed would you like to purchase? (Bed number): ")
        cursor.execute("SELECT COUNT(*) FROM BedTicket")
        bed_ticketNo = cursor.fetchone()[0] + 1

        affirmation = input("Are you sure? (yes/no): ")
        if affirmation.lower() == "yes":
            cursor.execute(
                """ INSERT INTO Ticket (TicketNo, OrderNo, TicketStart, TicketEnd, TicketDate, BedNo)""",
                (
                    bed_ticketNo,
                    OrderNo,
                    start_end[0],
                    start_end[1],
                    date,
                    int(bed_number),
                ),
            )
            con.commit()


def date_to_weekday(date):
    weekdays = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    return weekdays[datetime.strptime(date, "%Y-%m-%d").weekday()]
