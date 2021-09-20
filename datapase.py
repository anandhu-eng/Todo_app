import sqlite3

conn1 = sqlite3.connect("signup.db")
cursor1=conn1.cursor()
cursor1.execute("CREATE TABLE person(username varchar(250), password TEXT)")
msg1="your account is created"
conn1.commit()
conn1.close()