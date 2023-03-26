# Registered customers should be able to find available tickets for
# a desired train route and purchase the tickets they would like.
# This functionality should be programmed.
#
# Make sure to only sell available seats.

import sqlite3

con = sqlite3.connect("trainDB.db")
cursor = con.cursor()


def find_available_seat(train_route, date):

    available_seats = cursor.execute(
        """SELECT ChairCar.CarID, Seat.SeatNo FROM Seat
        LEFT JOIN ChairCar ON Seat.CarID = ChairCar.CarID
        LEFT JOIN CarInArrangement ON ChairCar.CarID = CarInArrangement.CarID
        LEFT JOIN TrainRoute ON TrainRoute.ArrangementID = CarInArrangement.ArrangementID
        LEFT JOIN TrainOccurence ON TrainOccurence.RouteID = TrainRoute.TrainRouteID
        WHERE TrainRoute.TrainRouteID = ? AND TrainOccurence.RouteDate = ?""",
        (train_route, date),
    )
    available_seats = list(available_seats)

    for seat in available_seats:
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
        print(f"Car number: {bed[0]} Compartment {bed[1]} - Bed: {bed[2]%2 + 1}")


find_available_seat(2, "2023-04-03")
find_available_bed(2, "2023-04-03")
con.close()
