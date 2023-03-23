# Registered customers should be able to find available tickets for a desired train route and purchase the tickets they would like.
# This functionality should be programmed. • Make sure to only sell available seats.

import sqlite3

con = sqlite3.connect("trainDB.db")
cursor = con.cursor()


def find_available_ticket(train_route):
    available_tickets = con.execute("SELECT")


def purchase_ticket(user, tickets):
    con.execute("INSERT")
