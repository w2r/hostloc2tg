import requests
import time
from urllib import parse


def mark_down(content):
    # 删除特殊符号，防止发生错误parse
    sign = ['&', '<', ".", '>', ' ', '?', '"', "'", '#', '%', '!', '@', '$', '^', '*', '(', ')', '-', '_', '+', '=', '~', '/', ',', ':', '’', '‘', '“', '”', '%', '^', '——', '{', '}', '*', '[', '、', '\\', ']', '`', '"', "'", '\n']
    for k in sign:
        content = content.replace(k, "")
    return content


def post_wechat(url, count):
    try:
        r = requests.get(url)
        print(r.text)
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
                post_wechat(url, count)
    except Exception:
        time.sleep(3)
        print("发送失败，正在重试")
        post_wechat(url, count)


hostloc_list = {"hello, hostloc!"}
hostloc_title = {"1"}
url_1 = "https://www.hostloc.com/"
start_time = time.time()
while True:
    try:
        r = requests.get("https://www.cherbim.ml")
        end_time = time.time()
        if end_time - start_time <= 600:
            pass
        else:
            local_time = time.strftime("%m-%d %H:%M:%S", time.localtime())
            print(local_time)
            start_time = end_time
        for i in r.json()["new_data"][0][15:]:
            if i['主题ID'] in hostloc_list or i['主题'] in hostloc_title:
                pass
            else:
                hostloc_list.add(i['主题ID'])
                hostloc_title.add(i['主题'])
                a = "https://www.hostloc.com/thread-{0}-1-1.html".format(i['主题ID'])
                time_1 = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime())
                if "论坛bug，此贴内容无法查看~" not in i['主题内容'][0:100]:
                    a = a
                else:
                    a = f"<s>{a}</s>"
                text = '主        题：' + "<b>{}</b>".format(i['主题']) + '\n' + '发  布  者：' + '''<a href="{0}">{1}</a>'''.format(i['发布者链接'], i['发布者']) + '\n' + '时        间：' + time_1 + '\n' + '内容预览：' + '''<b>{0}</b>'''.format(i['主题内容'][0:100].replace("&", "%26").replace("<", "%26lt%3b").replace(">", "%26gt%3b")) + "\n" + "直达链接： " + a
                print(text)
                # 修改为你自己的bot api token和chat_id
                # 切记群组id为负的
                chat_id = "5*****1213"
                bot_api_token = "1384839096:***************AksT60noQ"
                tg_url = f"https://api.telegram.org/bot{bot_api_token}/sendMessage?parse_mode=HTML&chat_id=" + chat_id + "&text=" + text

            # 控制重新发送次数，避免陷入死循环
                b = 0
                post_wechat(tg_url, b)
        time.sleep(3)
    except Exception:
        print("网络错误，请稍后重试")
        time.sleep(5)

