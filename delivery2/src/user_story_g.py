# Registered customers should be able to find available tickets for
# a desired train route and purchase the tickets they would like.
# This functionality should be programmed.
#
# Make sure to only sell available seats.

import sqlite3
from constants import con

cursor = con.cursor()


def find_available_ticket(train_route):

    available_tickets = []

    available_seat_tickets = cursor.execute(
        """SELECT TicketNo, TicketStart, TicketEnd FROM SeatTicket 
            WHERE NOT EXISTS (SELECT OrderNo FROM CustomerOrder 
            WHERE CustomerOrder.OrderNo = SeatTicket.OrderNo)"""
    )

    available_bed_tickets = con.execute(
        """SELECT TicketNo, TicketStart, TicketEnd FROM BedTicket 
            WHERE NOT EXISTS (SELECT OrderNo FROM CustomerOrder 
            WHERE CustomerOrder.OrderNo = BedTicket.OrderNo)"""
    )

    for ticket in available_seat_tickets:
        list_ticket = list(ticket)
        list_ticket.insert(0, "seat")
        available_tickets.append(list_ticket)

    for ticket in available_bed_tickets:
        list_ticket = list(ticket)
        list_ticket.insert(0, "bed")
        available_tickets.append(list_ticket)

    print(available_tickets)


def purchase_ticket(user, tickets):
    con.execute("INSERT")
