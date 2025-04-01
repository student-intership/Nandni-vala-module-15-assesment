import pymysql

mydb = pymysql.connect(host="localhost", user="root", password="")
mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS Billing")
mydb.commit()

mydb = pymysql.connect(host="localhost", user="root", password="", database="Billing")
mycursor = mydb.cursor()

mycursor.execute("""
CREATE TABLE IF NOT EXISTS person (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(60) NOT NULL,
    phone_no VARCHAR(20) UNIQUE NOT NULL,
    Bill_no VARCHAR(20) UNIQUE NOT NULL,             
    email VARCHAR(60) UNIQUE NOT NULL
)
""")
mydb.commit()

print("Database and table created successfully!")
