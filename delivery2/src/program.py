from datetime import datetime
from createTables import createTables
from fillExampleData import fillExampleData
from user_story_c import get_train_route
from user_story_d import get_train_route_between_two_stations
from user_story_e import register_customer
from user_story_h import print_all_tickets
from re import search
from constants import con


def user_story_c():
    station = input("Train station: ")
    weekday = input("Weekday: ")
    get_train_route(station, weekday)


def user_story_d():
    valid_stations = [
        "Trondheim",
        "Steinkjer",
        "Mosjøen",
        "Mo i Rana",
        "Fauske",
        "Bodø",
    ]

    station_1 = input("Starting station: ")
    while station_1 not in valid_stations:
        station_1 = input("Please enter a valid station or [q]uit: ")
        if station_1 == "q":
            return

    station_2 = input("Ending station: ")
    while station_2 not in valid_stations:
        station_2 = input("Please enter a valid station or [q]uit: ")
        if station_2 == "q":
            return

    date = input("What date? (YYYY-MM-DD): ")
    match = search("^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$", date)
    while match is None:
        date = input("Please enter a valid date (YYYY-MM-DD): ")
        match = search("^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$", date)

    time = input("What time? (HH:MM): ")
    match = search("^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$", time)
    while match is None:
        time = input("Please enter a valid time (HH:MM): ")
        match = search("^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$", time)

    get_train_route_between_two_stations(station_1, station_2, date, time)


def user_story_e():
    register_customer()


def user_story_g():
    return


def user_story_h():
    print_all_tickets()


def loop():
    createTables()
    try:
        fillExampleData()
    except:
        pass
    print("Welcome to this train system!")
    while True:
        print(
            """[1] Show all train routes that stop on a given station on a given weekday
[2] Search for train routes going between a starting station and an ending station based on date and time
[3] Register as a customer
[4] Book a train ticket
[5] Show all train tickets booked by a given customer
[6] Quit
            """
        )
        answer = input("Please choose one of the options above: ")
        print()
        if answer == "1":
            user_story_c()
        elif answer == "2":
            user_story_d()
        elif answer == "3":
            user_story_e()
        elif answer == "4":
            user_story_g()
        elif answer == "5":
            user_story_h()
        elif answer == "6":
            con.close()
            print("Goodbye!")
            return
        again = input("Do you wish to use another functionality of the system? (y/n): ")
        print()
        while again != "y" and again != "n":
            print("Please answer [y]es or [n]o")
            again = input(
                "Do you wish to use another functionality of the system? (y/n): "
            )
        if again == "n":
            con.close()
            print("Goodbye!")
            return


loop()
