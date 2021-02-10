# -*- encoding: utf-8 -*-

import requests
from lxml import etree
import time
from urllib import parse


# 获得日期
def get_week_day(date):
    week_day_dict = {
        0: '周一',
        1: '周二',
        2: '周三',
        3: '周四',
        4: '周五',
        5: '周六',
        6: '周日',
    }
    day = date.weekday()
    return week_day_dict[day]


def get_content(url):
    while True:
        try:
            s = requests.get(url)
            hostloc_content = etree.HTML(s.content).xpath('//table/tr/td[@class="t_f"]/text()')

            if not hostloc_content:
                return "因权限原因，内容无法预览，请手动登陆查看！"
            else:
                s = ''
                for j in hostloc_content:
                    s = s + j
                # 不展示全部内容，防止内容过长，严重影响体验
                return s[0:80].replace("\r\n", '').replace('\n', '').replace('\xa0', '').replace('\u200b', '')

        except Exception as e:
            return "因权限原因，内容无法预览，请手动登陆查看！"


def mark_down(content):
    # 删除特殊符号，防止发生错误parse
    sign = ['&', '<', ".", '>', ' ', '?', '"', "'", '#', '%', '!', '@', '$', '^', '*', '(', ')', '-', '_', '+', '=', '~', '/', ',', ':', '’', '‘', '“', '”', '%', '^', '——', '{', '}', '*', '[', '、', '\\', ']', '`', '"', "'", '\n']
    for k in sign:
        content = content.replace(k, "")
    return content


# 主程序
def master(r):
    xml_content = etree.HTML(r)
    href_list = xml_content.xpath('/html/body/div[@id="wp"]/div[5]/div/div/div[4]/div[2]/form/table/tbody/tr/th/a[3]/@href')
    author = xml_content.xpath('/html/body/div[@id="wp"]/div[5]/div/div/div[4]/div[2]/form/table/tbody/tr/td[2]/cite/a/text()')
    author_url = xml_content.xpath('/html/body/div[@id="wp"]/div[5]/div/div/div[4]/div[2]/form/table/tbody/tr/td[2]/cite/a/@href')
    number = xml_content.xpath('/html/body/div[@id="wp"]/div[5]/div/div/div[4]/div[2]/form/table/tbody/tr/td[3]/a/text()')
    href = xml_content.xpath('/html/body/div[@id="wp"]/div[5]/div/div/div[4]/div[2]/form/table/tbody/tr/th/a[3]/text()')
    href_2 = xml_content.xpath('/html/body/div[7]/div[5]/div/div/div[4]/div[2]/form/table/tbody/tr/th/a[2]/text()')
    print(author)
    print(number)
    for i in range(len(number)):
        if number[i] == '0':
            href_id = href_list[i].split("tid=",)[-1].split("&",)[0]
            if str(href_id) not in hostloc_list:
                hostloc_list.add(str(href_id))
                name = href[i].replace("\r\n", "")
                # 判断是否为权限贴
                if name == "New":
                    name = href_2[i].replace("\r\n", "")
                else:
                    pass
                # 文章链接
                # print(i)
                k = i + 1
                # print(k)
                url_list = "https://www.hostloc.com/{}".format(href_list[i])
                # 作者id链接
                url_author = "https://www.hostloc.com/{}".format(author_url[k])
                # 时间戳
                time2 = time.strftime("%Y-%m-%d   %H:%M:%S", time.localtime())
                # 获得预览内容
                # print(get_content(url_list))
                content_2 = mark_down(get_content(url_list))
                text = '主        题：' + "{}".format(mark_down(name)) + '\n' + '发  布  者：' + '''<a href="{0}">{1}</a>'''.format(url_author, mark_down(author[i + 1])) + '\n' + '时        间：' + time2 + '\n' + '内容预览：' + '''<a href="{0}">点击查看——{1}</a>'''.format(url_list, content_2)
                # post(access_token, text)
                wx_url = "https://***********.qyu0615.workers.dev/"
                requests.get(wx_url + text)
            else:
                pass
        else:
            pass


hostloc_list = {"hello"}
url_1 = "https://www.hostloc.com/"

headers = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
}
url_hostloc = "https://www.hostloc.com/forum.php?mod=forumdisplay&fid=45&filter=author&orderby=dateline"

while True:
    try:
        # 网站不要求js验
        r = requests.get(url_hostloc, headers=headers)
        xml_content = etree.HTML(r.content)
        href_list = xml_content.xpath('/html/body/div[@id="wp"]/div[5]/div/div/div[4]/div[2]/form/table/tbody/tr/th/a[3]/@href')
        # 获得access_token
        print(href_list)
        if href_list:
            master(r.content)
            # 推送间隔
            time.sleep(15)
        else:
            # 网站启用js验证，进入休眠模式
            print("2")
            time.sleep(1800)

    except KeyError:
        print("网络错误，请稍后重试")
        time.sleep(30)



