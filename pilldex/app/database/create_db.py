import sqlite3
from sqlite3 import Error
 
 
def create_connection(db_file):
    """Create a database connection to a SQLite database."""
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
        print("Table created succesfully!")
    except Error as e:
        print(e)

def main():
    database = "../pills_db.db"
    pills_ddl = """ CREATE TABLE IF NOT EXISTS pills_tbl (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        generic_name text,
                                        drug_class text
                                    ); """

    try:
        conn = create_connection(database)
    except Exception as e:
        print(e)

    if conn is not None:
        print("Executing table creation statement...")
        create_table(conn, pills_ddl)
    else:
        print("Error! cannot create the database connection.")
    conn.close()


if __name__ == '__main__':
    main()