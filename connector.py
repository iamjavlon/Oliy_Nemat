import sqlite3

with sqlite3.connect("oliynemat_db.sqlite3", check_same_thread=False) as connector:
    connector.commit()

cursor = connector.cursor()