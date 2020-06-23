### ***hostloc新帖推送机***

###### 简介：

迫于每次有活动都喝不上汤，特意搞了一个自动监视脚本，推送新帖到telegram的机器人，稍后有空补上推送到微信（微信已废，懒得修改了）。

目前已开通了推送频道，可自行点击查看推送效果：https://t.me/hostloc2tg

###### 使用说明：

本脚本为python3脚本，需依赖环境requests，lxml，torequests等库，第59行bot api需要改为自己bot api，115行需要修改推送id, 机器人每15秒更新一次

**需要注册tg机器人，若要推送到频道，请将机器人添加到频道，并给予权限**

###### ht.sh文件说明：

由于hostloc有时开启防御模式，导致部分国外ip无法访问hostloc，getupdate错误导致掉线，后台运行一个自动重新连接脚本

使用方法：linux添加定时任务，**ht.sh存放在root目录下**，注意，ht脚本里的里需要修改为你的hostloc2tg.py的路径（**可不用设置后台运行，目前程序改版，解决了getupdate问题**）

~~~
*/30 * * * * /root/ht.sh
~~~
后台脚本内容：

~~~
#!/bin/bash
# 30分钟判断一次进程是否存在，如果不存在就启动它
# python3请使用全路径，否则可能出现无法启动
PIDS=`ps -ef |grep hostloc2tg |grep -v grep | awk '{print $2}'`
if [ "$PIDS" != "" ]; then
	echo "myprocess is running!"
else
	echo "未发现程序后台运行，正在重启中！"
	/usr/bin/python3 /root/hostloc2tg.py &
fi
~~~




