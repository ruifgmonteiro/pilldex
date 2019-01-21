import sqlite3
from sqlite3 import Error
 
 
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = "/home/ruifgmonteiro/Desktop/FRESH/database/pills.db"
 
    pills_table = """ CREATE TABLE IF NOT EXISTS pills (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        generic_name text,
                                        drug_class text
                                    ); """
 
    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        # create projects table
        create_table(conn, pills_table)
    else:
        print("Error! cannot create the database connection.")
    conn.close()

if __name__ == '__main__':
    main()