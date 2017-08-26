# -*- coding: utf-8 -*-
import os
import urllib
import urllib2,json
from datetime import date
from os import path
import sys

#数字转中文
def numtozh(num):
    num_dict = {1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七',
                8: '八', 9: '九', 0: '零'}
    num = int(num)
    if 100 <= num < 1000:
        b_num = num // 100
        s_num = (num-b_num*100) // 10
        g_num = (num-b_num*100) % 10
        if g_num == 0 and s_num == 0:
            num = '%s百' % (num_dict[b_num])
        elif s_num == 0:
            num = '%s百%s%s' % (num_dict[b_num], num_dict.get(s_num, ''), num_dict.get(g_num, ''))
        elif g_num == 0:
            num = '%s百%s十' % (num_dict[b_num], num_dict.get(s_num, ''))
        else:
            num = '%s百%s十%s' % (num_dict[b_num], num_dict.get(s_num, ''), num_dict.get(g_num, ''))
    elif 10 <= num < 100:
        s_num = num // 10
        g_num = (num-s_num*10) % 10
        if g_num == 0:
            g_num = ''
        num = '%s十%s' % (num_dict[s_num], num_dict.get(g_num, ''))
    elif 0 <= num < 10:
        g_num = num
        num = '%s' % (num_dict[g_num])
    elif -10 < num < 0:
        g_num = -num
        num = '零下%s' % (num_dict[g_num])
    elif -100 < num <= -10:
        num = -num
        s_num = num // 10
        g_num = (num-s_num*10) % 10
        if g_num == 0:
            g_num = ''
        num = '零下%s十%s' % (num_dict[s_num], num_dict.get(g_num, ''))
    return num

def get_city_id(cityname, search_type=1):
    ids = ''
    if search_type == 1:# 查询城市ID
        search = 'allchina'
        fn0 = 'cityID'
    elif search_type == 0:# 查询景点ID
        fn0 = 'viewID'
        search = 'allattractions'
    else:
        # 代表type值出错
        return -1
    fn = fn0+str(date.today())+'.txt'
    try:
        if path.exists(fn):
            fp = open(fn, 'r')
            context = fp.read()
            fp.close()
        else:
            fp = open(fn, 'w')
            url_city = 'https://free-api.heweather.com/v5/citylist?search='+search+'&key=和风天气key'
            req = urllib2.Request(url_city)
            resp = urllib2.urlopen(req)
            context = resp.read().decode('utf-8')
            # print True
            fp.write(context)
            fp.close()
        city_json = json.loads(context,encoding='utf-8')
        city_info = city_json["city_info"]
        city_name = unicode(cityname, 'utf-8')
        # print city_name
        for index, cities in enumerate(city_info):
            if city_name in cities['city']:
                print cities['city']
                ids = cities['id']
                break
        else:
            # 之后将会返回-1
            print '您输入的城市或景点不存在，请反馈给管理员'
    except IOError, e:
        print e
    else:
        pass
    return ids


#返回和风天气数据
def get_city_weather(index, search_type=1):
    if search_type == 1:
        search = 'weather'
    elif search_type == 0:
        search = 'attractions'
    else:
        return -1
    url_weather = 'https://free-api.heweather.com/v5/'+search+'?city='+index+'&key=和风天气key'
    req = urllib2.Request(url_weather)
    resp = urllib2.urlopen(req)
    context = resp.read()
    weather_json = json.loads(context, encoding='utf-8')
    #fp = open("/home/Morning/temp/test.txt", 'w')
    fp = open("/home/pi/sourcecode/fuzhuscript/Mor_Evening/temp/test.txt", 'w')
    fp.write(context)
    fp.close()
    if search_type == 1:
        #weather = weather_json["HeWeather5"][0]['daily_forecast'][0] #这是取的是当天的天气
        weather = weather_json["HeWeather5"][0]
    else:
        weather = weather_json
    return weather


#获取百度语音token
def get_token():
    api_key = "百度api_key'"
    sec_key = "百度sce_key"
    url = url="https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id="+api_key+"&client_secret="+sec_key
    req = urllib2.Request(url)
    resp = urllib2.urlopen(req)
    context = resp.read().decode('utf-8')
    return json.loads(context)['access_token']


