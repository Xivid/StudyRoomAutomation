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
		self.pinnum=len(self.iomap)
		self.mode()

	def mode(m=GPIO.BOARD):
		GPIO.setmode(m)

	def setup(pin,mode):
		if isinstance(pin,int):
			pin=[pin]
		for i in pin:
			GPIO.setup(self.iomap[i],mode)

	def set(l,o):
		if isinstance(l,int):
			l=[l]
		for i in l:
			GPIO.output(self.iomap[i],o)

	def get(pin):
		return GPIO.input(self.iomap[pin])



