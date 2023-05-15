import mysql.connector as mysql


db = mysql.connect(host="localhost",
                   user="root",
                   passwd="Q1w2e3r4!",
                   database='test_db_2')

cursor = db.cursor()
cursor.execute("DESC locators")
print(cursor.fetchall())

cursor.execute("INSERT INTO locators (name, type) VALUES ('//div[@id=main_button]', 'XPATH')")
db.commit()
cursor.execute("INSERT INTO locators (name, type) VALUES ('#main_button', 'CSS')")

db.commit()
print(cursor.rowcount, "record inserted")

cursor.execute('SELECT * FROM locators')
print(cursor.fetchall())