# 环境初始化
#killall vlc
#/usr/bin/amixer set PCM 80%

#/bin/su - pi -c '/usr/bin/nice -n -20 /usr/bin/nohup /usr/bin/cvlc --no-video --network-caching=1024 --audio-resampler 44100 --equalizer-preamp=10 --equalizer-bands="8 3 0 -2 -1 0.5 1.5 0.5 3 1.5" --compressor-attack=50 --compressor-release=500 --compressor-threshold=-20 --compressor-ratio=8 --compressor-knee=6 --compressor-makeup-gain=6 -L -I rc --rc-fake-tty --rc-host 127.0.0.1:8877 >/dev/null 2>&1 &'

# 启动电台
#sleep 6s
#echo volume 120 | /bin/nc -q 0 127.0.0.1 8877
#echo add 'http://lhttp.qingting.fm/live/4576/64k.mp3' | /bin/nc -q 0 127.0.0.1 8877

# 播放5分钟后停止
#sleep 5m
#killall vlc

# 插播天气预报
python /home/pi/sourcecode/fuzhuscript/Mor_Evening/weather.py 
#python /home/pi/sourcecode/fuzhuscript/Mor_Evening/weather.py  >> /dev/null 2>&1
#nohup python /home/pi/sourcecode/fuzhuscript/Mor_Evening/weather.py & >> /dev/null 2>&1
#sleep 120s
#/home/pi/sourcecode/fuzhuscript/Mor_Evening/script/weather_ctrl.sh

#启动脚本控制程序
nohup python script_manage.py &  >> /dev/null 2>&1

#播放音乐
python music.py  
#python music.py  >> /dev/null 2>&1

#播放笑话
python qiushibaike.py 
#python qiushibaike.py >> /dev/null 2>&1

/usr/bin/mplayer -cache-min 80 -volume 10 'http://tts.baidu.com/text2audio?lan=en&ie=UTF-8&spd=3&text="Good night!"'
