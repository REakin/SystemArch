import mysql-connector-python
import pymysql

conn =  mysql.connector.connect(host="localhost", user="root", 
password="Password", database="systemarch")

c = conn.cursor()
c.execute('''
          DROP TABLE Region, Roast
          ''')

conn.commit()
conn.close()
