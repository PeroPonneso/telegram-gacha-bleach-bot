from dataclasses import asdict
import sqlite3
from sqlite3 import Error
import constants as keys

#region DB
#Connect to existing DB: connection if connected, 0 if error
#options: readonly ro, read/write rw,
def connect(options):
    connection = None
    try:
        connection = sqlite3.connect('file:' + keys.DB_PATH + '?mode=' + options, uri=True)
    except Error as e:
        print(f"The error '{e}' occurred")
        return 0

    return connection

#Generate a new DB: True if created, False if not Created
def generate():
    connection = connect('ro')
    if connection:
        print("Database already existing")
        connection.close()
        return 0
    try:
        connection = connect('rwc')
        #cursor
        cursor = connection.cursor()
        #create tables
        create_account_table(cursor)
        create_card_table(cursor)
        create_pack_table(cursor)
        create_accountXcard_table(cursor)
        connection.close()
    except Error as e:
        print(f"The error '{e}' occurred")
        if connection: connection.close()
    return 1
#endregion

#region Tables CREATION
def create_account_table(cursor):
    query = """CREATE TABLE account ( 
                    id INTEGER PRIMARY KEY,
                    is_bot BOOL DEFAULT "False",
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50),
                    username VARCHAR(50),
                    language_code VARCHAR(50),
                    normal_tickets INTEGER DEFAULT 0,
                    created_on DATE);"""
    # execute the statement
    cursor.execute(query)

def create_card_table(cursor):
    query = """CREATE TABLE card ( 
                    id INTEGER PRIMARY KEY,
                    rarity INTEGER NOT NULL,
                    name VARCHAR(100),
                    art_path VARCHAR(100),
                    art_name VARCHAR(100),
                    id_pack INTEGER NOT NULL,
                    created_on DATE);"""
    # execute the statement
    cursor.execute(query)

def create_pack_table(cursor):
    query = """CREATE TABLE pack ( 
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(100),
                    created_on DATE,
                    start_on DATE,
                    end_on DATE);"""
    # execute the statement
    cursor.execute(query)

#account+card primary key composta
def create_accountXcard_table(cursor):
    query = """CREATE TABLE account_card ( 
                    id INTEGER PRIMARY KEY,
                    amount INTEGER DEFAULT 0,
                    created_on DATE,
                    modified_on DATE,
                    id_account INTEGER NOT NULL,
                    id_card INTEGER NOT NULL);"""
    # execute the statement
    cursor.execute(query)

#endregion
