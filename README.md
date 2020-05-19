# homePi
Kodi, IR Blaster, remote control from web interface, anything that can run on an old Pi. Mostly BASH and Python



1. check external ip address

#!/bin/bash

ip=$(curl -s https://api.ipify.org)
echo "$ip"



2. Send email (with new ip address)
https://linuxhint.com/bash_script_send_email/
1. Install very simple CLI smtp client for send-only
sudo apt install ssmtp
2. Configure
sudo geany /etc/ssmtp/ssmtp.conf
3. edit your email address to ‘AuthUser’ and your email password to ‘AuthPass’ 
4. In your Google Account > Security > Allow unsafe apps


3. bash script for 
1. Check ip address
2. Compare with last one found (saved in currentIP.txt)
3. If different
  update file
  update log
  send email
4. if same, update log date?






web server for activating IR remote control
A/C - use like a much simpler Sensibo
Speakers - turn on for music from headless KODI running on the Pi
TV - eventually reduce volume if too loud? Turn off on timer to limit kids' viewing time? Automate Netflix (turn on tv, put on correct source, volume level, energy saving)


Activate LEDs for backlight - for returning from home at night? for automatic brightness for evening time?







