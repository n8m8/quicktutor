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

    c.execute("DELETE FROM users WHERE userid=?", (user_id,))
    conn.commit()

    conn.close()

def addClass(class_data, userid):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("INSERT INTO classes(classid, dept, c_number) VALUES(null,?,?)", class_data)
    conn.commit()

    conn.close()

def delClass(class_id, userid):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    # c.execute("DELETE FROM classes WHERE classid=?", (class_id))
    c.execute("DELETE FROM ruserclasses WHERE r_classid=? AND r_userid=?", (class_id, userid,))
    conn.commit()

    conn.close()

def addRuserClass(userId, classDept, classNum):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    classId = c.execute("SELECT classid FROM classes WHERE dept=? AND cnumber=?)", (classDept, classNum,))

    c.execute("INSERT INTO ruserclasses(r_userid, r_classid) VALUES(?,?)", (userId, classId,))
    conn.commit()

    conn.close()

def deleteRuserClass(userId, classDept, classNum):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    classId = c.execute("SELECT classid FROM classes WHERE dept=? AND cnumber=?)", (classDept, classNum,))

    c.execute("DELETE FROM ruserclasses WHERE r_userid=? AND r_classid=?", (userId, classId,))
    conn.commit()

    conn.close()

def addListing(email, location, cclass, description):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("INSERT INTO listings(listingid, l_userid, l_classid, shortDescription, time_Stamp) VALUES(null,?,?,?,null)", (email, cclass, description,))
    conn.commit()

    conn.close()

def deleteListing(listing_id):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("DELETE FROM listings WHERE listingid=?", (listing_id,))
    conn.commit()

    conn.close()

def addHelpPair(email, listingId):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("INSERT INTO helpPairs(pairid, h_listingid,tutorid,fieldname,time_Stamp) VALUES(null,?,?,?,?)", (email, listingId,))
    conn.commit()

    conn.close()

def delHelpPair(helpPair_id):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("DELETE FROM helpPairs WHERE pairid=?", (helpPair_id,))
    conn.commit()

    conn.close()

def addMessage(originId, destId, messagecontents):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("INSERT INTO messages(messagenumber,m_pairid,messagecontents,time_Stamp) VALUES(null,?,?,null)", (originId destId, messagecontents,))
    conn.commit()

    conn.close()

def getAllMessages(userId):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    # this is wrong and would only work if a tutor gets their messages
    c.execute("SELECT * FROM messages WHERE tutorid=?", (userId,))
    conn.commit()

    conn.close()

def delMessage(message_id):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("DELETE FROM messages WHERE messagenumber=?", (message_id,))
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

def checkUsername(user):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("SELECT userid FROM users WHERE email=?", (user,))

    ret = c.fetchone()
    conn.close()
    if ret is None:
        return -1
    return ret[0]

def checkPassword(pwd):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("SELECT userid FROM users WHERE password=?", (pwd,))

    ret = c.fetchone()
    conn.close()
    if ret is None:
        return -1
    return ret[0]
