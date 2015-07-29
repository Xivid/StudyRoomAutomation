# 
# Author Micheal Liu 	2015-03-06
# Project core code, to control hardware device
# 
import RPi.GPIO as GPIO
import time
import json

class io(object):
	"""basic IO and Pin remapping. Using board mode."""

	def __init__(self, configfile='ioconfig.json'):
		super(io, self).__init__()
		self.config=json.load(open(configfile))
		self.iomap=self.config["iomap"]
		self.pinnum=len(self.iomap)
		GPIO.setmode(GPIO.BOARD)

	def setup(self, pin,mode):
                if mode == "out":
                    mode = GPIO.OUT
                else:
                    mode = GPIO.IN
		if isinstance(pin,int):
			pin=[pin]
		for i in pin:
			GPIO.setup(self.iomap[i],mode)

	def set(self, l,o):
		if isinstance(l,int):
			l=[l]
		for i in l:
			GPIO.output(self.iomap[i],o)

	def get(self, pin):
		return GPIO.input(self.iomap[pin])



