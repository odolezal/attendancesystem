#!/usr/bin/python

# Show maintenance message on LCD display.

# READ:
# Run this script as: "python3 maintenance.py"
# Dont forget start service after maintenance! Use: "sudo systemctl start attendancesystem.service"

import os
import time
import Adafruit_CharLCD as LCD

# Raspberry Pi pin configuration:
lcd_backlight = 4

#Changed: https://pimylifeup.com/raspberry-pi-rfid-attendance-system/
lcd_rs        = 4
lcd_en        = 24
lcd_d4        = 23
lcd_d5        = 17
lcd_d6        = 18
lcd_d7        = 22

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

print("Raspberry Pi RFID Attendance System - Maintenance")

# Stop service
print("Stopping attendancesystem.service...")
os.system("sudo systemctl stop attendancesystem.service")
print("stopped.")
time.sleep(2)

# Clear LCD
lcd.clear()
# Print a two line message
#lcd.message('SYSTEM IS UNDER \nMAINTENANCE!')
# or:
lcd.message('SYSTEM IS OUT OF \nSERVICE! SORRY.')

print("LCD message displayed.")
print("Also check crontab or /etc/cron.d/")
print("--END--")
