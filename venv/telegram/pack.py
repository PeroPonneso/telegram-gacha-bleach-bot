from dataclasses import asdict
from datetime import datetime
from sqlite3 import Error
import db

#region account CRUD

'''id INTEGER PRIMARY KEY,
                    name VARCHAR(100),
                    created_on DATE,
                    start_on DATE,
                    end_on DATE);
'''

def count():
    conn =  db.connect('ro')
    cursor =  conn.cursor()
    sql_command = f"SELECT COUNT(1) FROM pack;"
    rows = cursor.execute(sql_command).fetchall()
    conn.close()
    if rows:
        results = rows[0]
        return results
    return 0

def exist(id):
    conn =  db.connect('ro')
    cursor =  conn.cursor()
    sql_command = f"SELECT COUNT(1) FROM pack WHERE id = '{id}';"
    rows = cursor.execute(sql_command).fetchone()
    conn.close()
    if rows[0]:
        print("pack esistente")
        return 1
    print("pack non esistente")
    return 0

def create(name,start_on,end_on):
    conn =  db.connect('rw')
    cursor =  conn.cursor()
    created_on = datetime.now()
    sql_command = f"INSERT INTO pack (name,created_on,start_on,end_on) \
                    VALUES ({name},{created_on},{start_on},{end_on}');"
    cursor.execute(sql_command)
    # To save the changes in the files. Never skip this.
    # If we skip this, nothing will be saved in the database.
    conn.commit()
    # close the connection
    conn.close()
    print("pack creato")
    return 1

def read_by_id(id):
    conn =  db.connect('ro')
    cursor =  conn.cursor()
    if exist(id):
        sql_command = f"SELECT id,name,created_on,start_on,end_on \
                        FROM pack WHERE id = '{id}';"
        rows = cursor.execute(sql_command).fetchall()
        conn.close()
        row = rows[0]
        results = f'Il pack:\nid {row[0]}\nname {row[1]}\ncreated_on {row[2]}\nstart_on {row[3]}\nend_on {row[4]}\n'
        return results
    return 0

def read_by_name(name):
    conn =  db.connect('ro')
    cursor =  conn.cursor()
    if exist(id):
        sql_command = f"SELECT id,name,created_on,start_on,end_on \
                        FROM pack WHERE name = '{name}';"
        rows = cursor.execute(sql_command).fetchall()
        conn.close()
        row = rows[0]
        results = f'Il pack:\nid {row[0]}\nname {row[1]}\ncreated_on {row[2]}\nstart_on {row[3]}\nend_on {row[4]}\n'
        return results
    return 0
#TODO update pack
def update(id,data):
    conn =  db.connect('rw')
    cursor =  conn.cursor()
    sql_command = f""
    cursor.execute(sql_command)
    conn.commit()
    conn.close()
    return "Card updated"

def delete(id):
    conn =  db.connect('rw')
    cursor =  conn.cursor()
    if exist(id):
        sql_command = f"DELETE FROM pack WHERE id = '{id}'"
        cursor.execute(sql_command)
        conn.commit()
        conn.close()
        exist(id)
        return 1
    return 0
#TODO add card to pack from pack?
def add_card(*args):
    if len(args) == 1 and isinstance(args[0], int):
        # add_by_id
        pass
    elif len(args) == 2 and isinstance(args[0], str):
        # add_by_name 
        pass
    else:
        return 0

#endregion
