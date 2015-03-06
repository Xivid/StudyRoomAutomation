# 
# Author Micheal Liu 	2015-03-06
# Project core code, to control hardware device
# 
import RPi.GPIO as GPIO
import time
import json

class IO(object):
	"""basic IO and Pin remapping. Using board mode."""

	def __init__(self, configfile='ioconfig.json'):
		super(IO, self).__init__()
		self.config=json.load(open(configfile))
		self.iomap=self.config["iomap"]
		self.mode()

	def mode(m=GPIO.BOARD):
		GPIO.setmode(m)


