#-*- coding: utf-8 -*-
# 
# Author Micheal Liu     2015-03-07
# Project core code, to control hardware device
# 
import io
import time
import client
class control(object):
    """docstring for control, Basic counting."""
    global myio
    light=[0,1]
    monitor=[2,3]
    clientcode="A"
    myio = io.io()
    def __init__(self):
        super(control, self).__init__()
        #self.arg = arg
        myio.setup(self.light, "out")
        myio.setup(self.monitor, "in")
    
    def passroad(self, pin1,pin2):
            if myio.get(pin1):
                if myio.get(pin2):
                    ## 两个脚都穿过为错误的通过方式
                    return 0
                else:
                    ## 等待人进入第二范围
                    while not (myio.get(pin2)):
                        pass

                if myio.get(pin1):
                    ## 进入第二脚时，已经通过第一脚，通过物体太小，忽略
                    return 0
                while not myio.get(pin1):
                    ## 等待通过第一脚
                    pass
                if myio.get(pin2):
                    ## 同时离开两个脚，不能出现
                    return 0
                while not myio.get(pin2):
                    pass
                return 1
            else:
                ## 其他情况输入错误
                return 0

    def mainloop(self):
        while True:
            if myio.get(self.monitor[0]) == 1:
                print "monitor 0 shadowed"
                if self.passroad(self.monitor[0],self.monitor[1]):
                    print "passroad --->"
                    client.send(self.clientcode+'+')
            if myio.get(self.monitor[1]) == 1:
                print "monitor 1 shadowed"
                if self.passroad(self.monitor[1],self.monitor[0]):
                    print "<--- passroad"
                    client.send(self.clientcode+'+')
            time.sleep(0.1)

if __name__ == "__main__":
    ctrl = control()
    ctrl.mainloop()