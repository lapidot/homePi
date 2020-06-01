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



install apache
sudo apt update
sudo apt install apache2 -y




web server for activating IR remote control
A/C - use like a much simpler Sensibo
Speakers - turn on for music from headless KODI running on the Pi
TV - eventually reduce volume if too loud? Turn off on timer to limit kids' viewing time? Automate Netflix (turn on tv, put on correct source, volume level, energy saving)


Activate LEDs for backlight - for returning from home at night? for automatic brightness for evening time?



Connect to WiFi network using SSH
https://www.ev3dev.org/docs/tutorials/setting-up-wifi-using-the-command-line/
robot@ev3dev:~$ connmanctl
Error getting VPN connections: The name net.connman.vpn was not provided by any
connmanctl> enable wifi
Enabled wifi
connmanctl> scan wifi
Scan completed for wifi
connmanctl> services
*AO Wired                ethernet_b827ebbde13c_cable
                         wifi_e8de27077de3_hidden_managed_none
    AH04044914           wifi_e8de27077de3_41483034303434393134_managed_psk
    Frissie              wifi_e8de27077de3_46726973736965_managed_psk
    ruijgt gast          wifi_e8de27077de3_7275696a67742067617374_managed_psk
    schuur               wifi_e8de27077de3_736368757572_managed_psk
connmanctl> agent on
Agent registered
connmanctl> connect wifi_e8de27077de3_41      # You can use the TAB key at this point to autocomplete the name
connmanctl> connect wifi_e8de27077de3_41483034303434393134_managed_psk
Agent RequestInput wifi_e8de27077de3_41483034303434393134_managed_psk
  Passphrase = [ Type=psk, Requirement=mandatory ]
Passphrase? *************
Connected wifi_e8de27077de3_41483034303434393134_managed_psk
connmanctl> quit





Simple Python Script To Control XBMC via Web/JSON API

https://forum.kodi.tv/showthread.php?tid=197645

ip = 'localhost'
port = '8080'
username = 'KodiUserName'
password = 'KodiPassword'


Action	    Method	          Prarmeters
Shutdown	  System.Shutdown	  {}
Previous	  Player.GoTo	      {"playerid":0,"to":"previous"}
Next	      Player.GoTo	      {"playerid":0,"to":"next"}
Party Mode	Player.Open	      {"item":{"partymode":"music"}}
Play/Pause	Player.PlayPause	{ "playerid":0}

entire script added to code - read iR codes from remote, make a call to JSON-RPC on localhost


for RPi.GPIO to work in the scipt we need to install it. This cannot be done over shell (ssh) as apt-get pip etc. don't work on LibreElec
from Kodi UI, install libreElec addons -> program addons -> Raspberry Pi Tools 
