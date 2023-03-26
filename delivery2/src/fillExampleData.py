import sqlite3
import math
from constants import con


def fillExampleData():
    cursor = con.cursor()

    # Railway stations on Nordlandsbanen
    cursor.execute("INSERT INTO RailwayStation VALUES ('Trondheim', 5.1)")
    cursor.execute("INSERT INTO RailwayStation VALUES ('Steinkjer', 3.6)")
    cursor.execute("INSERT INTO RailwayStation VALUES ('Mosjøen', 6.8)")
    cursor.execute("INSERT INTO RailwayStation VALUES ('Mo i Rana', 3.5)")
    cursor.execute("INSERT INTO RailwayStation VALUES ('Fauske', 34.0)")
    cursor.execute("INSERT INTO RailwayStation VALUES ('Bodø', 4.1)")

    # Track sections on Nordlandsbanen
    cursor.execute(
        "INSERT INTO TrackSection VALUES (1, 'Trønderbanen', 0, 'Trondheim', 'Steinkjer')"
    )
    cursor.execute(
        "INSERT INTO TrackSection VALUES (2, 'Nordlandsbanen', 0, 'Trondheim', 'Bodø')"
    )
    cursor.execute(
        "INSERT INTO TrackSection VALUES (3, 'Nordlandsbanen', 0, 'Trondheim', 'Mo i Rana')"
    )

    # Subsections on Nordlandsbanen
    cursor.execute(
        "INSERT INTO Subsection VALUES (1, 120, 1, 'Trondheim', 'Steinkjer')"
    )
    cursor.execute("INSERT INTO Subsection VALUES (2, 280, 1, 'Steinkjer', 'Mosjøen')")
    cursor.execute("INSERT INTO Subsection VALUES (3, 90, 1, 'Mosjøen', 'Mo i Rana')")
    cursor.execute("INSERT INTO Subsection VALUES (4, 170, 1, 'Mo i Rana', 'Fauske')")
    cursor.execute("INSERT INTO Subsection VALUES (5, 60, 1, 'Fauske', 'Bodø')")

    # Subsections on TrackSections
    cursor.execute("INSERT INTO HasSubsection VALUES (1, 1, 0)")
    cursor.execute("INSERT INTO HasSubsection VALUES (2, 1, 0)")
    cursor.execute("INSERT INTO HasSubsection VALUES (2, 2, 1)")
    cursor.execute("INSERT INTO HasSubsection VALUES (2, 3, 2)")
    cursor.execute("INSERT INTO HasSubsection VALUES (2, 4, 3)")
    cursor.execute("INSERT INTO HasSubsection VALUES (2, 5, 4)")
    cursor.execute("INSERT INTO HasSubsection VALUES (3, 1, 0)")
    cursor.execute("INSERT INTO HasSubsection VALUES (3, 2, 1)")
    cursor.execute("INSERT INTO HasSubsection VALUES (3, 3, 2)")

    # Train Operators
    cursor.execute("INSERT INTO Operator VALUES (1, 'SJ Nord', 2 )")

    # Cars
    cursor.execute("INSERT INTO Car VALUES (1)")
    cursor.execute("INSERT INTO Car VALUES (2)")
    cursor.execute("INSERT INTO Car VALUES (3)")
    cursor.execute("INSERT INTO Car VALUES (4)")
    cursor.execute("INSERT INTO Car VALUES (5)")

    # Chair Cars
    for i in range(1, 5):
        cursor.execute(f"INSERT INTO ChairCar VALUES ({i}, 1, 3, 4)")

    # Sleeping Cars
    cursor.execute("INSERT INTO SleepingCar VALUES (5, 1, 4)")

    # Car Arrangements
    for i in range(1, 4):
        cursor.execute(f"INSERT INTO CarArrangement VALUES ({i})")

    # Cars in CarArrangement
    cursor.execute("INSERT INTO CarInArrangement VALUES (1, 1)")
    cursor.execute("INSERT INTO CarInArrangement VALUES (1, 2)")
    cursor.execute("INSERT INTO CarInArrangement VALUES (2, 3)")
    cursor.execute("INSERT INTO CarInArrangement VALUES (2, 5)")
    cursor.execute("INSERT INTO CarInArrangement VALUES (3, 4)")

    # Seats
    for i in range(1, 5):
        for j in range(1, 13):
            cursor.execute(f"INSERT INTO Seat VALUES ({i}, {j})")

    # Beds
    for i in range(1, 9):
        cursor.execute(f"INSERT INTO Bed VALUES (5, {math.ceil(i/2)}, {i})")

    # Train Routes
    cursor.execute("INSERT INTO TrainRoute VALUES (1, 0, 1, 2, 1)")
    cursor.execute("INSERT INTO TrainRoute VALUES (2, 0, 1, 2, 2)")
    cursor.execute("INSERT INTO TrainRoute VALUES (3, 1, 1, 3, 3)")

    # Train Occurences
    cursor.execute("INSERT INTO TrainOccurence VALUES (1, '2023-04-03')")
    cursor.execute("INSERT INTO TrainOccurence VALUES (2, '2023-04-03')")
    cursor.execute("INSERT INTO TrainOccurence VALUES (3, '2023-04-03')")
    cursor.execute("INSERT INTO TrainOccurence VALUES (1, '2023-04-04')")
    cursor.execute("INSERT INTO TrainOccurence VALUES (3, '2023-04-04')")

    # Route Timetable
    cursor.execute("INSERT INTO RouteTimetable VALUES (1, 'Trondheim', '07:49')")
    cursor.execute("INSERT INTO RouteTimetable VALUES (1, 'Steinkjer', '09:51')")
    cursor.execute("INSERT INTO RouteTimetable VALUES (1, 'Mosjøen', '13:20')")
    cursor.execute("INSERT INTO RouteTimetable VALUES (1, 'Mo i Rana', '14:31')")
    cursor.execute("INSERT INTO RouteTimetable VALUES (1, 'Fauske', '16:49')")
    cursor.execute("INSERT INTO RouteTimetable VALUES (1, 'Bodø', '17:34')")
    cursor.execute("INSERT INTO RouteTimetable VALUES (2, 'Trondheim', '23:05')")
    cursor.execute("INSERT INTO RouteTimetable VALUES (2, 'Steinkjer', '00:57')")
    cursor.execute("INSERT INTO RouteTimetable VALUES (2, 'Mosjøen', '04:41')")
    cursor.execute("INSERT INTO RouteTimetable VALUES (2, 'Mo i Rana', '05:53')")
    cursor.execute("INSERT INTO RouteTimetable VALUES (2, 'Fauske', '08:19')")
    cursor.execute("INSERT INTO RouteTimetable VALUES (2, 'Bodø', '09:05')")
    cursor.execute("INSERT INTO RouteTimetable VALUES (3, 'Mo i Rana', '08:11')")
    cursor.execute("INSERT INTO RouteTimetable VALUES (3, 'Mosjøen', '09:14')")
    cursor.execute("INSERT INTO RouteTimetable VALUES (3, 'Steinkjer', '12:31')")
    cursor.execute("INSERT INTO RouteTimetable VALUES (3, 'Trondheim', '14:13')")

    con.commit()
