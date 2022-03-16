from dataclasses import asdict
from datetime import datetime
from sqlite3 import Error
import db

#region account CRUD

#0 id INTEGER PRIMARY KEY,
#1 rarity INTEGER NOT NULL,
#2 name VARCHAR(100),
#3 art_path VARCHAR(100),
#4 art_name VARCHAR(100),
#5 created_on DATE,
#6 id_pack INTEGER NOT NULL

def count():
    conn =  db.connect('ro')
    cursor =  conn.cursor()
    sql_command = f"SELECT COUNT(1) FROM card;"
    rows = cursor.execute(sql_command).fetchall()
    conn.close()
    if rows:
        results = rows[0]
        return results[0]
    return 0

def exist(id):
    conn =  db.connect('ro')
    cursor =  conn.cursor()
    sql_command = f"SELECT COUNT(1) FROM card WHERE id = '{id}';"
    rows = cursor.execute(sql_command).fetchone()
    conn.close()
    if rows[0]:
        print("exist: carta esistente")
        return 1
    print("exist: carta non esistente")
    return 0

def create(data):
    is_present = exist(data[0])
    print("create: is present?",is_present)
    if is_present:
        return 0
    conn =  db.connect('rw')
    cursor =  conn.cursor()
    created_on = datetime.now()
    sql_command = f"INSERT INTO card (rarity,name,art_name,id_pack,created_on) VALUES ({data[0]},{data[1]},'{data[2]}','{data[3]}','{created_on}');"
    cursor.execute(sql_command)
    # To save the changes in the files. Never skip this.
    # If we skip this, nothing will be saved in the database.
    conn.commit()
    # close the connection
    conn.close()
    print("create: carta inserita")
    return 1

def read_by_id(id):
    conn =  db.connect('ro')
    cursor =  conn.cursor()
    if exist(id):
        sql_command = f"SELECT * FROM card WHERE id = '{id}';"
        rows = cursor.execute(sql_command).fetchall()
        conn.close()
        row = rows[0]
        results = f'La tua carta:\nid {row[0]}\nrarity {row[1]}\nname {row[2]}\nart_parth {row[3]}\nart_name {row[4]}\nid_pack {row[5]}\ncreated_on {row[6]}'
        return rows
    return 0

def read_by_name(name):
    conn =  db.connect('ro')
    cursor =  conn.cursor()
    if exist(id):
        sql_command = f"SELECT * FROM card WHERE name = '{name}';"
        rows = cursor.execute(sql_command).fetchall()
        conn.close()
        results = []
        for row in rows:
            results.append(f'La tua carta:\nid {row[0]}\nrarity {row[1]}\nname {row[2]}\nart_parth {row[3]}\nart_name {row[4]}\nid_pack {row[5]}\ncreated_on {row[6]}\n')
        return rows
    return 0

def read_full_path(id):
    conn =  db.connect('ro')
    cursor =  conn.cursor()
    if exist(id):
        sql_command = f"SELECT art_path,art_name FROM card WHERE id = '{id}';"
        rows = cursor.execute(sql_command).fetchall()
        conn.close()
        row = rows[0]
        results = f'{row[0]}/{row[1]}'
        return results
    return 0

def read_name(id):
    conn =  db.connect('ro')
    cursor =  conn.cursor()
    if exist(id):
        sql_command = f"SELECT name FROM card WHERE id = '{id}';"
        rows = cursor.execute(sql_command).fetchall()
        conn.close()
        row = rows[0]
        results = f'{row[0]}'
        return results
    return 0

def read_by_rarity(star):
    conn =  db.connect('ro')
    cursor =  conn.cursor()
    
    sql_command = f"SELECT id FROM card WHERE rarity = '{star}';"
    rows = cursor.execute(sql_command).fetchall()
    result = []
    for elt in rows:
        result.append(elt[0])
    conn.close()
    print(f"read by rarity: SELECT id FROM card WHERE rarity = '{star}';\
             {result}")
    return result

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
        sql_command = f"DELETE FROM card WHERE id = '{id}'"
        cursor.execute(sql_command)
        conn.commit()
        conn.close()
        exist(id)
        return 1
    return 0
#endregion
