#-*- coding: utf-8 -*-
# 
# Author Micheal Liu     2015-03-07
# Project core code, to control hardware device
# 
import io
import time
import client
from time import sleep
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
        myio.set(self.light, 0)
    
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
        # Solution 1: 因两传感器之间间隔很短，故不考虑“无->m0->无->m1->无”和"无->m1->无->m0->无"的情况
        state = [0, 0] # 空闲状态
        enter = [False, False] # 在空闲状态，谁先被遮住
        leave = [False, False] # 在繁忙状态，谁先被释放
        while True: # 状态转移
            nxstate = [myio.get(self.monitor[0]), myio.get(self.monitor[1])]  # 次态
            
            if state == [0, 0]:
                enter = [nxstate[0] == 1, nxstate[1] == 1]
            elif state == [0, 1]:
                leave[1] = (not leave[0] and nxstate[1] == 0)
            elif state == [1, 0]:
                leave[0] = (not leave[1] and nxstate[0] == 0)
            elif state == [1, 1]:
                leave = [nxstate[0] == 0, nxstate[1] == 0]
            print "st =", state, "nx =", nxstate, "enter =", enter, "leave =", leave
            state = nxstate

            flag = False # reset flag
            if enter != [False, False]:
                if enter == [True, False]: # 0首先被遮住
                    client.send(self.clientcode+'+')
                    flag = True
                    print "----->"
                elif enter == [False, True]: # 1首先被遮住
                    client.send(self.clientcode+'-')
                    flag = True
                    print "<-----"
                elif enter == [True, True]: # 同时在空闲状态被遮住
                    if leave == [True, False]: # 0首先被释放
                        client.send(self.clientcode+'+')
                        flag = True
                        print "----->"
                    elif leave == [False, True]: # 1首先被释放
                        client.send(self.clientcode+'-')
                        flag = True
                        print "----->"
                if flag:
                    enter = [False, False]
                    leave = [False, False]
            # 其余情况，无法判断方向，直接忽略
            sleep(0.1)



if __name__ == "__main__":
    ctrl = control()
    ctrl.mainloop()
