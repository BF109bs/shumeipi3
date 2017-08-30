#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys
import time
import random
import getopt

import urllib
import urllib2
import time
import json
import requests
import re
import chardet

#��ȡ�ٶ�����token
def get_token():
    api_key = "�ٶ�api_key"
    sec_key = "�ٶ�sec_key"
    url = url="https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id="+api_key+"&client_secret="+sec_key
    req = urllib2.Request(url)
    resp = urllib2.urlopen(req)
    context = resp.read().decode('utf-8')
    return json.loads(context)['access_token']

if __name__ == "__main__" :
    reload(sys)
    sys.setdefaultencoding( "UTF-8")
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "v:t:",['vstring=','delaytime=',])
    except Exception, e:
        print e
        sys.exit(2)
    
    voice_string = ''
    delaytime = 0
    for opt, arg in opts:
        if opt in ('--vstring','-v'):
            voice_string = arg
        if opt in ('--delaytime','-t'):
            delaytime  = arg
    
    #print voice_string
    token = get_token()
    per = random.randint(3,4) 
    url = "http://tsn.baidu.com/text2audio?tex="+voice_string+"&lan=zh&per=" + str(per) +"&pit=5&spd=4&cuid=b827ebcac3a8&ctp=1&tok="+token  #3Ϊ��кϳ�-����ң��4Ϊ��кϳ�-��ѾѾ
    if delaytime != 0:
        time.sleep(int(delaytime))
    os.system('/usr/bin/mplayer -cache-min 80 -volume 40 "%s"' %(url))


