import sqlite3
from datetime import datetime

con = sqlite3.connect("trainDB.db")
cursor = con.cursor()
