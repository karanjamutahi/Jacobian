import lcddriver
import time

lcd = lcddriver.lcd()
lcd.lcd_clear()
lcd.lcd_pretty_print('Pi has Booted')
wait=60
while wait >0:
  lcd.lcd_display_string('{}'.format(wait), 2)
  time.sleep(1)
  wait-= 1
