import requests
import time


def mark_down(content):
    # 删除特殊符号，防止发生错误parse
    sign = ['&', '<', ".", '>', ' ', '?', '"', "'", '#', '%', '!', '@', '$', '^', '*', '(', ')', '-', '_', '+', '=', '~', '/', ',', ':', '’', '‘', '“', '”', '%', '^', '——', '{', '}', '*', '[', '、', '\\', ']', '`', '"', "'", '\n']
    for k in sign:
        content = content.replace(k, "")
    return content


hostloc_list = {"hello, hostloc!"}
url_1 = "https://www.hostloc.com/"
while True:
    try:
        r = requests.get("https://www.cherbim.ml")
        for i in r.json()["new_data"][0]:
            print(i)
            if i['主题ID'] in hostloc_list:
                pass
            else:
                hostloc_list.add(i['主题ID'])
                text = '主        题：' + "{}".format(mark_down(i['主题'])) + '\n' + '发  布  者：' + '''<a href="{0}">{1}</a>'''.format(i['发布者链接'], mark_down(i['发布者'])) + '\n' + '时        间：' + i['发布时间'].replace("    周五    ", "").replace("\\", "") + '\n' + '内容预览：' + '''<a href="{0}">点击查看——{1}</a>'''.format(i['主题链接'].replace("#lastpost", ""), mark_down(i['主题内容'][0:80]))
                # 需要修改为你自己反代的cf worker地址
                wx_url = "https://**************-f816.qyu0615.workers.dev/"
                print(text)
                try:
                    requests.get(wx_url + text)
                except Exception:
                    requests.get(wx_url + text)
    except KeyError:
        print("网络错误，请稍后重试")
        time.sleep(3)
