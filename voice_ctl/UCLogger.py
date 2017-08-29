#!/usr/bin/env python
# -*-coding: UTF-8 -*-
import time, datetime
import sys,os
import threading
import logging
import logging.handlers

class LoggerManager:
	instance=None
	mutex=threading.Lock()
	def __init__(self):
		self.Logger = None
		self.log_path = ''
		self.fh=None
		self.module = None

	def __del__(self):
		pass
	
	@staticmethod
	def GetInstance( ):
		if(LoggerManager.instance==None):
			LoggerManager.mutex.acquire()
			if(LoggerManager.instance==None):
				logging.basicConfig(
						level=logging.NOTSET,
						filemode = 'a',
						format='%(asctime)s - %(process)d - %(module)s - %(levelname)s - %(message)s',
						)
				LoggerManager.instance = LoggerManager()
			LoggerManager.mutex.release()
		return LoggerManager.instance 
	
        #no single instance
	@staticmethod
        def GetInstanceNoSingle( ):
		LoggerManager.mutex.acquire()
		logging.basicConfig(
			level=logging.NOTSET,
			filemode = 'a',
			format='%(asctime)s - %(process)d - %(module)s - %(levelname)s - %(message)s',
			)
		LoggerManager.instance = LoggerManager()
		LoggerManager.mutex.release()
		return LoggerManager.instance 

	@staticmethod
	def Config(module='test',path='/var/log/'):
                t_logger = LoggerManager.GetInstance()
		t_logger._config(module,path)

	@staticmethod
        def GetAndConfigNoSingleInstance(module='test',path='/var/log/'):
                t_logger = LoggerManager.GetInstanceNoSingle()
                t_logger._config(module,path)
                return t_logger
                
	
	def _config(self,module,path):
		if self.Logger == None:
			self.Logger = logging.getLogger(module)
			if path[-1] == r'/':
				self.log_path = path
			else:
				self.log_path = path + '/'
			self.module = module
		logname = self.log_path  +  self.module +'-'+ str(os.getpid())+'.log'
		#self.fh = logging.handlers.TimedRotatingFileHandler(logname,'S',1,0)
		self.fh = logging.handlers.TimedRotatingFileHandler(logname,'midnight',1,0)
		self.fh.suffix = '%Y%m%d.log'
		self.fh.setLevel(logging.NOTSET)
		formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',datefmt='%H:%M:%S')
		self.fh.setFormatter(formatter)
		self.Logger.addHandler(self.fh)

	def debug(self,msg,*args,**kwargs):
		self.Logger.debug(msg,*args,**kwargs)
	
	def info(self,msg,*args,**kwargs):
		self.Logger.info(msg,*args,**kwargs)
	
	def warning(self,msg,*args,**kwargs):
		self.Logger.warning(msg,*args,**kwargs)
	
	def error(self,msg,*args,**kwargs):
		self.Logger.error(msg,*args,**kwargs)
	
	
if __name__ == '__main__':
	#先调用一次Config，设置日志目录和模块（日志文件前缀）
	LoggerManager.Config(path='/home/jiusen/log')
	logger = LoggerManager.GetInstance()
	while True:
		logger.info('s%s,%d'%('sss',12))
		logger.error('s%s,%d'%('error',12))
		time.sleep(1)
	
	sys.exit(0)

