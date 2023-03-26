import sqlite3
from datetime import datetime
from createTables import createTables
from fillExampleData import fillExampleData
from user_story_e import register_customer
from user_story_g import purchase_ticket
from user_story_h import get_orders
from user_story_h import get_tickets

# write a program loop using the different python programs located in the src foulder
# the program should be able to do the following:


def loop():
    purchase_ticket()


loop()
