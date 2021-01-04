# Raspberry Pi RFID Attendance System

This project is based on **"Raspberry Pi RFID Attendance System" by [Pi My Life Up](https://pimylifeup.com)**. 

You can find original project page here: https://pimylifeup.com/raspberry-pi-rfid-attendance-system/. **I recommend read this tutorial first.**

## Localisation
1. Move ```frontend``` folder to ```/var/www/html/attendancesystem```
2. Move ```backend``` folder to ```/home/pi/attendance/```

## Changes:
* change local MySQL (MariaDB) server to remote (needs allow remote connection https://mariadb.com/kb/en/configuring-mariadb-for-remote-client-access/)
* added HTTP Digest Authorization
* added "maintenance" script
* some not major changes is main backend Python engine
* turn backend to [systemd service](attendancesystem.service)
* [cron entry](attendancesystem.cron) in ```/etc/cron.d/``` preventing backend service to freeze

**This README is incomplete! Will be updated continuously.**
