#!/bin/bash
#echo "hello"
MYUSER=`whoami` 
#echo ${MYUSER}

declare -i i=1
while ((i<=1))
do
  sleep 1
  #echo $i
  let i++
done

MYPID1=`ps -aux | grep "python /home/pi/sourcecode/fuzhuscript/voice_ctl/weather.py" | awk {'print $2'}`
MYPID2=`ps -aux | grep '/usr/bin/mplayer  "http://tsn.baidu.com/text2audio' | awk {'print $2'}`
MYPID3=`ps -aux | grep '/usr/bin/mplayer http://tsn.baidu.com/text2audio' | awk {'print $2'}`

kill -9  $MYPID1 $MYPID2 $MYPID3
#kill -10  $MYPID2 $MYPID1



