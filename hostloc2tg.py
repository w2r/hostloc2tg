# -*- encoding: utf-8 -*-

import requests
from urllib import parse
from lxml import etree
import time
import datetime
from requests.adapters import HTTPAdapter
import re
import js2py


# 获得cookie
def getcookies():
    url = 'https://www.hostloc.com/forum.php?mod=forumdisplay&fid=45&filter=author&orderby=dateline'
    js = js2py.EvalJs()
    headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'}
    aesjs = requests.get("https://www.hostloc.com/aes.min.js", headers=headers, timeout=5).text
    js.execute(aesjs)
    getcookie = requests.get(url).text
    getcookie_script = re.findall("<script>(.*?)</script>",getcookie)
    js.execute(getcookie_script[0].split("document")[0])
    data = js.toHex(js.slowAES.decrypt(js.c, 2, js.a, js.b))
    cookie = "L7DFW=" + data
    return cookie


# 获得日期
def get_week_day(date):
    week_day_dict = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期日',
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
            print("网络原因，无法访问，请稍后再试...")
            return "因权限原因，内容无法预览，请手动登陆查看！"


def mark_down(content):
    # 删除特殊符号，防止发生错误parse
    sign = ['&', '.', '<', '>', ' ', '?', '"', "'", '#', '%', '!', '@', '$', '^', '*', '(', ')', '-', '_', '+', '=', '~', '/', ',', ':', '’', '‘', '“', '”', '%', '^', '——', '{', '}', '*', '[', '、', '\\', ']', '`', '"', "'", '\n']
    for k in sign:
        content = content.replace(k, "")
    return content


def post(chat_id, text):
    try:
        text = parse.quote(text)
        post_url = 'https://api.telegram.org/bot********************_Lg65aNPbt78nsAgb0/sendMessage' \
                   '?parse_mode=MarkdownV2&chat_id={0}&text={1}'.format(chat_id, text)
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'}
        requests.get(post_url, headers=headers)
    except Exception:
        print("推送失败！")
        time.sleep(3)
        post(chat_id, text)


# 主程序
def master(r):
    xml_content = etree.HTML(r.content)
    href_list = xml_content.xpath('/html/body/div[@id="wp"]/div[5]/div/div/div[4]/div[2]/form/table/tbody/tr/th/a[3]/@href')
    author = xml_content.xpath('/html/body/div[@id="wp"]/div[5]/div/div/div[4]/div[2]/form/table/tbody/tr/td[2]/cite/a/text()')
    author_url = xml_content.xpath('/html/body/div[@id="wp"]/div[5]/div/div/div[4]/div[2]/form/table/tbody/tr/td[2]/cite/a/@href')
    number = xml_content.xpath('/html/body/div[@id="wp"]/div[5]/div/div/div[4]/div[2]/form/table/tbody/tr/td[3]/a/text()')
    href = xml_content.xpath('/html/body/div[@id="wp"]/div[5]/div/div/div[4]/div[2]/form/table/tbody/tr/th/a[3]/text()')
    print(author)
    print(number)
    for i in range(len(number)):
        if number[i] == '0':
            if str(href[i].replace("\r\n", "")) not in hostloc_list:
                hostloc_list.add(str(href[i].replace("\r\n", "")))
                name = href[i].replace("\r\n", "")
                # 文章链接
                # print(i)
                k = i + 1
                # print(k)
                url_list = "https://www.hostloc.com/{}".format(href_list[i])
                # 作者id链接
                url_author = "https://www.hostloc.com/{}".format(author_url[k])
                # 时间戳
                time_1 = time.strftime("%Y-%m-%d    %H:%M:%S", time.localtime())
                date_1 = get_week_day(datetime.datetime.now())
                time_2 = time_1 + '    ' + date_1 + '    '
                time2 = str(time_2).replace('-', '\\-')
                # 获得预览内容
                # print(get_content(url_list))
                content_2 = mark_down(get_content(url_list))
                text = '主        题：' + "***{}***".format(mark_down(name)) + '\n' + '发  布  者：[{0}]({1})'.format(mark_down(author[i + 1]), url_author) + '\n' + '时        间：' + time2 + '\n' + '内容预览：[点击查看——{0}]({1})'.format(content_2, url_list)
                print(text)
                # 修改为自己的想推送的ID
                post('*********', text)
            else:
                pass
        else:
            pass


