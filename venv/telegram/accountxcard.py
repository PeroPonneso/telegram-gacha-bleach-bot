from dataclasses import asdict
from datetime import datetime
from sqlite3 import Error
import db, account

#region account CRUD

'''def create_accountXcard_table(cursor):
    query = """CREATE TABLE account_card ( 
                    id INTEGER PRIMARY KEY,
                    amount INTEGER DEFAULT 0,
                    created_on DATE,
                    modified_on DATE,
                    id_account INTEGER NOT NULL,
                    id_card INTEGER NOT NULL);"""
    # execute the statement'''

def count():
    conn =  db.connect('ro')
    cursor =  conn.cursor()
    sql_command = f"SELECT COUNT(1) FROM account_card;"
    rows = cursor.execute(sql_command).fetchall()
    conn.close()
    if rows:
        results = rows[0]
        return results
    return 0

def exist(id):
    conn =  db.connect('ro')
    cursor =  conn.cursor()
    sql_command = f"SELECT COUNT(1) FROM account_card WHERE id = '{id}';"
    rows = cursor.execute(sql_command).fetchone()
    conn.close()
    if rows[0]:
        print("exist: associazione esistente")
        return 1
    print("exist: associazione non esistente")
    return 0

def read_all_id(id):
    conn =  db.connect('ro')
    cursor =  conn.cursor()
    if account.exist_account(id):
        sql_command = f"SELECT id_card \
                        FROM account_card \
                        WHERE id_account = '{id}'"
        rows = cursor.execute(sql_command).fetchall()
        conn.close()
        results = []
        for row in rows:
            results.append(row[0])
        print(f"reading all id's {rows},{results}")
        return results
    return 0

def create(id_card, id_account):
    conn =  db.connect('rw')
    cursor =  conn.cursor()
    created_on = datetime.now()
    #verifico che esista
    sql_command = f"SELECT COUNT(1)\
                    FROM account_card\
                    WHERE id_account={id_account} AND id_card={id_card}"
    present = cursor.execute(sql_command).fetchall()
    if present[0][0]:
        sql_command = f"UPDATE account_card\
                        SET amount = amount + 1\
                        WHERE id_account={id_account} AND id_card={id_card}"
        cursor.execute(sql_command)
        # To save the changes in the files. Never skip this.
        # If we skip this, nothing will be saved in the database.
        conn.commit()
        # close the connection
        conn.close()
        print("carta inserita")
        return 1
    else:
        sql_command = f"INSERT INTO account_card (amount,created_on,modified_on,id_account,id_card) \
                        VALUES (1,'{created_on}','{created_on}',{id_account}, {id_card});"
        cursor.execute(sql_command)
        # To save the changes in the files. Never skip this.
        # If we skip this, nothing will be saved in the database.
        conn.commit()
        # close the connection
        conn.close()
        print("carta inserita")
        return 1

def read_from_account(account_id):
    conn =  db.connect('ro')
    cursor =  conn.cursor()
    if account.exist_account(account_id):
        sql_command = f"SELECT X.id,X.amount,X.created_on,X.modified_on,C.name,C.rarity,C.art_name \
                        FROM account_card X \
                        JOIN card C ON X.id_card = C.id \
                        WHERE X.id_account = {account_id};"
        rows = cursor.execute(sql_command).fetchall()
        print("read from account id: ---> - {account_id} - {rows}")
        results = []
        for row in rows:
            results.append(f'Collezione:\nid {row[0]}\namount of cards {row[1]}\ncreated_on {row[2]}\nmodified_on {row[3]}\ncard name {row[4]}\nart file {row[5]}')
        return results
    return 0

def read_amount(account_id,card_id):
    conn =  db.connect('ro')
    cursor =  conn.cursor()
    if account.exist_account(account_id):
        sql_command = f"SELECT amount \
                        FROM account_card \
                        WHERE id_account = '{account_id}' AND id_card='{card_id}'"
        rows = cursor.execute(sql_command).fetchall()
        conn.close()
        print(rows)
        return rows[0][0]
    return 0

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
        sql_command = f"DELETE FROM account_card WHERE id = '{id}'"
        cursor.execute(sql_command)
        conn.commit()
        conn.close()
        exist(id)
        return 1
    return 0
#endregion
