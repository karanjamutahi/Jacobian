# Strategy
# Typical Hardware (Init Phase and Infinite Loop phase)
# When app starts up, prints to the LCD that its booting up and check that the Fingerprint module is connected.
# It should default start in search mode always scanning the sensor and checking whether there is a finger.
# When it eventually finds a finger it should scan the finger, get the position of the template and query it against a postgres database from where it should return a students reg.no and name
# It should then print those on the LCD screen and a button press should clear the details and start the loop afresh. 

from pyfingerprint.pyfingerprint import PyFingerprint
import sqlite3 as db
from time import *
import lcddriver
from time import sleep
import RPi.GPIO as GPIO

lcd = lcddriver.lcd()
lcd.lcd_clear()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Global Vars
#db_active = false
fingerprint = None
db_inst = None
enroll = True

def print_lcd(message):
  #20X4 buffer
  #pass message to lcd_print
 # lcd.lcd_clear()
  lcd.lcd_print(message)
  print(message)


def init_fingerprint_sensor():
  print_lcd('Init Fingerprint')
  try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
    if (f.verifyPassword() == False):
       print_lcd('Wrong Sensor Password')
       raise Exception('Wrong Sensor Password')
    print_lcd('Init Success')
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
    print_lcd('Init Success')
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

def enrol_finger(f):
  print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

  ## Tries to enroll new finger
  try:
      print('Waiting for finger...')
      print_lcd("Put finger on")

      ## Wait that finger is read
      while ( f.readImage() == False ):
          pass

      ## Converts read image to characteristics and stores it in charbuffer 1
      f.convertImage(0x01)

      ## Checks if finger is already enrolled
      result = f.searchTemplate()
      positionNumber = result[0]

      if ( positionNumber >= 0 ):
          print('Template already exists at position #' + str(positionNumber))
          exit(0)

      print('Remove finger...')
      print_lcd("Remove Finger")
      time.sleep(2)

      print('Waiting for same finger again...')
      print_lcd("Put finger again")

      ## Wait that finger is read again
      while ( f.readImage() == False ):
          pass

      ## Converts read image to characteristics and stores it in charbuffer 2
      f.convertImage(0x02)

      ## Compares the charbuffers
      if ( f.compareCharacteristics() == 0 ):
          raise Exception('Fingers do not match')
          print_lcd("Fingers mismatch")

      ## Creates a template
      f.createTemplate()

      ## Saves template at new position number
      positionNumber = f.storeTemplate()
      print('Finger enrolled successfully!')
      print('New template position #' + str(positionNumber))
      print_lcd("Enrolled Successfully")

  except Exception as e:
      print('Operation failed!')
      print('Exception message: ' + str(e))
      print_lcd("Operation Fail")
      exit(1)

def read_fingerprint(f):
  #print('Trying to read fingerprint')
  try:
    if (f.readImage()):
      f.convertImage(0x01)
      result = f.searchTemplate()
      position = result[0]
      return position
    else:
      #print("Didn't find finger")
      return None

  except Exception as e:
    print_lcd('Read Print: FAIL Try Again')
    print(e)
    sleep(1)

def fetch_from_db_with_position(db_inst, position):
  query = 'SELECT * FROM students WHERE fingerprint_position = {}'.format(position)
  cursor = db_inst.cursor()
  cursor.execute(query)
  results = cursor.fetchone()
  print(results)
  return results

def insert_into_db(db_inst, fName, surname, registration, position, active=1):
  try:
    cursor = db_inst.cursor()
    query = "INSERT into students (fName, surname, registration, fingerprint_position, active) VALUES ('{}', '{}', '{}', {}, {})".format(fName, surname, registration, position, active)
    cursor.execute(query)
    db_inst.commit()
    cursor.close()
  except db.Error as error:
    print_lcd("Insert Failed")
    print(error)

def read_fingerprint_and_fetch(f, db_inst):
  position = read_fingerprint(f)
  if position is None:
    print("Read Failed")
    return
  fetch_from_db_with_position(db_inst, position)
  print("FOUND FINGER AT POSITION 3 {}".format(position))

def setup():
  global fingerprint
  global db_inst
  fingerprint = init_fingerprint_sensor()
  db_inst = init_db()
  print('Waiting for finger . . .')

def loop():
  position = read_fingerprint(fingerprint)
  if position is not None:
    result = fetch_from_db_with_position(db_inst, position)
    if result is not None:
      firstName = result[1]
      lastName = result[2]
      registration = result[3]
      print('Found at position {}'.format(position))
      print('\n================{}===============\n'.format(firstName))
      print('\n================{}===============\n'.format(lastName))
      print('\n================{}===============\n'.format(registration))
      print_lcd("{} {}\n{}".format(firstName, lastName, registration))
      print("Waiting for Finger....")
    else:
      print("Result is None")
      print_lcd("Print not found")

  sleep(0.3)

setup()
while 1:
  loop()
  if GPIO.input(16) == GPIO.LOW:
    if enroll == True:
      enroll = False
      #proceed to enrolling students
      print("Enroll Mode")
      print_lcd("Enroll")
      lcd.lcd_clear()
      enrol_finger(fingerprint)






    elif enroll == False:
      enroll = True
      print("Search Mode")
      lcd.lcd_clear()
      print_lcd("Enter Search Mod")
      loop()

