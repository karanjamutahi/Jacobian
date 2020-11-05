# Strategy
# Typical Hardware (Init Phase and Infinite Loop phase)
# When app starts up, prints to the LCD that its booting up and check that the Fingerprint module is connected.
# It should default start in search mode always scanning the sensor and checking whether there is a finger.
# When it eventually finds a finger it should scan the finger, get the position of the template and query it against a postgres database from where it should return a students reg.no and name
# It should then print those on the LCD screen and a button press should clear the details and start the loop afresh. 


from pyfingerprint.pyfingerprint import Pyfingerprint

def init_fingerprint_sensor():
  try:
    f = Pyfingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
    if (f.verifyPassword() == False):
       print_lcd('Wrong Sensor Password')
       raise Exception('Wrong Sensor Password')
    return f 
  except Exception as e:
    lcd_print('Sensor Init Failed')
    exit()

def setup():
  f = init_fingerprint_sensor()
  
def loop():
  pass

setup()
while 1:
  loop()
