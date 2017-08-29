#!/bin/bash
MYPID1=`ps -aux | grep "python Main.py" | awk {'print $2'}`

kill -9  $MYPID1 
