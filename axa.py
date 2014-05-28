#!/usr/bin/python
import RPi.GPIO as GPIO
import time

### Setup GPIO-0(aka:pin 11)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

### looping
while True:
	GPIO.output(11, GPIO.HIGH)
	time.sleep(1)
	GPIO.output(11, GPIO.LOW)
	time.sleep(1)
