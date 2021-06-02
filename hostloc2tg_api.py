# encoding=utf-8
"""
@Author  :   cherbim
@License :   清羽 (C) Copyright 2013-2019
@Contact :   qyu0615@gmail.com
@Software:   PyCharm
@Project ：  new_project_1
@File    :   1.py
@Time    :   2021/5/6 12:03
@User    ：   cherbim
"""
import requests
import time
from urllib import parse


def post_tg(url, count):
    try:
        r = requests.get(url)
        if '"ok":true,' in r.text:
            print('发送成功！')
            pass
        else:
            count = count + 1
            if count > 5:
                pass
            else:
                time.sleep(3)
                print("发送失败，正在重试")
                post_tg(url, count)
    except Exception:
        time.sleep(3)
        print("发送失败，正在重试")
        post_tg(url, count)


hostloc_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", ]
hostloc_title = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", ]
url_1 = "https://www.hostloc.com/"
while True:
    try:
        with requests.get('https://hostloc.cherbim.ml/', stream=True, timeout=5) as r:
            print(time.strftime("%m-%d %H:%M:%S", time.localtime()))
            for i in r.json()["new_data"][0][15:]:
                if i['主题ID'] in hostloc_list or i['主题'] in hostloc_title:
                    pass
                else:
                    hostloc_list = hostloc_list[1::]
                    hostloc_list.append(i['主题ID'])
                    hostloc_title = hostloc_title[1::]
                    hostloc_title.append(i['主题'])
                    a = "https://www.hostloc.com/thread-{0}-1-1.html".format(i['主题ID'])
                    time_1 = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime())
                    if "论坛bug，此贴内容无法查看~" not in i['主题内容'][0:100]:
                        a = a
                    else:
                        a = f"<s>{a}</s>"
                    text = '主        题：' + "<b>{}</b>".format(i['主题'].replace("&", "%26").replace("<", "%26lt%3b").replace(">", "%26gt%3b").replace("#", " ")) + '\n' + '发  布  者：' + '''<a href="{0}">{1}</a>'''.format(i['发布者链接'], i['发布者']) + '\n' + '时        间：' + time_1 + '\n' + '内容预览：' + '''<b>{0}</b>'''.format(i['主题内容'][0:100].replace("&", "%26").replace("<", "%26lt%3b").replace(">", "%26gt%3b").replace("#", " ")) + "\n" + "直达链接： " + a
                    print(text)
                    # 修改为你自己的bot api token和chat_id(可以是用户也可以是频道）
                    chat_id = "5*****1213"
                    bot_api_token = "1384839096:***************AksT60noQ"
                    tg_url = f"https://api.telegram.org/bot{bot_api_token}/sendMessage?parse_mode=HTML&chat_id=" + chat_id + "&text=" + text
                    b = 0
                    post_tg(tg_url, b)
            time.sleep(2)
    except Exception:
        print("网络错误，请稍后重试")
        time.sleep(5)


