from constants import con
from user_story_h import get_customer
from user_story_c import get_train_route
from datetime import datetime

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
                finished = input("Do you want to order another? (yes/no): ")
                if finished == "no":
                    place_order = False


def find_available_seat(train_route, date, OrderNo, start, end):
    cursor.execute(
        """SELECT ChairCar.CarID, Seat.SeatNo FROM Seat
        LEFT JOIN ChairCar ON Seat.CarID = ChairCar.CarID
        LEFT JOIN CarInArrangement ON ChairCar.CarID = CarInArrangement.CarID
        LEFT JOIN TrainRoute ON TrainRoute.ArrangementID = CarInArrangement.ArrangementID
        LEFT JOIN TrainOccurence ON TrainOccurence.RouteID = TrainRoute.TrainRouteID
        WHERE TrainRoute.TrainRouteID = ? AND TrainOccurence.RouteDate = ?""",
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

    if len(occupied) > 0:
        for seat in seats:
            for o_seat in occupied:
                if seat[0] * seat[1] != o_seat[0] * o_seat[1]:
                    free_seats.append(seat)
    else:
        for seat in seats:
            free_seats.append(seat)

    for seat in free_seats:
        print(f"Car number: {seat[0]} - Seat number: {seat[1]}")

    car_number = input("Which car would you like? (Car number): ")
    seat_number = input("Which seat would you like to purchase? (Seat number): ")
    valid = True
    if len(occupied) > 0:
        for seat in occupied:
            if seat[0] == int(car_number) and seat[1] == int(seat_number):
                valid = False

    if valid:
        cursor.execute("SELECT COUNT(*) FROM SeatTicket")
        seat_ticketNo = cursor.fetchone()[0] + 1
        cursor.execute(
            """INSERT INTO SeatTicket VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                seat_ticketNo,
                OrderNo,
                start,
                end,
                train_route,
                date,
                int(car_number),
                int(seat_number),
            ),
        )
        con.commit()
        print(
            f"Ticket from {start} to {end} on {date} successfully ordered! Car: {car_number} Seat: {seat_number}"
        )
    else:
        print("This seat is occupied, please choose another")


def find_available_bed(train_route, date, OrderNo, start, end):
    cursor.execute(
        """SELECT SleepingCar.CarID, Bed.CompartmentNo, Bed.BedNo FROM Bed
        LEFT JOIN SleepingCar ON Bed.CarID = SleepingCar.CarID
        LEFT JOIN CarInArrangement ON SleepingCar.CarID = CarInArrangement.CarID
        LEFT JOIN TrainRoute ON TrainRoute.ArrangementID = CarInArrangement.ArrangementID
        LEFT JOIN TrainOccurence ON TrainOccurence.RouteID = TrainRoute.TrainRouteID
        WHERE TrainRoute.TrainRouteID = ? AND TrainOccurence.RouteDate = ?""",
        (train_route, date),
    )

    beds = cursor.fetchall()

    cursor.execute(
        """SELECT BedTicket.CarID, BedTicket.CompartmentNo, BedTicket.BedNo, BedTicket.TicketStart, BedTicket.TicketEnd, CustomerOrder.OrderNo FROM BedTicket
                                    INNER JOIN CustomerOrder ON CustomerOrder.OrderNo = BedTicket.OrderNo
                                    WHERE BedTicket.OrderNo = CustomerOrder.OrderNo"""
    )
    occupied = cursor.fetchall()

    free_beds = []

    if len(occupied) > 0:
        for bed in beds:
            for o_bed in occupied:
                if bed[0] * bed[1] != o_bed[0] * o_bed[1]:
                    free_beds.append(bed)
    else:
        for bed in beds:
            free_beds.append(bed)

    for bed in free_beds:
        print(
            f"Car number: {bed[0]} - compartment number: {bed[1]} - bed number: {bed[2]}"
        )

    car_number = input("Which car would you like? (Car number): ")
    compartment_number = input(
        "Which compartment would you like? (Compartment number): "
    )
    bed_number = input("Which bed would you like to purchase? (Bed number): ")
    valid = True
    if len(occupied) > 0:
        for bed in occupied:
            if bed[0] == int(car_number) and bed[1] == int(bed_number):
                valid = False

    if valid:
        cursor.execute("SELECT COUNT(*) FROM BedTicket")
        bed_ticketNo = cursor.fetchone()[0] + 1
        cursor.execute(
            """INSERT INTO BedTicket VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                bed_ticketNo,
                OrderNo,
                start,
                end,
                train_route,
                date,
                int(car_number),
                int(compartment_number),
                int(bed_number),
            ),
        )
        con.commit()
        print(
            f"Ticket from {start} to {end} on {date} successfully ordered! Car: {car_number} bed: {bed_number}"
        )
    else:
        print("This bed or compartment is occupied, please choose another")


def handle_seat_purchase(OrderNo, date):
    start = input("Where to where would you like to travel from? (Station): ")
    end = input("Where to where would you like to travel to? (Station): ")
    get_train_route(start, date_to_weekday(date))
    train_route = input("Which route would you like to travel on? (Route number): ")
    find_available_seat(int(train_route), date, OrderNo, start, end)


def handle_bed_purchase(OrderNo, date):
    start = input("Where to where would you like to travel from? (Station): ")
    end = input("Where to where would you like to travel to? (Station): ")
    get_train_route(start, date_to_weekday(date))
    train_route = input("Which route would you like to travel on? (Route number): ")
    find_available_bed(train_route, date, OrderNo, start, end)


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


def purchase_ticket(user, tickets):
    con.execute("INSERT")
