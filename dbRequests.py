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

def deleteUser(user_data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("DELETE FROM users WHERE userid=?", user_data)
    conn.commit()

    conn.close()

def addClass(class_data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("INSERT INTO classes(classid, dept, c_number) VALUES(null,?,?)", class_data)
    conn.commit()

    conn.close()

def delClass(class_data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    # c.execute("DELETE FROM classes WHERE classid=?", (class_id))
    c.execute("DELETE FROM ruserclasses WHERE r_classid=? AND r_userid=?", class_data)
    conn.commit()

    conn.close()

def addRuserClass(query_data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    classId = c.execute("SELECT classid FROM classes WHERE dept=? AND cnumber=?)", query_data)

    c.execute("INSERT INTO ruserclasses(r_userid, r_classid) VALUES(?,?)", query_data)
    conn.commit()

    conn.close()

def deleteRuserClass(query_data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    classId = c.execute("SELECT classid FROM classes WHERE dept=? AND cnumber=?)", query_data)

    c.execute("DELETE FROM ruserclasses WHERE r_userid=? AND r_classid=?", query_data)
    conn.commit()

    conn.close()

def addListing(listing_data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("INSERT INTO listings(listingid, l_userid, l_classid, shortDescription, topic, time_Stamp) VALUES(null,?,?,?,?,null)", listing_data)
    conn.commit()

    conn.close()

def deleteListing(listing_data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("DELETE FROM listings WHERE listingid=?", listing_data)
    conn.commit()

    conn.close()

def addHelpPair(pair_data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("INSERT INTO helpPairs(pairid, h_listingid,tutorid,fieldname,time_Stamp) VALUES(null,?,?,?,?)", pair_data)
    conn.commit()

    conn.close()

def delHelpPair(pair_data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("DELETE FROM helpPairs WHERE pairid=?", pair_data)
    conn.commit()

    conn.close()

def addMessage(message_data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("INSERT INTO messages(messagenumber,m_pairid,messagecontents,time_Stamp) VALUES(null,?,?,null)", message_data)
    conn.commit()

    conn.close()

def getAllMessages(query_data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    # this is wrong and would only work if a tutor gets their messages
    c.execute("SELECT * FROM messages WHERE tutorid=?", query_data)
    conn.commit()

    conn.close()

def delMessage(query_data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("DELETE FROM messages WHERE messagenumber=?", query_data)
    conn.commit()

    conn.close()

def getAllUsers():
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("SELECT * FROM users")
    conn.commit()

    conn.close()

def getAllClasses():
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("SELECT * FROM classes")
    conn.commit()

    conn.close

def getAllListings():
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("SELECT * FROM listings")
    conn.commit()

    conn.close

def checkUsername(user_data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("SELECT userid FROM users WHERE email=?", user_data)

    ret = c.fetchone()
    conn.close()
    if ret is None:
        return -1
    return ret[0]

def checkPassword(query_data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("SELECT userid FROM users WHERE password=?", query_data)

    ret = c.fetchone()
    conn.close()
    if ret is None:
        return -1
    return ret[0]
