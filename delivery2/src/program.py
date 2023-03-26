import sqlite3
from datetime import datetime
from createTables import createTables
from fillExampleData import fillExampleData

# write a program loop using the different python programs located in the src foulder
# the program should be able to do the following:


def loop():
    createTables()
    fillExampleData()


loop()
