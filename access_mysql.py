#!/usr/bin/python
import mysql.connector


# Open database connection
db = mysql.connector.connect(
    host="127.0.0.1",
    username="root",
    passwd="1234",
    database="TESTDB",
    port="3307",
)

# prepare a cursor object using cursor() method
cursor = db.cursor()

# # Drop table if it already exist using execute() method.
# cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
#
# # Create table as per requirement
# sql = """CREATE TABLE EMPLOYEE (
#          FIRST_NAME  CHAR(20) NOT NULL,
#          LAST_NAME  CHAR(20),
#          AGE INT,
#          SEX CHAR(1),
#          INCOME FLOAT )"""
#
# cursor.execute(sql)

# # Prepare SQL query to INSERT a record into the database.
# sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
#          LAST_NAME, AGE, SEX, INCOME)
#          VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""
# try:
#     # Execute the SQL command
#     cursor.execute(sql)
#     # Commit your changes in the database
#     db.commit()
# except:
#     # Rollback in case there is any error
#     db.rollback()

# Queries all the records from EMPLOYEE table having salary more than 1000 −
sql = "SELECT * FROM EMPLOYEE \
       WHERE INCOME > '%d'" % (1000)
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
   for row in results:
      fname = row[0]
      lname = row[1]
      age = row[2]
      sex = row[3]
      income = row[4]
      # Now print fetched result
      print("fname=%s,lname=%s,age=%d,sex=%s,income=%d" % \
             (fname, lname, age, sex, income ))
except:
   print("Error: unable to fecth data")


# disconnect from server
db.close()
