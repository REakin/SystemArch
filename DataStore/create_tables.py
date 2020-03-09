import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE Region
          (id VARCHAR(100) PRIMARY KEY ASC,
           name VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE Roast
          (id VARCHAR(100) PRIMARY KEY ASC,
           name VARCHAR(100) NOT NULL,
           region VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()
