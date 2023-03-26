import sqlite3
from datetime import datetime
from createTables import createTables
from fillExampleData import fillExampleData
from user_story_e import register_customer
from user_story_g import purchase_ticket
from user_story_h import get_orders
from user_story_h import get_tickets
from user_story_h import print_all_tickets

# write a program loop using the different python programs located in the src foulder
# the program should be able to do the following:


def loop():
    action = input("What would you like to do? (register/purchase/tickets/init): ")
    if action == "register":
        register_customer()
    elif action == "purchase":
        purchase_ticket()
    elif action == "tickets":
        orders = get_orders()
        print_all_tickets(orders)
    elif action == "init":
        createTables()
        fillExampleData()


loop()
