#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys
import time
import json
import json
import subprocess
import threading

class myThread (threading.Thread):   #继承父类threading.Thread
        def __init__(self, threadID, name, delay, shellcmd):
                threading.Thread.__init__(self)
                self.threadID = threadID
                self.name = name
                self.delay = delay
                self.shellcmd = shellcmd
        def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
                #print "Starting " + self.name + self.shellcmd
                time.sleep(self.delay)
                subprocess.call(self.shellcmd , shell=True)
                #print "Exiting " + self.name +  self.shellcmd

if __name__ == "__main__" :
	reload(sys)
	sys.setdefaultencoding( "UTF-8")
        
        qiushibaike_thread = myThread(1, "qiushibaike_thread", 62,"/home/pi/sourcecode/fuzhuscript/Mor_Evening/script/qiushibaike_ctrl.sh")
        music_thread = myThread(2, "music_thread", 1,"/home/pi/sourcecode/fuzhuscript/Mor_Evening/script/music_ctrl.sh")
        #weather_thread = myThread(3, "weather_thread", 1,"/home/pi/sourcecode/fuzhuscript/Mor_Evening/script/weather_ctrl.sh")
        


        qiushibaike_thread.start()
        music_thread.start()
        #weather_thread.start()
        
        #print "Exiting Main Thread"


