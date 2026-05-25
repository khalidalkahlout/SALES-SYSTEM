import sqlite3

conn = sqlite3.connect('store_database.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("SELECT * FROM Sales")
sales = cursor.fetchall()

for s in sales:
    print(dict(s))

conn.close()