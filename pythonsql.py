import sqlite3
from sqlite3 import Error

dbname = 'pythonsqlite.db'

def create_connection(db_file):
    """ creating a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        # print(sqlite3.version)
        return conn
    except Error as e:
        print(e)
    # finally:
    #     conn.close()
    return None

# this one doesn't specify the database used, I wrote the user one below following the convention
def create_user(eemail, ddisplayname, ppassword):
    try:
        query = "INSERT INTO users (email, password, displayname) VALUES ('nfwalls', 'testpassword', 'testname')";
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        conn.close()
    except Error as e:
        print(e)

def get_all_users():
    try:
        query = "SELECT * FROM users"
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        conn.close()
    except Error as e:
        print(e)


#########################################
def create_table(conn, create_table_sql):
    # create a table from the create_table_sql statement
    # :param conn: Connection object
    # :param create_table_sql: a CREATE TABLE statement
    # :return:
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_users(conn, user):
    # Create a new user into the users table
    # :param conn:
    # :param user:
    # :return: user id (optional)
    sql = '''INSERT INTO users(email,password,displayname)
              VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, user)
    return cur.lastrowid

# def create_ruserclasses(conn, ruserclass):
#     # Create a new relation into the ruserclasses table
#     # :param conn:
#     # :param user:
#     # :return: user id (optional)
#     sql = '''INSERT INTO ruserclasses()
#               VALUES(?)'''
#     cur = conn.cursor()
#     cur.execute(sql, ruserclass)
#     return cur.lastrowid

def create_classes(conn, classes):
    # Create a new class into the classes table
    # :param conn:
    # :param class:
    # :return:
    sql = '''INSERT INTO classes(dept,c_number)
              VALUES(?,?)'''
    cur = conn.cursor()
    cur.execute(sql, classes)
    return cur.lastrowid

def create_listings(conn, listing):
    # Create a new listing into the listings table
    # :param conn:
    # :param listing:
    # :return:
    sql = '''INSERT INTO listings(l_userid,l_classid,shortDescription,time_Stamp)
              VALUES(?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, listing)
    return cur.lastrowid

def create_helphairs(conn, help_pair):
    # Create a new user into the users table
    # :param conn:
    # :param help_pair:
    # :return: user id (optional)
    sql = '''INSERT INTO helpPairs(h_listingid,tutorid,fieldname,time_Stamp)
              VALUES(?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, help_pair)
    return cur.lastrowid

def create_messages(conn, message):
    # Create a new message into the messages table
    # :param conn:
    # :param user:
    # :return: user id (optional)
    sql = '''INSERT INTO helpPairs(m_pairid,messagecontents,time_Stamp)
              VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, message)
    return cur.lastrowid


def main():
    database = "pythonsqlite.db"
    sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                userid integer NOT NULL,
                                email text NOT NULL,
                                password text NOT NULL,
                                displayname text NOT NULL,
                                PRIMARY KEY(userid)
                                );"""
    sql_create_classes_table = """CREATE TABLE IF NOT EXISTS classes (
                                    classid integer NOT NULL,
                                    dept text NOT NULL,
                                    c_number integer NOT NULL,
                                    PRIMARY KEY(classid)
                                    );"""
    sql_create_ruserclasses_table = """CREATE TABLE IF NOT EXISTS ruserclasses (
                                        r_userid integer NOT NULL,
                                        r_classid integer NOT NULL,
                                        FOREIGN KEY (r_userid) REFERENCES users (userid),
                                        FOREIGN KEY (r_classid) REFERENCES classes (classid)
                                        );"""
    sql_create_listings_table = """CREATE TABLE IF NOT EXISTS listings (
                                    listingid integer NOT NULL,
                                    l_userid integer NOT NULL,
                                    l_classid integer NOT NULL,
                                    shortDescription text NOT NULL,
                                    time_Stamp text NOT NULL,
                                    PRIMARY KEY(listingid),
                                    FOREIGN KEY (l_userid) REFERENCES users(userid),
                                    FOREIGN KEY (l_classid) REFERENCES classes(classid)
                                    );"""
    sql_create_helppairs_table = """CREATE TABLE IF NOT EXISTS helpPairs (
                                    pairid integer NOT NULL,
                                    h_listingid integer NOT NULL,
                                    tutorid integer NOT NULL,
                                    fieldname text NOT NULL,
                                    time_Stamp text NOT NULL,
                                    PRIMARY KEY(pairid),
                                    FOREIGN KEY (h_listingid) REFERENCES listings (listingid)
                                    );"""
    sql_create_messages_table = """CREATE TABLE IF NOT EXISTS messages (
                                    messagenumber integer NOT NULL,
                                    m_pairid integer NOT NULL,
                                    messagecontents text NOT NULL,
                                    time_Stamp text NOT NULL,
                                    PRIMARY KEY(messagenumber),
                                    FOREIGN KEY (m_pairid) REFERENCES helpPairs(pairid)
                                    );"""

    conn = create_connection(database)
    if conn is not None:
        # create users table
        create_table(conn, sql_create_users_table)
        # create classes table
        create_table(conn, sql_create_classes_table)
        # create ruserclasses table
        create_table(conn, sql_create_ruserclasses_table)
        # create listings table
        create_table(conn, sql_create_listings_table)
        # create helppairs table
        create_table(conn, sql_create_helppairs_table)
        # create messages table
        create_table(conn, sql_create_messages_table)
        conn.commit()
    else:
        print("Error! cannot create the database connection.")

    create_user("nfwalls", "nathan", "testpassword")
    print(get_all_users())

if __name__ == '__main__':
    main()
