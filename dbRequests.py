import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

dbname = 'pythonsqlite.db'

def dict_from_row(row):
    return dict(zip(row.keys(), row))

def addUser(user_data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("INSERT INTO users(userid, email, password, displayname) values(null,?,?,?)", user_data)
    conn.commit()

    conn.close()

def confirmUser(query_data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("DELETE FROM users WHERE timestamp <= date('now','-1 day');")

    c.execute("SELECT email FROM users WHERE confirmed = 'FALSE' AND email=?",query_data)

    fet = c.fetchone()
    if fet is None:
        conn.commit()
        conn.close()
        return False

    c.execute("UPDATE users SET confirmed = 'TRUE' WHERE email=?",query_data)


    conn.commit()
    conn.close()
    return True

def changeUserPassword(query_data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("UPDATE users SET password=? WHERE email=?",query_data)

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

    # classId = c.execute("SELECT classid FROM classes WHERE dept=? AND cnumber=?)", query_data)

    c.execute("INSERT INTO ruserclasses(r_userid, r_classid) VALUES((SELECT userid FROM users WHERE email=?),(SELECT classid FROM classes WHERE dept=? AND c_number=?))", query_data)
    conn.commit()

    conn.close()

def deleteRuserClass(query_data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("SELECT classid FROM classes WHERE dept=? AND cnumber=?)", query_data)

    c.execute("DELETE FROM ruserclasses WHERE r_userid=(SELECT userid FROM users WHERE email=?) AND r_classid=(SELECT classid FROM classes WHERE dept=? AND c_number=?)", query_data)
    conn.commit()

    conn.close()

def getClassesForUser(user_data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("SELECT r_classid FROM ruserclasses WHERE r_userid= (SELECT userid FROM users WHERE email=?)", user_data)
    classes = c.fetchall()

    conn.close()

    return classes

def getClassStringName(query_data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    print(query_data)
    c.execute("SELECT dept, c_number FROM classes WHERE classid=?",query_data)
    deptNumPair = c.fetchone()
    conn.close()

    if deptNumPair is None:
        return ""
    else:
        return str(deptNumPair[0]) + " " + str(deptNumPair[1])

def getUserIdFromEmail(query_data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("SELECT userid FROM users WHERE email=?",query_data)

    ret = c.fetchone()
    conn.commit()
    conn.close()

    return ret

def addListing(listing_data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("INSERT INTO listings(listingid, l_userid, l_classid, shortDescription, topic, l_location, time_Stamp) VALUES(null,(SELECT userid FROM users WHERE email=?),?,?,?,?,(SELECT datetime('now')))", listing_data)
    conn.commit()

    conn.close()
    return c.lastrowid

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

    conn.close()

def getClassIdFromName(className):
    tokens = className.split(" ")
    dept = tokens[0]
    num = tokens[1]

    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("SELECT classid FROM classes WHERE dept=? AND c_number=? LIMIT 1", (dept, num,))

    ret = c.fetchone()
    conn.commit()
    conn.close()
    if ret is None:
        return -1
    else:
        return ret[0]

def getAllListings():
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("SELECT * FROM listings")
    ret = c.fetchall()

    conn.commit()
    conn.close()

    return ret


def validateUserData(user_data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("SELECT userid FROM users WHERE email=? AND password=?", user_data)

    ret = c.fetchone()
    conn.close()
    if ret is None:
        return -1
    return ret[0]

def getHashedPassword(query_data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("SELECT password FROM users WHERE email=?", query_data)

    hashedPassword = c.fetchone()
    conn.close()

    if hashedPassword is None:
        return None
    return hashedPassword[0]

def getUsernameFromUserEmail(data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("SELECT displayname FROM users WHERE email=?", data)
    name = c.fetchone()[0]

    conn.commit()
    conn.close()
    return name

def changeUserScreenname(query_data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("UPDATE users SET displayname=? WHERE email=?", query_data)

    conn.commit()
    conn.close()

def checkPassword(query_data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("SELECT userid FROM users WHERE password=?", query_data)

    ret = c.fetchone()
    conn.close()
    if ret is None:
        return -1
    return ret[0]

def lookupUserIdFromEmail(query_data):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute("SELECT userid FROM users WHERE email=?", query_data)

    userid = c.fetchone()

    conn.commit()
    conn.close()
    if userid != None:
        return userid
    else:
        return -1

def addDefaultAccounts():
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    adminpw = generate_password_hash('Password1')
    modpw = generate_password_hash('Password1')

    try:
        c.execute("INSERT INTO users(userid, email, password, displayname, confirmed) values(null,?,?,?,?)", ('qtadmin@case.edu', adminpw, 'admin', True))
        c.execute("INSERT INTO users(userid, email, password, displayname, confirmed) values(null,?,?,?,?)", ('qtmod@case.edu', modpw, 'moderator', True))
    except sqlite3.IntegrityError:
        print("Tried to add default accounts, but they already exist")


    conn.commit()
    conn.close()
