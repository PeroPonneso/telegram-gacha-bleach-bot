from dataclasses import asdict
from datetime import datetime
from sqlite3 import Error
import db

#region account CRUD

#id INTEGER PRIMARY KEY,
#0 is_bot BOOL DEFAULT "False",
#1 first_name VARCHAR(50) NOT NULL,
#2 last_name VARCHAR(50),
#3 username VARCHAR(50),
#4 language_code VARCHAR(50),
#5 created_on DATE;

def count_account():
    conn =  db.connect('ro')
    cursor =  conn.cursor()
    sql_command = f"SELECT COUNT(1) FROM account;"
    rows = cursor.execute(sql_command).fetchall()
    conn.close()
    if rows:
        results = rows[0]
        return results
    return 0

def exist_account(id):
    conn =  db.connect('ro')
    cursor =  conn.cursor()
    sql_command = f"SELECT COUNT(1) FROM account WHERE id = '{id}';"
    rows = cursor.execute(sql_command).fetchone()
    conn.close()
    if rows[0]:
        print("account esistente")
        return 1
    print("account non esistente")
    return 0

def create_account(id,bot,first_name,last_name,username,lang):
    is_signed_up = exist_account(id)
    print("is signed up?",is_signed_up)
    if is_signed_up:
        return 0
    conn =  db.connect('rw')
    cursor =  conn.cursor()
    created_on = datetime.now()
    sql_command = f"INSERT INTO account ('id','is_bot','first_name','last_name','username','language_code','created_on')\
                    VALUES ({id},{bot},'{first_name}','{last_name}','{username}','{lang}','{created_on}');"
    cursor.execute(sql_command)
    # To save the changes in the files. Never skip this.
    # If we skip this, nothing will be saved in the database.
    conn.commit()
    # close the connection
    conn.close()
    print("account registrato")
    return 1

def read_account(id):
    conn =  db.connect('ro')
    cursor =  conn.cursor()
    if exist_account(id):
        sql_command = f"SELECT A.id,A.is_bot,A.first_name,A.last_name,A.username,A.language_code,A.normal_tickets,A.created_on\
                        FROM account A \
                        WHERE id = '{id}';"
        rows = cursor.execute(sql_command).fetchall()
        conn.close()
        rows = rows[0]
        results = f'Il tuo profilo:\nId: \t\t\t{rows[0]}\nFirst: {rows[2]}\nLast: {rows[3]}\nUser: {rows[4]}\nLang: {rows[5]}\nTickets: {rows[6]}\nCreated: {rows[7][:16]}'
        return results
    return 0
#TODO update account

def update_account(id,data):
    pass

def add_ticket(id_account, n):
    conn =  db.connect('rw')
    cursor =  conn.cursor()
    #verifico che esista
    sql_command = f"UPDATE account\
                    SET normal_tickets = normal_tickets + {n}\
                    WHERE id={id_account}"
    cursor.execute(sql_command)
    conn.commit()
    conn.close()
    print("biglietto/i aggiunto/i")
    return 1

def add_tickets(n):
    conn =  db.connect('rw')
    cursor =  conn.cursor()
    #verifico che esista
    sql_command = f"UPDATE account\
                    SET normal_tickets = normal_tickets + {n}"
    cursor.execute(sql_command)
    conn.commit()
    conn.close()
    print("biglietto/i aggiunto/i per tutti")
    return 1

def read_ticket(id_account):
    conn =  db.connect('rw')
    cursor =  conn.cursor()
    #verifico che esista
    sql_command = f"SELECT normal_tickets\
                    FROM account\
                    WHERE id={id_account}"
    rows = cursor.execute(sql_command).fetchall()
    conn.close()
    return rows[0][0]

def delete_account(id):
    conn =  db.connect('rw')
    cursor =  conn.cursor()
    if exist_account(id):
        sql_command = f"DELETE FROM account WHERE id = '{id}'"
        cursor.execute(sql_command)
        conn.commit()
        conn.close()
        exist_account(id)
        return 1
    return 0
#endregion
