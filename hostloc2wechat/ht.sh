#!/bin/bash
#判断进程是否存在，如果不存在就启动它
PIDS=`ps -ef |grep hostloc2wechat |grep -v grep | awk '{print $2}'`
if [ "$PIDS" != "" ]; then
	echo "myprocess is running!"
else

	python3 /app/hostloc2tg/hostloc2wechat.py &
fi

