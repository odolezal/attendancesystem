#Raspberry Pi RFID Attendance System
#Original source: https://pimylifeup.com/raspberry-pi-rfid-attendance-system/
#Modifications by: https://github.com/odolezal/

#!/usr/bin/env python

import os
import time
from datetime import datetime
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector
from mysql.connector import Error
import Adafruit_CharLCD as LCD
#from gpiozero import TonalBuzzer
#from gpiozero.tones import Tone
from gpiozero import LED

print("Raspberry Pi RFID Attendance System")
print("CONSOLE DEBUG:")

reader = SimpleMFRC522()
print("OK - RFID reader initialized.")

lcd = LCD.Adafruit_CharLCD(4, 24, 23, 17, 18, 22, 16, 2, 4);
print("OK - LCD display initialized.")

#buzzer = TonalBuzzer(5)
#print("OK - Buzzer initialized.")
ledGreen = LED(5)
ledRed = LED(6)
print("OK - LEDs initialized.")

try:
  db = mysql.connector.connect(
    host="10.0.0.99",
    user="attendanceadmin",
    passwd="mysql_password",
    database="attendancesystem",
    connect_timeout=28800,
    )
  print("OK - Database-Python connector initialized.")

  db.is_connected()
  print('OK - Connected to MySQL database.')

  cursor = db.cursor()

  print("Waiting for card...")

  while True:
    lcd.clear()
    lcd.blink(True)
    lcd.message('Place card to\nattendance.')
    id, text = reader.read()

    cursor.execute("Select id, name FROM users WHERE rfid_uid="+str(id))
    result = cursor.fetchone()
    lcd.clear()

    if cursor.rowcount >= 1:
      now = datetime.now()
      dateTime = now.strftime("%d.%m.%Y %H:%M:%S")
      lcd.blink(False)
      lcd.message("Welcome \n" + result[1])
      cursor.execute("INSERT INTO attendance (user_id) VALUES (%s)", (result[0],) )
      db.commit()
      print(dateTime + " Access granted for: " + result[1])
      ledGreen.on()
      time.sleep(2)
      ledGreen.off()

    else:
      now = datetime.now()
      dateTime = now.strftime("%d.%m.%Y %H:%M:%S")
      lcd.message("Card not\nrecognized!")
      ledRed.on()
      time.sleep(2)
      ledRed.off()
      print(dateTime + " Access denied! Card not recognized.")

  time.sleep(3)
finally:
  GPIO.cleanup()
