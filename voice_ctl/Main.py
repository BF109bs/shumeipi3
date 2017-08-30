#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import urllib
import urllib2
import time
import json
import requests
import re
import chardet
import random
import datetime
import thread
import signal
import Queue
import subprocess

import UCLogger
import RWLock
import VoiceIdentify

#path set
PROJECT_PATH = '/home/pi/sourcecode/fuzhuscript/voice_ctl/'
LOG_PATH = '/home/pi/sourcecode/fuzhuscript/voice_ctl/log'
SOURCE_FILE_ARECORD_PATH = '/home/pi/sourcecode/fuzhuscript/voice_ctl/voice/'

#queue set
SOURCE_FILE_QUEUE_SIZE = 3
START_FILE_QUEUE_SIZE = 1
STOP_FILE_QUEUE_SIZE = 1

#key set
START_STOP_KEY_TUPLE = ('音乐','天气','笑话','程序')

IS_RECORD_VOICE = True

g_running = True
def signHandle(signum, frame):
    global g_running
    if( signum in (signal.SIGINT,signal.SIGTERM)):
        g_running = False

def delIdentifyFaild(logger,result,filePath):
    logger.info('identifySound: faild. result=%s',result)
    rmCmd = 'sudo rm -rf ' + filePath
    os.system(rmCmd)

def selectStartStopKey(logger,result):
    num = len(START_STOP_KEY_TUPLE)
    '''
    if '小q' in result:
        pass
    else:
        return None
    '''
    i=0
    for key in START_STOP_KEY_TUPLE:
        if i == num :
            return None
        if key in result:
            return i
        else:
            i = i + 1


def recordSound( threadName, logger,sourceFileQueue, rwLock):
    #global IS_RECORD_VOICE
    i=1
    while g_running and True:
        if sourceFileQueue.full():
            time.sleep(1)
            continue;
        '''
        if IS_RECORD_VOICE == False:
            time.sleep(5)
            logger.info('recordSound: not record')
            continue;
        '''
        fileName = 'file'+ str(i) + '.wav'
        filePath = SOURCE_FILE_ARECORD_PATH + fileName
        arecordCmd = 'sudo arecord  -D plughw:1,0 -c 1 -d 5 ' + filePath + ' -r 8000 -f S16_LE 2 > /dev/null'
        os.system(arecordCmd) 
        try:
            rwLock.acquire_write()
        except  Exception, e:
            logger.info('recordSound: Exception: %s ', e)
            rmCmd = 'sudo rm -rf ' + filePath
            os.system(rmCmd)
            continue;
        
        try:
            sourceFileQueue.put(filePath, 0)
        except  Exception, e:
            logger.info('recordSound: Exception: %s ', e)
            rwLock.release()
            rmCmd = 'sudo rm -rf ' + filePathfilePath
            os.system(rmCmd)
            continue;
        
        try:
            rwLock.release()
        except  Exception, e:
            logger.info('recordSound: Exception: %s ', e)
            sourceFileQueue.get()
            rmCmd = 'sudo rm -rf ' + filePathfilePath
            os.system(rmCmd)
            scriptPath = PROJECT_PATH + 'script/stop_main.sh'
            os.system(scriptPath)
            #os.system('/home/pi/sourcecode/fuzhuscript/voice_ctl/script/kill_reset_main.sh')
        i = i + 1


def identifySound( threadName, logger,sourceFileQueue,startStopDict ,rwLockSourceFileQueue,rwLockStartStopDict):
    filePath = ''
    identify_ob = VoiceIdentify.VoiceIdentify()
    identify_ob.init( logger )
    while g_running and True:
        #'''
        if sourceFileQueue.empty():
            time.sleep(0.5)
            continue;
        if startStopDict['停止'].full():
            time.sleep(0.5)
            continue;
        if startStopDict['开始'].full():
            time.sleep(0.5)
            continue;
        
        try:
            rwLockSourceFileQueue.acquire_read()
        except  Exception, e:
            logger.info('identifySound: Exception: %s ', e)
            continue;
        
        try:
            filePath = sourceFileQueue.get(0)
        except  Exception, e:
            logger.info('identifySound: Exception: %s ', e)
            rwLock.release()
            continue;
        
        try:
            rwLockSourceFileQueue.release()
        except  Exception, e:
            logger.info('identifySound: Exception: %s ', e)
            scriptPath = PROJECT_PATH + 'script/stop_main.sh'
            os.system(scriptPath)
            #os.system('/home/pi/sourcecode/fuzhuscript/voice_ctl/script/stop_main.sh')
        #'''
        #result = identify_ob.identifyLocalFile('/home/pi/sourcecode/fuzhuscript/voice_ctl/voice/benfen/f2.wav','wav',8000, 'zh')
        result = identify_ob.identifyLocalFile(filePath,'wav',8000, 'zh')
        if result == None:
            delIdentifyFaild(logger,result,filePath)
            continue;
            
        logger.info('identifySound: %s ', result[0].encode("utf-8"))
        result = result[0].encode("utf-8")
        if '开始' in result:
            index = selectStartStopKey(logger,result)
            if index == None:
                delIdentifyFaild(logger,result,filePath)
                continue;
            logger.info('identifySound: %s ', START_STOP_KEY_TUPLE[index])
            rwLockStartStopDict.acquire_write()
            startStopDict['开始'].put(START_STOP_KEY_TUPLE[index])
            rwLockStartStopDict.release()
        elif '停止' in result:
            index = selectStartStopKey(logger,result)
            if index == None:
                delIdentifyFaild(logger,result,filePath)
                continue;
            logger.info('identifySound: %s ', START_STOP_KEY_TUPLE[index])
            rwLockStartStopDict.acquire_write()
            startStopDict['停止'].put(START_STOP_KEY_TUPLE[index])
            rwLockStartStopDict.release()
        else:
            delIdentifyFaild(logger,result,filePath)
        #time.sleep(30)

