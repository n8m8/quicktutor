import sqlite3, json # , dbSetupClasses

dbname = 'pythonsqlite.db'

conn = sqlite3.connect(dbname)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
                                userid integer NOT NULL,
                                email text NOT NULL UNIQUE,
                                password text NOT NULL,
                                displayname text NOT NULL,
                                confirmed boolean DEFAULT FALSE,
                                timestamp text DEFAULT (datetime('now')),
                                PRIMARY KEY(userid)
                                )''')
c.execute('''CREATE TABLE IF NOT EXISTS classes (
                                    classid integer NOT NULL,
                                    dept text NOT NULL,
                                    c_number integer NOT NULL,
                                    name integer NOT NULL,
                                    description integer NOT NULL,
                                    PRIMARY KEY(classid)
                                    )''')
c.execute('''CREATE TABLE IF NOT EXISTS ruserclasses (
                                        r_userid integer NOT NULL,
                                        r_classid integer NOT NULL,
                                        FOREIGN KEY (r_userid) REFERENCES users (userid),
                                        FOREIGN KEY (r_classid) REFERENCES classes (classid)
                                        )''')
c.execute('''CREATE TABLE IF NOT EXISTS listings (
                                    listingid integer NOT NULL,
                                    l_userid integer NOT NULL,
                                    l_classid integer NOT NULL,
                                    shortDescription text NOT NULL,
                                    topic text,
                                    time_Stamp text NOT NULL,
                                    PRIMARY KEY(listingid),
                                    FOREIGN KEY (l_userid) REFERENCES users(userid),
                                    FOREIGN KEY (l_classid) REFERENCES classes(classid)
                                    )''')
c.execute('''CREATE TABLE IF NOT EXISTS helpPairs (
                                    pairid integer NOT NULL,
                                    h_listingid integer NOT NULL,
                                    tutorid integer NOT NULL,
                                    fieldname text NOT NULL,
                                    time_Stamp text NOT NULL,
                                    PRIMARY KEY(pairid),
                                    FOREIGN KEY (h_listingid) REFERENCES listings (listingid)
                                    FOREIGN KEY (tutorid) REFERENCES users (userid)
                                    )''')
c.execute('''CREATE TABLE IF NOT EXISTS messages (
                                    messagenumber integer NOT NULL,
                                    m_pairid integer NOT NULL,
                                    messagecontents text NOT NULL,
                                    time_Stamp text NOT NULL,
                                    PRIMARY KEY(messagenumber),
                                    FOREIGN KEY (m_pairid) REFERENCES helpPairs(pairid)
                                    )''')
with open('data.txt', 'r') as f:
    datastore = json.loads(f.read())
    # print(datastore)

for item in datastore:
    # print(json.dumps(item))
    query = "INSERT INTO classes (dept, c_number, name, description) VALUES ( '" + item["dept"] + "', '" + item["num"] + "', '" + item["name"] + "', '" + item["desc"] + "');"
    # print(query)
    c.execute(query)

# c.execute("INSERT INTO users(userid, email, password, displayname) values(null,?,?,?)", ('qtadmin@case.edu', 'Password1', 'admin'))
# c.execute("INSERT INTO users(userid, email, password, displayname) values(null,?,?,?)", ('qtmod@case.edu', 'Password1', 'moderator'))

conn.commit()
conn.close()
