import sqlite3
import random


conn = sqlite3.connect('doors.db')
conn2 = sqlite3.connect('windows.db')
c=conn.cursor()
c2=conn2.cursor()

c.execute("""CREATE TABLE doorsTable (
          doorNumber integer,
          lock text
           )""")

c2.execute("""CREATE TABLE windowsTable (
           windowNumber integer,
           lock text
           )""")
conn.commit()
conn2.commit()


def insert_door(doorNumber, lock):
    with conn:
        c.execute("INSERT INTO doorsTable VALUES (:doorNumber, :lock)",{'doorNumber':doorNumber, 'lock':lock})

def update_door(doorNumber, lock):
    with conn:
        c.execute("""UPDATE from doorsTable SET lock = :lock WHERE doorNumber =:doorNumber""",{'doorNumber':doorNumber, 'lock':lock})

def get_status_by_number(doorNumber):
    c.execute("SELECT * FROM doorsTable WHERE doorNumber=:doorNumber", {'doorNumber': doorNumber})
    return c.fetchall()

def insert_window(windowNumber, lock):
    with conn2:
        c2.execute("INSERT INTO windowsTable VALUES (:windowNumber, :lock)",{'windowNumber':windowNumber, 'lock':lock})

def update_window(windowNumber, lock):
    with conn2:
        c2.execute("""UPDATE from windowsTable SET lock = :lock WHERE windowNumber =:windowNumber""",{'windowNumber':windowNumber, 'lock':lock})

def get_status_by_number(windowNumber):
    c.execute("SELECT * FROM windowsTable WHERE windowNumber=:windowNumber", {'windowNumber': windowNumber})
    return c.fetchall()

for x in range(21):
    
    mylist1 = ['open', 'close']
    insert_door(x+1,random.choice(mylist1)) 
    insert_window(x+1,random.choice(mylist1)) 
    
conn.close()
conn2.close()