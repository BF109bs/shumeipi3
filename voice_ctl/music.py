#!/usr/bin/python
#-*- coding: utf-8 -*-
import time, os, datetime
import random
import signal
import subprocess
LOG_PATH = '/home/pi/sourcecode/fuzhuscript/music.log'
IS_DEBUG=True
#IS_DEBUG=False

g_running = True
def signHandle(signum, frame):
    global g_running
    if( signum in (signal.SIGINT,signal.SIGTERM)):
        g_running = False
        exit(0)

def log(level, msg):
    log_msg = '[%s]: %s (%s)' % (level, msg, datetime.datetime.now() )
    if IS_DEBUG:
	print log_msg
	return 
    if level == 'DEBUG':
	return
    try:
	with open(LOG_PATH, 'a') as f:
	    f.write(log_msg+'\n')
    except Exception as e:
        print "Unable to log, %s" % e

def getMusic():
        music = os.popen('ls /home/pi/Music').read()  
        return music.split('\n')[:-1]

def selectMusic(musicjihe):
        index =  random.randint(0, len(musicjihe)-1)
        return musicjihe.pop(index)      

if __name__ == '__main__':
    os.environ["TZ"] = 'Asia/Shanghai'
    time.tzset()
    
    signal.signal(signal.SIGINT, signHandle)
    signal.signal(signal.SIGTERM, signHandle)    
    
    musicjihe = getMusic();
    log('INFO', 'start play music shero.mp3')
    while g_running and True: 
        if g_running == False:
            exit(0)
        
        if musicjihe == []:
                break
        music = selectMusic(musicjihe)
        musicpath = 'mplayer /home/pi/Music/'+ music
        os.system(musicpath)
        #str = os.popen('mplayer /home/pi/Music/3.mp3').read() 
        #log('INFO', str)
        time.sleep(1)
    log('INFO', 'quit.')
