#!/usr/bin/env python
# -*- coding: UTF-8 -*-
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
from lxml import etree
import signal

g_running = True
def signHandle(signum, frame):
    global g_running
    if( signum in (signal.SIGINT,signal.SIGTERM)):
        g_running = False

#获取百度语音token
def get_token():
        api_key = "百度api-key"
        sec_key = "百度sec-key"
        url = url="https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id="+api_key+"&client_secret="+sec_key
        req = urllib2.Request(url)
        resp = urllib2.urlopen(req)
        context = resp.read().decode('utf-8')
        return json.loads(context)['access_token']

def start(): 
	#out = open('qibai.json','w+')
        token=get_token()
	for page in range(2,63):
		#print page
                if page == 14:
                        break;

		url = 'http://www.qiushibaike.com/8hr/page/' + str(page) + "/"
		headers = {
	    	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
	    	'Accept-Language': 'zh-CN,zh;q=0.8'}
		item = {}
		try:
			response = requests.get(url, headers=headers)
			resHtml = response.text
			html = etree.HTML(resHtml)
			result = html.xpath('//div[contains(@id,"qiushi_tag")]')
			for site in result:
                                if g_running == False:
                                    exit(0)
				imgUrl    = site.xpath('.//a')[0].attrib['href']
				username  = site.xpath('.//h2')[0].text.encode('utf-8')
				#br标签截断文本内容
				content   = re.sub(r'<br />', '\n', etree.tostring(site.xpath('.//div[@class="content"]')[0],encoding='utf-8'))
				content   = re.sub(r'<.*?>', '', content).strip()
				vote      = site.xpath('.//i')[0].text.strip()
				comments  = site.xpath('.//i')[1].text.strip()

				#print '发布人：',username
				#print  '内容：',content
                                #print '点赞数：',vote
				#print '评论数：',comments
				#print '\n'
				
                                #item['name']=username
				#item['content']=content
				#item['vote']=vote
				#item['comments']=comments
				#print item['content']
				#line = json.dumps(item,ensure_ascii=False)
				#print line
				#out.write(line+'\n') 
                                
                                per = random.randint(3,4) 
                                url = "http://tsn.baidu.com/text2audio?tex="+content+"&lan=zh&per=" + str(per) +"&pit=5&spd=4&cuid=b827ebcac3a8&ctp=1&tok="+token  #3为情感合成-度逍遥，4为情感合成-度丫丫
                                #os.system('/usr/bin/mplayer -cache-min 80 -volume 40 "%s"' %(url))
                                os.system('/usr/bin/mplayer "%s"' %(url))
                                time.sleep(2)
		except Exception,e:
			print 'error',e
	#out.close()
if __name__ == "__main__" :
	reload(sys)
	sys.setdefaultencoding( "UTF-8")
        signal.signal(signal.SIGINT, signHandle)
        signal.signal(signal.SIGTERM, signHandle)    
        start()
	




