import mysql.connector

conn = mysql.connector.connect(host="ec2-34-219-64-10.us-west-2.compute.amazonaws.com", user="root",
password="Password", database="servicearch")

c = conn.cursor()
c.execute('''
          CREATE TABLE Region
          (id VARCHAR(100) NOT NULL,
           name VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT Region_id_pk PRIMARY KEY (id))
          ''')

c.execute('''
          CREATE TABLE Roast
          (id VARCHAR(100) NOT NULL,
           name VARCHAR(100) NOT NULL,
           region VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT Roast_id_pk PRIMARY KEY (id))
          ''')

conn.commit()
conn.close()
