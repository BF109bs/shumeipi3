#!/bin/bash
MYPID1=`ps -aux | grep "python Main.py" | awk {'print $2'}`

rm -rf /home/pi/sourcecode/fuzhuscript/voice_ctl/log/*
rm -rf /home/pi/sourcecode/fuzhuscript/voice_ctl/voice/*

kill -15  $MYPID1 


