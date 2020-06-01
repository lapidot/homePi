#---------------------------------------------------------------------#
#Name - IR&NECDataCollect.py
#Description - Reads data from the IR sensor but uses the official NEC Protocol (command line version)
#Author - Lime Parallelogram
#Licence - Attribution Lime
#Date - 06/07/19 - 18/08/19
#---------------------------------------------------------------------#
#Imports module

import sys
sys.path.append('/storage/.kodi/addons/virtual.rpi-tools/lib/')

import json
import urllib2
import base64



import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime
	
#==================#
#Promps for values
#Input pin
PinIn = 11
#Sets up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PinIn,GPIO.IN)

ip = 'localhost'#'192.168.1.124' '
port = '8080'
username = 'Kodi'
password = 'Kodi'



PLAYPAUSE = 1
PLAYNEXT = 2
PLAYPREV = 3
PARTYMODE = 4
SHUTDOWN = 5
commands=[None]*6
commands[PLAYPAUSE] ="0x30c0c4eb1L" #PLAY
commands[PLAYNEXT]= "0x30c0c2ed1L" #RIGHT
commands[PLAYPREV]= "0x30c0c8e71L" #LEFT
commands[PARTYMODE]="0x30c0c0cf3L" #FAV
commands[SHUTDOWN]= "0x30c0ca857L" #RED

JSONmethods=[None]*6
JSONmethods[PLAYPAUSE]=	'Player.PlayPause'
JSONmethods[PLAYNEXT]= 	'Player.GoTo'
JSONmethods[PLAYPREV]= 	'Player.GoTo'
JSONmethods[PARTYMODE]=	'Player.Open'
JSONmethods[SHUTDOWN]= 	'System.Shutdown'

JSONparameters=[None]*6
JSONparameters[SHUTDOWN]={}
JSONparameters[PLAYNEXT]= {"playerid":0,"to":"next"}#RIGHT
JSONparameters[PLAYPREV]=  {"playerid":0,"to":"previous"}#LEFT
JSONparameters[PARTYMODE]= {"item":{"partymode":"music"}}#FAV
JSONparameters[PLAYPAUSE]= {"playerid":0} #RED






url = 'http://%s:%s/jsonrpc' %(ip, port)
# Next we'll build out the Data to be sent





#def getJsonRemote(host,port,username,password,method,parameters):

def makeJSONCall(jsonmethod, jsonparam):
    # First we build the URL we're going to talk to
    values ={}
    values["jsonrpc"] = "2.0"
    values["method"] = jsonmethod
    # This fork handles instances where no parameters are specified
    values["params"] = jsonparam
    values["id"] = "1"
    headers = {"Content-Type":"application/json",}
    # Format the data
    data = json.dumps(values)
    print " data:"
    print data
    print " url:"
    print url
    
    # Now we're just about ready to actually initiate the connection
    req = urllib2.Request(url, data, headers)
    # This fork kicks in only if both a username & password are provided
    print username
    print password
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    req.add_header("Authorization", "Basic %s" % base64string)
    # Now we're ready to talk to XBMC
    # I wrapped this up in a try: statement to allow for graceful error handling
    print req.header_items
    print req.data
    try:
		print req
		response = urllib2.urlopen(req)
		response = response.read()
		response = json.loads(response)
		# A lot of the XBMC responses include the value "result", which lets you know how your call went
		# This logic fork grabs the value of "result" if one is present, and then returns that.
		# Note, if no "result" is included in the response from XBMC, the JSON response is returned instead.
		# You can then print out the whole thing, or pull info you want for further processing or additional calls.
		if 'result' in response:
			print response
			response = response['result']
			print " | response:  "
			print response
    # This error handling is specifically to catch HTTP errors and connection errors
    except urllib2.URLError as e:
	print "   |error!  :"
        # In the event of an error, I am making the output begin with "ERROR " first, to allow for easy scripting.
        # You will get a couple different kinds of error messages in here, so I needed a consistent error condition to check for.
        response = 'ERROR '+str(e.reason)
    return response

# Here's an example of using the above method and variable values to make XBMC run the add-on
#results=getJsonRemote(ip,port,username,password,method,parameters)
# I just print the results out
#print results
#return
#==================#
#Defines Subs	
def ConvertHex(BinVal): #Converts binary data to hexidecimal
	tmpB2 = int(str(BinVal), 2)
	return hex(tmpB2)
		
def getData(): #Pulls data from sensor
	num1s = 0 #Number of consecutive 1s
	command = [] #Pulses and their timings
	binary = 1 #Decoded binary command
	previousValue = 0 #The previous pin state
	value = GPIO.input(PinIn) #Current pin state
	
	while value: #Waits until pin is pulled low
		value = GPIO.input(PinIn)
	
	startTime = datetime.now() #Sets start time
	
	while True:
		if value != previousValue: #Waits until change in state occurs
			now = datetime.now() #Records the current time
			pulseLength = now - startTime #Calculate time in between pulses
			startTime = now #Resets the start time
			command.append((previousValue, pulseLength.microseconds)) #Adds pulse time to array (previous val acts as an alternating 1 / 0 to show whether time is the on time or off time)
		
		#Interrupts code if an extended high period is detected (End Of Command)	
		if value:
			num1s += 1
		else:
			num1s = 0
		
		if num1s > 10000:
			break
		
		#Reads values again
		previousValue = value
		value = GPIO.input(PinIn)
		
	#Covers data to binary
	for (typ, tme) in command:
		if typ == 1:
			if tme > 1000: #According to NEC protocol a gap of 1687.5 microseconds repesents a logical 1 so over 1000 should make a big enough distinction
				binary = binary * 10 + 1
			else:
				binary *= 10
				
	if len(str(binary)) > 34: #Sometimes the binary has two rouge charactes on the end
		binary = int(str(binary)[:34])
		
	return binary
	
def runTest(): #Actually runs the test
	#Takes samples
	command = ConvertHex(getData())
	print("Hex value: " + str(command)) #Shows results on the screen
	return command
	###

#==================#
#Main program loop
while True:
  print "entered while loop"
  finalData = runTest()
  commandCode = str(finalData)
  print " code="
  print commandCode
  for x in range(1,len(commands)):
	print x
	if finalData==commands[x]:
		print " good! "
		print commands[x]
		jsonMethod = JSONmethods[x]
		jsonParams = JSONparameters[x]
		print JSONmethods[x]
		makeJSONCall(jsonMethod,jsonParams)
		break
GPIO.cleanup()
