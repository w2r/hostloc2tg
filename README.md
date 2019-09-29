### ***hostloc新帖推送机***

###### 简介：

一个推送新帖到telegram的python脚本。

###### 使用说明：

本脚本为python3脚本，需依赖环境requests，lxml等库

###### ht.sh文件说明：

由于hostloc有时开启防御模式，导致部分国外ip无法访问hostloc，导致掉线，后台运行一个自动重新连接脚本

使用方法：linux添加定时任务，ht.sh存放在root目录下

~~~
* */1 * * * /root/ht.sh
~~~



