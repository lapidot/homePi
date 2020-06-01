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



# Connect to WiFi network using CLI (SSH)
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





# Parameters for Python Script To Control XBMC via Web/JSON API

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



# GPIO on LibreElec
this thread gave me a lot of info on making the GPIO work:
https://forum.libreelec.tv/thread/1754-problem-installing-pi-tools-addon/


for RPi.GPIO to work in the scipt we need to install it. This cannot be done over shell (ssh) as apt-get pip etc. don't work on LibreElec

1. from Kodi UI, install libreElec addons -> program addons -> Raspberry Pi Tools 

2. A file named config.txt exists on the /boot folder. It was on a different partition on the microSD card, that wasn't accessible over SSH. I took it out and read it on a computer. Found the file in the root directory.
Add these lines to the config.txt file: 

dtoverlay=lirc-rpi
dtparam=gpio_in_pull=up

source:
https://filter-failure.eu/2015/11/raspberry-pi-2-lirc-with-an-active-low-ir-receiver-with-raspbian-jessie/

3. make sure these lines are added to the top of the python script file (these were not needed when testing on a non-openelec debian distro):
import sys
sys.path.append('/storage/.kodi/addons/virtual.rpi-tools/lib')

# Run on startup
https://forum.kodi.tv/showthread.php?tid=247988
create the file (touch, or just use nano)
/storage/.config/autostart.sh
then make it an executable:
chmod +x /storage/.config/autostart.sh

(
  python /downloads/ir.sys
)&

# Get files over SSH
sudo sftp LibreELEC.018.co.il
lcd Downloads/
get ir.py


# Untested - Rurn wifi on/off (bash script)
https://www.linuxquestions.org/questions/linux-wireless-networking-41/script-to-turn-wifi-on-off-4175564405/

# Untested - Run bash script from python (not checked if possible on LibreElec)
https://python-forum.io/Thread-Enable-Disable-Wireless-connection-by-using-python
import subprocess
result = subprocess.run(["netsh", "interface", "set", "interface", "Wi-Fi", "DISABLED"])
print("FAILED..." if result.returncode else "SUCCESS!")