#获取需要的数据
def get_wat():
    city_id = "城市代码"  #城市代码   
    city_weather = get_city_weather(city_id)
    
    #当天的整体天气
    city_weather_weather = city_weather['daily_forecast'][0]
    a= numtozh( city_weather_weather['tmp']['max'] ) #最高温度
    b= numtozh( city_weather_weather['tmp']['min'] ) #最低温度
    c= city_weather_weather['cond']['txt_d']         #日间天气
    d= city_weather_weather['cond']['txt_n']         #夜间天气
    e= city_weather_weather['date']                  #日期
    f= city_weather_weather['wind']['dir']           #风向
    g= city_weather_weather['wind']['sc']            #风力
    h= numtozh( city_weather_weather['wind']['spd']) #风速
    weather_str = "早上好,今天是{0},最高温度{1}度,最低温度{2}度,日间天气{3},夜间天气{4},风向{5},风力{6},风速{7}级;".format(e,a,b,c,d,f,g,h)
   
    #实况天气
    city_weather_now = city_weather['now']
    a= city_weather_now['cond']['txt']               #天气状况描述
    b= numtozh(city_weather_now['pres'] )            #气压
    c= numtozh(city_weather_now['tmp'] )             #温度
    d= numtozh(city_weather_now['vis'])              #能见度
    e= city_weather_now['wind']['dir']               #风向
    f= city_weather_now['wind']['sc']                #风力
    g= numtozh( city_weather_now['wind']['spd'])     #风速
    weather_now_str = "目前天气{0},气压{1}帕斯卡,温度{2}度,能见度{3},风向{4},风力{5},风速{6}级;".format(a,b,c,d,e,f,g)


    #当天的空气质量
    city_weather_aqi = city_weather['aqi']
    a = numtozh( city_weather_aqi['city']['aqi'])    #空气AQI指数
    b = numtozh( city_weather_aqi['city']['pm25'])   #空气pm25指数
    c = city_weather_aqi['city']['qlty']             #空气质量
    aqi_str = "今天空气AQI指数{0},PM2.5指数{1},空气质量{2};".format(a,b,c)

    #灾害预警
    city_alarms = city_weather.get('alarms',None)
    if city_alarms == None:
        city_alarms_str = "目前无城市预警;"
    else:
        a = city_alarms['title']                     #预警信息
        b = city_alarms['type']                      #预警类型
        c = city_alarms['level']                     #预警等级
        d = city_alarms['stat']                      #预警状态
        e = city_alarms['txt']                       #预警信息详情
        city_alarms_str = "城市预警信息{0},预警类型{1},预警等级{2},预警状态{3},预警信息详情{4};".format(a,b,c,d,e)
   
    #生活建议
    city_suggestion = city_weather['suggestion']
    a = city_suggestion['comf']['brf']                    #舒适度指数
    a_specific = city_suggestion['comf']['txt']           #舒适度解释
    b = city_suggestion['drsg']['brf']                    #穿衣指数
    b_specific = city_suggestion['drsg']['txt']           #穿衣建议
    c = city_suggestion['flu']['brf']                     #感冒指数
    c_specific = city_suggestion['flu']['txt']            #防感冒建议
    d = city_suggestion['sport']['brf']                   #运动指数
    d_specific = city_suggestion['sport']['txt']          #运动建议
    e = city_suggestion['trav']['brf']                    #旅游指数
    e_specific = city_suggestion['trav']['txt']           #旅游建议
    city_suggestion_str = "舒适度指数{0},因为{1}穿衣指数{2},穿衣建议{3}感冒指数{4},防感冒建议{5}运动指数{6},运动建议{7}旅游指数{8},旅游建议{9};".format(a,a_specific,b,b_specific,c,c_specific,d,d_specific,e,e_specific) 
    
    #明天的整体天气
    city_weather_weather = city_weather['daily_forecast'][1]
    a= numtozh( city_weather_weather['tmp']['max'] ) #最高温度
    b= numtozh( city_weather_weather['tmp']['min'] ) #最低温度
    c= city_weather_weather['cond']['txt_d']         #日间天气
    d= city_weather_weather['cond']['txt_n']         #夜间天气
    e= city_weather_weather['date']                  #日期
    f= city_weather_weather['wind']['dir']           #风向
    g= city_weather_weather['wind']['sc']            #风力
    h= numtozh( city_weather_weather['wind']['spd']) #风速
    weather_tomorrow_str = "明天是{0},最高温度{1}度,最低温度{2}度,日间天气{3},夜间天气{4},风向{5},风力{6},风速{7}级.".format(e,a,b,c,d,f,g,h)
  
    return weather_str + weather_now_str + aqi_str + city_alarms_str + city_suggestion_str + weather_tomorrow_str

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    token=get_token()
    weather=get_wat()
    print weather    

    #tts
    #url = "http://tsn.baidu.com/text2audio?tex="+weather+"&lan=zh&per=3&pit=5&spd=4&cuid=b827ebcac3a8&ctp=1&tok="+token #男声
    url = "http://tsn.baidu.com/text2audio?tex="+weather+"&lan=zh&per=4&pit=5&spd=4&cuid=b827ebcac3a8&ctp=1&tok="+token  #女声

    #播放
    try:
        #os.system('/home/pi/sourcecode/fuzhuscript/Mor_Evening/vlc/volume-drop.sh')
        os.system('/usr/bin/mplayer -cache-min 80 -volume 40 "%s"' %(url))
        #os.system('/home/pi/sourcecode/fuzhuscript/Mor_Evening/vlc/volume-rise.sh')

    except Exception as e:
        print('Exception',e)
