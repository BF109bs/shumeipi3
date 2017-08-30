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
from aip import AipSpeech

import UCLogger

# ���峣��
APP_ID = '�ٶ�app_id'
API_KEY = '�ٶ�api_key'
SECRET_KEY = '�ٶ�sec_key'

LOG_PATH = '/home/pi/sourcecode/fuzhuscript/log/'
#IS_DEBUG=False
IS_DEBUG=True

class VoiceIdentify():
    def __init__(self):
        self.app_id = APP_ID
        self.api_key= API_KEY
        self.sec_key= SECRET_KEY
    def __del__(self):
        pass
    
    def init(self,logger):
        self.logger = logger
        try:
            self.aip_speech = AipSpeech(self.app_id, self.api_key, self.sec_key)
        except Exception, e:
            self.logger.info('VoiceIdentify: init Exception: %s' , e)
            return False
        self.logger.info('VoiceIdentify: init sucess')
        return True
    
    '''
    �õ��ļ�buffer����
    filePath:type:string;   �ļ�·��
    return type: Buffer
    '''
    def getFileContent(self,filePath):
        try:
            with open(filePath, 'rb') as fp:
                ret_buffer = fp.read() 
        except Exception, e:
            self.logger.info('VoiceIdentify: getFileContent Exception: %s' , e)
            return None
        self.logger.info('VoiceIdentify: getFileContent sucess')
        return ret_buffer

    '''
    ʶ�𱾵��ļ�
    fileName:type:Buffer;       �ļ�����
    fileFormat:type:String;     �ļ�����,����pcm����ѹ������wav��amr
    fileRate:type:int;          �ļ������ʣ�֧�� 8000 ���� 16000
    fileContentLan:type:String; �ļ��������ԡ���������=zh������=ct��Ӣ��=en�������ִ�Сд��Ĭ������
    return type: dict
    '''
    def identifyLocalFile(self,fileName,fileFormat,fileRate,fileContentLan=None):
        ret_dict ={}
        try:
            ret_buffer = self.getFileContent(fileName)
            if ret_buffer == None:
                return None
            if fileContentLan == None:
                ret_dict =  self.aip_speech.asr(ret_buffer , fileFormat , fileRate, {
                                'lan': 'zh',
                            })
            else:
                ret_dict =  self.aip_speech.asr(ret_buffer, fileFormat , fileRate, {
                                'lan': fileContentLan,
                            })
        except Exception, e:
            self.logger.info('VoiceIdentify: identifyLocalFile Exception: %s' ,e)
        result = ret_dict.get('result',None)
        if result == None:
            self.logger.info('VoiceIdentify: identifyLocalFile error, %s',ret_dict)
        else:
            self.logger.info('VoiceIdentify: identifyLocalFile sucess')
        return result

    '''
    ʶ��URL�ļ�
    fileUrl:                    �ļ�url��ַ
    fileFormat:type:String;     �ļ�����,����pcm����ѹ������wav��amr
    fileRate:type:int;          �ļ������ʣ�֧�� 8000 ���� 16000
    callback:                   ʶ�����ص���ַ
    return type: dict
    '''
    def identifyUrlFile(self,fileUrl,fileFormat,fileRate, callback):
        ret_dict ={}
        try:
            ret_dict  = aipSpeech.asr('', fileFormat , fileRate, {
                            'url': fileUrl,
                            'callback': callback,
                        })
        except Exception, e:
            self.logger.info('VoiceIdentify: identifyUrlFile Exception: %s' , e)
        self.logger.info('VoiceIdentify: identifyUrlFile sucess')
        return ret_dict

if __name__ == '__main__':
    os.environ["TZ"] = 'Asia/Shanghai'
    time.tzset()
    reload(sys)
    sys.setdefaultencoding( "UTF-8")
    

    logger = UCLogger.LoggerManager.GetAndConfigNoSingleInstance(module='voice_identify',path= LOG_PATH )

    identify_ob = VoiceIdentify()
    identify_ob.init(logger)
    ret_dict = identify_ob.identifyLocalFile('./voice/f1.wav','wav',8000, 'zh')
    print ret_dict
    print ret_dict['result']
    print ret_dict['result'][0].encode("utf-8")



