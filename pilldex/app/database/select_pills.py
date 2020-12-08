"""
Example usage for accessing data in pills database.
"""

import sqlite3
from sqlite3 import Error
 
 
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None
 
 
def select_all_pills(conn):
    """
    Query all rows in the pills table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM pills_tbl")
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)
 
 
def select_pills_by_id(conn, pill_id):
    """
    Query pills by their pill id
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM pills_tbl WHERE id=?", (pill_id,))
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)
 
 
def main():
    database = "../pills_db.db"
 
    conn = create_connection(database)
    with conn:
        print("1. Query pill by pill id:")
        select_pills_by_id(conn,10)
 
        print("2. Query all pills")
        select_all_pills(conn)
 
 
if __name__ == '__main__':
    main()