### ***hostloc新帖推送机***

###### 简介：

迫于每次有活动都喝不上汤，特意搞了一个自动监视脚本，推送新帖到telegram的机器人，稍后有空补上推送到微信。

###### 使用说明：

本脚本为python3脚本，需依赖环境requests，lxml等库，第34行bot api需要改为自己的, 机器人每30秒更新一次

###### ht.sh文件说明：

由于hostloc有时开启防御模式，导致部分国外ip无法访问hostloc，getupdate错误导致掉线，后台运行一个自动重新连接脚本

使用方法：linux添加定时任务，ht.sh存放在root目录下，然后启动定时任务，注意，ht脚本里的里需要修改为你的hostloc2tg.py的路径

~~~
*/30 * * * * /root/ht.sh
~~~
![](https://i.postimg.cc/8CdGMXSV/cherbim-2019-10-10-06-17-33.jpg)


