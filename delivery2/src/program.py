import sqlite3
from datetime import datetime
from createTables import createTables
from fillExampleData import fillExampleData
from user_story_c import get_train_route
from user_story_e import register_customer
from user_story_h import print_all_tickets
from constants import con

# write a program loop using the different python programs located in the src foulder
# the program should be able to do the following:


def user_story_c():
    station = input("Train station: ")
    weekday = input("Weekday: ")
    get_train_route(station, weekday)


def user_story_d():
    return


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
            "[1] Show all train routes that stop on a given station on a given weekday"
        )
        print(
            "[2] Search for train routes going between a starting station and an ending station based on date and time"
        )
        print("[3] Register as a customer")
        print("[4] Book a train ticket")
        print("[5] Show all train tickets booked by a given customer")
        print("[6] Quit")
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
