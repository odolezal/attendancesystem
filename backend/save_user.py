#Raspberry Pi RFID Attendance System
#Original source: https://pimylifeup.com/raspberry-pi-rfid-attendance-system/
#Modifications by: https://github.com/odolezal/

#!/usr/bin/env python

import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector
import Adafruit_CharLCD as LCD

#create connection to MYSQL server
db = mysql.connector.connect(
  host="10.0.0.99",
  user="attendanceadmin",
  passwd="mysql_password",
  database="attendancesystem"
)

#setup DB
cursor = db.cursor()

#setup RFID reader
reader = SimpleMFRC522()

#setup LCD
lcd = LCD.Adafruit_CharLCD(4, 24, 23, 17, 18, 22, 16, 2, 4);

print("Raspberry Pi RFID Attendance System")
print("Save user mode")
print(" ")

#start main loop
try:
  while True:
    lcd.clear() #clear LCD
    print("Place new card to register...")
    lcd.message('Place new card \nto register...') #display default message
    id, text = reader.read() #read RFID card/tag by reader

    cursor.execute("SELECT id FROM users WHERE rfid_uid="+str(id)) #searching in “users” table
    cursor.fetchone() #grab one row from the returned results

    if cursor.rowcount >= 1:
      lcd.clear()
      print("Add/overwrite existing user?")
      lcd.message("Add/overwrite\nexisting user?")
      overwrite = input("Add/overwite (Y/N)? ")

      if overwrite[0] == 'Y' or overwrite[0] == 'y':
        lcd.clear()
        print("Adding/overwriting user...")
        lcd.message("Adding/ \noverwriting user...")
        time.sleep(1)
        sql_insert = "UPDATE users SET name = %s WHERE rfid_uid=%s"
      else:
        continue;
    else:
      sql_insert = "INSERT INTO users (name, rfid_uid) VALUES (%s, %s)"

    lcd.clear()
    print("Enter new name")
    lcd.message('Enter new name')
    new_name = input("Name: ")

    cursor.execute(sql_insert, (new_name, id))

    db.commit()

    lcd.clear()
    print("User " + new_name + " saved.")
    lcd.message("User " + new_name + "\nSaved")
    time.sleep(2)
    print("Done. Press Ctrl+C to quit or continue for next user.")
finally:
  GPIO.cleanup()
