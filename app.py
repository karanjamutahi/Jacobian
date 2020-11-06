# Strategy
# Typical Hardware (Init Phase and Infinite Loop phase)
# When app starts up, prints to the LCD that its booting up and check that the Fingerprint module is connected.
# It should default start in search mode always scanning the sensor and checking whether there is a finger.
# When it eventually finds a finger it should scan the finger, get the position of the template and query it against a postgres database from where it should return a students reg.no and name
# It should then print those on the LCD screen and a button press should clear the details and start the loop afresh. 

from pyfingerprint.pyfingerprint import PyFingerprint
import sqlite3 as db

#Global Vars
#db_active = false

def print_lcd(message):
  print(message)

def init_fingerprint_sensor():
  try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
    if (f.verifyPassword() == False):
       print_lcd('Wrong Sensor Password')
       raise Exception('Wrong Sensor Password')
    return f 
  except Exception as e:
    print_lcd('Sensor Init Failed')
    exit()

def init_db():
  print_lcd('Init DB')
  try:
    db_conn = db.connect('student_fingerprint.db')
    cursor = db_conn.cursor()
    cursor.close()
    return db_conn
  except db.Error as error:
   print_lcd('DB Init failed')
   return False

def create_table(db_instance):
  try:
    query = '''CREATE TABLE students (id INTEGER PRIMARY KEY, 
                                      fName TEXT NOT NULL, 
                                      surname TEXT NOT NULL, 
                                      registration TEXT NOT NULL, 
                                      fingerprint_position INTEGER NOT NULL, 
                                      active INTEGER);
                                      '''
    cursor = db_instance.cursor()
    print("SQLite Connection Established")
    cursor.execute(query)
    db_instance.commit()
    print("Table Created")
    cursor.close()
  except Exception as e:
    print("Error while connecting to DB", e)
  finally:
    db_instance.close()

def get_user_at_position(position):
  pass

def_enrol_finger():
  pass

def read_fingerprint(f):
  print('Trying to read fingerprint')
  try:
    if (f.readImage()):
      f.convertImage(0x01)
      result = f.searchTemplate()
      position = result[0]
      print("Found finger at position {position}".format(position))
      accuracy = result[1]
      student = get_user_at_position(position)

    else:
      print("Didn't find finger")

  except Exception as e:
    print_lcd('Read Print: FAIL')
    print(e)

def setup():
  f = init_fingerprint_sensor()
  db_inst = init_db()
  
def loop():
  pass

setup()
#while 1:
#  loop()