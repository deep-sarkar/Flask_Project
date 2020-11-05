import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = 'CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT, password TEXT)'
cursor.execute(create_table)

create_table = 'CREATE TABLE IF NOT EXISTS items(id INTEGER PRIMARY KEY,name text, price reql)'
cursor.execute(create_table)

# for row in cursor.execute("select * from items"):
#     print(row)

connection.commit()
connection.close()