db_inst = None

import sqlite3 as db
def print_lcd(message):
    print(message)

def init_db():
  print_lcd('Init DB')
  try:
    db_conn = db.connect('student_fingerprint.db')
    cursor = db_conn.cursor()
    cursor.close()
    print_lcd('Init Success')
    return db_conn
  except db.Error as error:
   print_lcd('DB Init failed')
   print(error)
   return False

def insert_into_db(db_inst, fName, surname, registration, position, active=1):
  try:
    cursor = db_inst.cursor()
    query = 'INSERT into students (fName, surname, registration, position, active) VALUES ({}, {}, {}, {}, {})'.format(fName, surname, registration, position, active)
    cursor.execute(query)
    db_inst().commit()
    cursor.close()
  except db.Error as error:
    print_lcd("Insert Failed")
    print(error)

db_inst = init_db
insert_into_db(db_inst,'Karanja', 'Mutahi', 'EN271-3867/2015', 3)