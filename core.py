# 
# Author Micheal Liu 	2015-03-07
# Project core code, to control hardware device
# 
import io
import time
import client
class control(object):
	"""docstring for control, Basic counting."""
	light=[0,1]
	monitor=[2,3]
	clientcode="A"

	def __init__(self, arg):
		super(control, self).__init__()
		self.arg = arg
		io.mode(self.light,GPIO.OUT)
		io.mode(self.monitor,GPIO.IN)
	
	def passroad(pin1,pin2):
			if io.get(pin1):

				if io.get(pin2):
					## 两个角都穿过为错误的通过方式
					return 0
				else:
					## 等待人进入第二范围
					while !(io.get(pin2)):
						pass

				if io.get(pin1):
					## 进入第二脚时，已经通过第一脚，通过物体太小，忽略
					return 0
				while !io.get(pin1):
					## 等待通过第一脚
					pass
				if io.get(pin2):
					## 同时离开两个角，不能出现
					return 0
				while !io.get(pin2):
					pass
				return 1
			else:
				## 其他情况输入错误
				return 0

	def mainloop(self):
		while 1:
			if io.get(self.monitor[0]):
				if self.passroad(self.monitor[0],self.monitor[1]):
					client.send(self.clientcode+'+')
			if io.get(self.monitor[1]):
				if self.passroad(self.monitor[1],self.monitor[0]):
					client.send(self.clientcode+'+')
			time.sleep(0.1)