# 副程序
def master_1(r):
    xml_content = etree.HTML(r.content)
    href_list = xml_content.xpath("//div[@class='threadlist']/ul/li/a/@href")
    author = xml_content.xpath("//span[@class='by']/text()")
    number = xml_content.xpath("//span[@class='num']/text()")
    href = xml_content.xpath("//div[@class='threadlist']/ul/li/a/text()")
    print(author)
    print(number)
    # print(href)
    # print(href_list)
    for i in range(len(number)):
        if number[i] == '0':
            if str(href[2 * i].replace("\r\n", "")) not in hostloc_list:
                hostloc_list.add(str(href[i * 2].replace("\r\n", "")))
                name = href[2 * i].replace("\r\n", "")
                # 转换链接：
                str_url = href_list[i].replace("forum.php?mod=viewthread&tid=", '').replace("&extra=page%3D1%26filter%3Dauthor%26orderby%3Ddateline&mobile=2", '')

                url_list = "https://www.hostloc.com/thread-{0}-1-1.html".format(str_url)
                # 时间戳
                time_1 = time.strftime("%Y-%m-%d    %H:%M:%S", time.localtime())
                date_1 = get_week_day(datetime.datetime.now())
                time_2 = time_1 + '    ' + date_1 + '    '
                time2 = str(time_2).replace('-', '\\-')
                # 获得预览内容
                # print(get_content(url_list))
                content_2 = mark_down(get_content_1(url_list))
                text = '主        题：' + "***{}***".format(mark_down(name)) + '\n' + '发  布  者：{0}'.format(mark_down(author[i])) + '\n' + '时        间：' + time2 + '\n' + '内容预览：[点击查看——{0}]({1})'.format(content_2, url_list)
                print(text)
                post('-1001427090413', text)
            else:
                pass
        else:
            pass


# 获得内容
def get_content_1(url):
    while True:
        try:
            headers = {
                'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'}
            requests.adapters.DEFAULT_RETRIES = 5
            s = requests.session()
            s.keep_alive = False
            result = 'L7DFW' in cookiestr
            if result:
                headers = {'Cookie': cookiestr, 'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; '
                                                              'Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                                                              '/46.0.2490.76 Mobile Safari/537.36'}
                r = s.get(url, headers=headers)
            else:
                r = s.get(url, headers=headers)
            xmlContent = etree.HTML(r.content)
            content = xmlContent.xpath('//div[@class="message"]/text()')
            return content[0].replace("\r\n", '').replace("\n", '').replace("\r", '').replace("\t", '').replace(" ", '')[0:80]

        except Exception as e:
            print("网络原因，无法访问，请稍后再试...")
            return "网络原因，无法访问，内容无法预览..."
            time.sleep(5)


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
            # 网站要求js验证(无法预览网页内容）
            cookiestr = getcookies()
            print(cookiestr)
            print("1")
            url = 'https://www.hostloc.com/forum.php?mod=forumdisplay&fid=45&filter=author&orderby=dateline'
            headers = {
                'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'}
            requests.adapters.DEFAULT_RETRIES = 5
            s = requests.session()
            s.keep_alive = False
            result = 'L7DFW' in cookiestr
            if result:
                headers = {'Cookie': cookiestr, 'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; '
                                                              'Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                                                              '/46.0.2490.76 Mobile Safari/537.36'}
                r = s.get(url, headers=headers)
            else:
                r = s.get(url, headers=headers)
            master_1(r)
            # 多少秒抓取一次网站，自己设定，不要太小，会被ban ip的
            time.sleep(20)
        except Exception as e:
            try:
                # 网站不要求js验证
                print("2")
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
                r = requests.get(url_hostloc, headers=headers)
                master(r)
                time.sleep(20)
            except Exception:
                print("网络错误，请稍后重试")
                time.sleep(120)