def stopSound( threadName, logger,startStopDict ,rwLockStartStopDict):
    sourcePath = PROJECT_PATH + 'VoiceSynthesis.py'
    while g_running and True:
        if startStopDict['停止'].empty():
            time.sleep(0.5)
            continue;
        
        rwLockStartStopDict.acquire_read()
        key = startStopDict['停止'].get( 0)
        rwLockStartStopDict.release()
        logger.info('stopSound: %s', key)
        index = selectStartStopKey(logger,key)
        if  index == 0: #停止音乐
            scriptPath = PROJECT_PATH + 'script/music_ctrl.sh'
            os.system(scriptPath)
            
            cmd = 'python ' + sourcePath + ' -v ' + '停止音乐完成'
            os.system(cmd)
            #os.system('/home/pi/sourcecode/fuzhuscript/voice_ctl/script/music_ctrl.sh')
            #os.system('/home/pi/sourcecode/fuzhuscript/voice_ctl/script/music_ctrl.sh')
        elif index == 1:#停止预报天气
            scriptPath = PROJECT_PATH + 'script/weather_ctrl.sh'
            os.system(scriptPath)
            #subprocess.call(scriptPath,shell=True)
            
            cmd = 'python ' + sourcePath + ' -v ' + '停止预报天气完成'
            os.system(cmd)
        elif index == 2: #停止笑话
            scriptPath = PROJECT_PATH + 'script/qiushibaike_ctrl.sh'
            os.system(scriptPath)
            #os.system(scriptPath)
            #subprocess.call(scriptPath,shell=True)
            
            cmd = 'python ' + sourcePath + ' -v ' + '停止笑话完成'
            os.system(cmd)
        elif index == 3: #停止程序
            cmd = 'nohup python ' + sourcePath + ' -v 停止程序完成 -t 6 &' 
            subprocess.call(cmd,shell=True)
            
            scriptPath = PROJECT_PATH + 'script/script_manage.sh'
            os.system(scriptPath)
            
        elif index == None:
            pass

def startSound( threadName, logger,startStopDict ,rwLockStartStopDict):
    sourcePath = PROJECT_PATH + 'VoiceSynthesis.py'
    while g_running and True:
        if startStopDict['开始'].empty():
            time.sleep(0.5)
            continue;
        
        rwLockStartStopDict.acquire_read()
        key = startStopDict['开始'].get( 0)
        rwLockStartStopDict.release()
        logger.info('startSound: %s', key)
        index = selectStartStopKey(logger,key)
        if  index == 0: #开始音乐
            sourcePath = 'python ' +PROJECT_PATH + 'music.py'
            os.system(sourcePath)
        elif index == 1:#开始天气
            sourceCmd = 'python ' + PROJECT_PATH + 'weather.py '
            os.system(sourceCmd)
        elif index == 2:#开始笑话
            sourcePath = 'python ' + PROJECT_PATH + 'qiushibaike.py'
            os.system(sourcePath)
        elif index == None:
            pass


if __name__ == '__main__':
    os.environ["TZ"] = 'Asia/Shanghai'
    time.tzset()
    reload(sys)
    sys.setdefaultencoding( "UTF-8")
    
    signal.signal(signal.SIGINT, signHandle)
    signal.signal(signal.SIGTERM, signHandle)    
    
    loggerMain = UCLogger.LoggerManager.GetAndConfigNoSingleInstance(module='Main',path= LOG_PATH )
    loggerRecordSound = UCLogger.LoggerManager.GetAndConfigNoSingleInstance(module='record_sound',path= LOG_PATH )
    loggerIdentifySound = UCLogger.LoggerManager.GetAndConfigNoSingleInstance(module='identify_sound',path= LOG_PATH )
    loggerStopSound = UCLogger.LoggerManager.GetAndConfigNoSingleInstance(module='stop_sound',path= LOG_PATH )
    loggerStartSound = UCLogger.LoggerManager.GetAndConfigNoSingleInstance(module='start_sound',path= LOG_PATH )
    
    sourceFileQueue = Queue.Queue(maxsize = SOURCE_FILE_QUEUE_SIZE)
    startStopDict = {}
    startQueue = Queue.Queue(maxsize = START_FILE_QUEUE_SIZE)
    stopQueue = Queue.Queue( maxsize = STOP_FILE_QUEUE_SIZE)
    startStopDict['开始'] = startQueue
    startStopDict['停止'] = stopQueue
    
    rwLockSourceFileQueue = RWLock.RWLock()
    rwLockStartStopDict = RWLock.RWLock()

    try:
        thread.start_new_thread( recordSound , ("record_sound", loggerRecordSound ,sourceFileQueue,rwLockSourceFileQueue) )
        thread.start_new_thread( identifySound , ("identify_sound", loggerIdentifySound  ,sourceFileQueue,startStopDict,rwLockSourceFileQueue,rwLockStartStopDict) )
        thread.start_new_thread( stopSound , ("stop_sound", loggerStopSound  ,startStopDict,rwLockStartStopDict) )
        thread.start_new_thread( startSound , ("start_sound", loggerStartSound  ,startStopDict,rwLockStartStopDict) )
    except:
        loggerMain.info('master process %d quit',os.getpid())
 
    while g_running and True:
        time.sleep(1)
    loggerMain.info('master process %d quit',os.getpid())



