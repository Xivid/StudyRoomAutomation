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
                    ## 两个脚都穿过为错误的通过方式
                    return 0
                else:
                    ## 等待人进入第二范围
                    while not (io.get(pin2)):
                        pass

                if io.get(pin1):
                    ## 进入第二脚时，已经通过第一脚，通过物体太小，忽略
                    return 0
                while not io.get(pin1):
                    ## 等待通过第一脚
                    pass
                if io.get(pin2):
                    ## 同时离开两个脚，不能出现
                    return 0
                while not io.get(pin2):
                    pass
                return 1
            else:
                ## 其他情况输入错误
                return 0

    def mainloop(self):
        # Solution 0
        while 1:
            if io.get(self.monitor[0]):
                if self.passroad(self.monitor[0],self.monitor[1]):
                    client.send(self.clientcode+'+')
            if io.get(self.monitor[1]):
                if self.passroad(self.monitor[1],self.monitor[0]):
                    client.send(self.clientcode+'+')
            time.sleep(0.1)

        # Solution 1
        state = [0, 0] # 空闲状态
        enter = [False, False] # 在空闲状态，谁先被遮住
        leave = [False, False] # 在繁忙状态，谁先被释放
        while True: # 状态转移
            nxstate = [io.get(self.monitor[0]), io.get(self.monitor[1])]  # 次态
            if state == [0, 0]:
                enter = [nxstate[0] == '1', nxstate[1] == '1']
            else if state == [0, 1]:
                leave[1] = (not leave[0] and nxstate[1] == '0')
            else if state == [1, 0]:
                leave[0] = (not leave[1] and nxstate[0] == '0')
            else if state == [1, 1]:
                leave = [nxstate[0] == '0', nxstate[1] == '0']
            state = nxstate
            if enter != [False, False]:
                if enter == [True, False]: # 0首先被遮住
                    client.send(self.clientcode+'+')
                else if enter == [False, True]: # 1首先被遮住
                    client.send(self.clientcode+'-')
                else if enter == [True, True]: # 同时在空闲状态被遮住
                    if leave == [True, False]: # 0首先被释放
                        client.send(self.clientcode+'+')
                    else if leave == [False, True]: # 1首先被释放
                        client.send(self.clientcode+'-')
                enter = [False, False]
                leave = [False, False]
                state = [0, 0]
            # 其余情况，无法判断方向，直接忽略



if __name__ == "__main__":
    print "ok"
