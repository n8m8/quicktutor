import sqlite3

dbname = 'pythonsqlite.db'

def dict_from_row(row):
    return dict(zip(row.keys(), row))

def addUser(user_data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("INSERT INTO users(userid, email, password, displayname) values(null,?,?,?)", user_data)
    conn.commit()

    conn.close()

def deleteUser(user_id):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("DELETE FROM users WHERE userid=?", (user_id))
    conn.commit()

    conn.close()

def addClass(class_data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("INSERT INTO classes(classid, dept, c_number) VALUES(null,?,?)", class_data)
    conn.commit()

    conn.close()

def delClass(class_id):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("DELETE FROM classes WHERE classid=?", (class_id))
    conn.commit()

    conn.close()
