import sqlite3
from sqlite3 import Error

#create database


def sql_connection():
    try:
        con = sqlite3.connect('mydatabase.db')
        return con
    except Error:
        print(Error)


def sql_table(con):
    cursorObj = con.cursor()
    cursorObj.execute("""CREATE TABLE user_family
                    (id integer PRIMARY KEY, user_id text, next_payment text )
                """)

    con.commit()


# con = sql_connection()
# sql_table(con)


