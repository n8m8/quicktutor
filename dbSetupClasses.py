import sqlite3

dbname = 'pythonsqlite.db'

conn = sqlite3.connect(dbname)
c = conn.cursor()

with open('data.txt', 'r') as f:
    datastore = json.load(f)

for item in datastore:
    query = "INSERT INTO classes (department, c_number, name, description) VALUES ( " + item['dept'] + ", " + item['num'] + ", " + item['name'] + ", " + item['desc'] + ");"
