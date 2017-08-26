#!/bin/bash
#echo "hello"
MYUSER=`whoami` 
#echo ${MYUSER}

declare -i i=0
while ((i<=240))
do
  sleep 1
  #echo $i
  let i++
done

MYPID1=`ps -aux | grep qiushibaike.py | awk {'print $2'}`
MYPID2=`ps -aux | grep '/usr/bin/mplayer -cache-min 80 -volume 40 "http://tsn.baidu.com/text2audio' |awk {'print $2'}`
MYPID3=`ps -aux | grep "/usr/bin/mplayer -cache-min 80 -volume 40 http://tsn.baidu.com/text2audio" |awk {'print $2'}`
kill -9  $MYPID1 $MYPID2 $MYPID3



