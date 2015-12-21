# Raspberry Pi Fabulous Festive Thermometer, Copyright (c) 2015, Chelsea Back
# All rights reserved.

# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

#  2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Note: connect the DS18B20 to pin 7 (GPIO 4) and ensure w1-gpio is loaded

# Import libraries

import RPi.GPIO as GPIO
import time

# Initialise variable

previousTemp = 10

# Define which LEDs are off and on for each temperature

LEDPINS = {3, 5, 8, 10, 11, 12, 13, 15, 16, 18, 19, 21}
TM5ON = {3, 5, 8, 10, 11, 12}
TM5OFF = {13, 15, 16, 18, 19}
TM4ON = {5, 8, 10, 11, 12}
TM4OFF = {3, 13, 15, 16, 18, 19}
TM3ON = {8, 10, 11, 12}
TM3OFF = {3, 5, 13, 15, 16, 18, 19}
TM2ON = {10, 11, 12}
TM2OFF = {3, 5, 8, 13, 15, 16, 18, 19}
TM1ON = {11, 12}
TM1OFF = {3, 5, 8, 10, 13, 15, 16, 18, 19}
T0ON = {12}
T0OFF = {3, 5, 8, 10, 11, 13, 15, 16, 18, 19}
T1ON = {12, 13}
T1OFF = {3, 5, 8, 10, 11, 15, 16,  18, 19}
T2ON = {12, 13, 15}
T2OFF = {3, 5, 8, 10, 11, 16, 18, 19}
T3ON = {12, 13, 15, 16}
T3OFF = {3, 5, 8, 10, 11, 18, 19}
T4ON = {12, 13, 15, 16, 18}
T4OFF = {3, 5, 8, 10, 11, 19}
T5ON = {12, 13, 15, 16, 18, 19}	
T5OFF = {3, 5, 8, 10, 11}
alertLeds = 21

# set up GPIO pins

GPIO.setmode(GPIO.BOARD)
for pin in LEDPINS:
	GPIO.setup(pin,GPIO.OUT)

# Function to get the temperature

def getTemp():

	# Open the file for the sensor and read contents
	tempfile = open("/sys/bus/w1/devices/28-000006951c87/w1_slave")
	thetext = tempfile.read()
	tempfile.close()
	# Get the temperature
	tempdata = thetext.split("\n")[1].split(" ")[9]
	temperature = float(tempdata[2:])
	temperature = temperature / 1000
	# Print out the temperature
	roundTemp = round(temperature)
	return roundTemp

# Function to update the temperature LEDs

def updateThermometer(temp):
	if temp <= -5:
		for onpin in TM5ON:
			GPIO.output(onpin,GPIO.HIGH)
		for offpin in TM5OFF:
			GPIO.output(offpin,GPIO.LOW)
	elif temp == -4:
		for onpin in TM4ON:
			GPIO.output(onpin,GPIO.HIGH)
		for offpin in TM4OFF:
			GPIO.output(offpin,GPIO.LOW)
        elif temp == -3:
                for onpin in TM3ON:
			GPIO.output(onpin,GPIO.HIGH)
                for offpin in TM3OFF:
                        GPIO.output(offpin,GPIO.LOW)
        elif temp == -2:
                for onpin in TM2ON:
                        GPIO.output(onpin,GPIO.HIGH)
                for offpin in TM2OFF:
                        GPIO.output(offpin,GPIO.LOW)
        elif temp == -1:
                for onpin in TM1ON:
                        GPIO.output(onpin,GPIO.HIGH)
                for offpin in TM1OFF:
                        GPIO.output(offpin,GPIO.LOW)
        elif temp == 0:
                for onpin in T0ON:
                        GPIO.output(onpin,GPIO.HIGH)
                for offpin in T0OFF:
                        GPIO.output(offpin,GPIO.LOW)
        elif temp == 1:
                for onpin in T1ON:
                        GPIO.output(onpin,GPIO.HIGH)
                for offpin in T1OFF:
                        GPIO.output(offpin,GPIO.LOW)
        elif temp == 2:
                for onpin in T2ON:
                        GPIO.output(onpin,GPIO.HIGH)
                for offpin in T2OFF:
                        GPIO.output(offpin,GPIO.LOW)
        elif temp == 3:
                for onpin in T3ON:
                        GPIO.output(onpin,GPIO.HIGH)
                for offpin in T3OFF:
                        GPIO.output(offpin,GPIO.LOW)
        elif temp == 4:
                for onpin in T4ON:
                        GPIO.output(onpin,GPIO.HIGH)
                for offpin in T4OFF:
                        GPIO.output(offpin,GPIO.LOW)
        else:
                for onpin in T5ON:
                        GPIO.output(onpin,GPIO.HIGH)
                for offpin in T5OFF:
                        GPIO.output(offpin,GPIO.LOW)

# Function to control the snow alert LEDs

def snowalert(active):
	if active == 'on':
		for i in range(0,5):
			GPIO.output(alertLeds,GPIO.LOW)
			time.sleep(1)
			GPIO.output(alertLeds,GPIO.HIGH)
			time.sleep(1)
			GPIO.output(alertLeds,GPIO.LOW)
	else:
		GPIO.output(alertLeds,GPIO.HIGH)
	return
			
# Main program loop
# Snow alert only active at 0C (but could easily be modified)

while 1:

	currentTemp = getTemp()
	print currentTemp
	updateThermometer(currentTemp)
	if currentTemp == 0 and previousTemp != 0:
		snowalert('on')
	else:
		snowalert('off')
	previousTemp = currentTemp
	time.sleep(0.5)

# Clean up GPIO pins on exit

GPIO.cleanup()
