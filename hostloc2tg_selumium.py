# -*- encoding: utf-8 -*-
# 自行百度安装chrome和chromedriver
# 修改第89行， 修改自己的bot api token
# 修改第140行， 修改自己的推送id
# 修改第176行， 修改自己的Chromedriver路径
# 修改第187行， 修改自己的Chromedriver路径


import requests
from urllib import parse
from lxml import etree
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


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
    if a == 2:
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
    else:
        while True:
            try:
                browser.get(url)
                s = browser.page_source
                hostloc_content = etree.HTML(s).xpath('//td[@class="t_f"]/text()')

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
    sign = ['&', '<', ".", '>', ' ', '?', '"', "'", '#', '%', '!', '@', '$', '^', '*', '(', ')', '-', '_', '+', '=', '~', '/', ',', ':', '’', '‘', '“', '”', '%', '^', '——', '{', '}', '*', '[', '、', '\\', ']', '`', '"', "'", '\n']
    for k in sign:
        content = content.replace(k, "")
    return content


def post(chat_id, text):
    try:
        text = parse.quote(text)
        # 修改自己的bot api token
        post_url = 'https://api.telegram.org/bot854********************sAgb0/sendMessage' \
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
                time_1 = time.strftime("%Y-%m-%d    %H:%M:%S", time.localtime())
                date_1 = get_week_day(datetime.datetime.now())
                time_2 = time_1 + '    ' + date_1 + '    '
                time2 = str(time_2).replace('-', '\\-')
                # 获得预览内容
                # print(get_content(url_list))
                content_2 = mark_down(get_content(url_list))
                text = '主        题：' + "***{}***".format(mark_down(name)) + '\n' + '发  布  者：[{0}]({1})'.format(mark_down(author[i + 1]), url_author) + '\n' + '时        间：' + time2 + '\n' + '内容预览：[点击查看——{0}]({1})'.format(content_2, url_list)
                print(text)
                # 修改为自己的推送id
                post('-10********413', text)
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
n = 0
session = requests.session()

while True:
    try:
        # 网站不要求js验
        r = requests.get(url_hostloc, headers=headers)
        xml_content = etree.HTML(r.content)
        href_list = xml_content.xpath('/html/body/div[@id="wp"]/div[5]/div/div/div[4]/div[2]/form/table/tbody/tr/th/a[3]/@href')
        if href_list:
            a = 2
            print(a)
            master(r.content)
            time.sleep(15)
        else:
            a = 1
            print("js验证")
            # 网址
            url = 'https://www.hostloc.com/forum.php?mod=forumdisplay&fid=45&filter=author&orderby=dateline'
            # executable_path=r"/app/chromedriver"
            c_service = Service(executable_path=r"/app/chromedriver")
            c_service.command_line_args()
            c_service.start()
            c_options = Options()
            # 无界面浏览器
            c_options.add_argument('--no-sandbox')
            c_options.add_argument('--headless')
            c_options.add_argument('--disable-gpu')
            # executable_path=r"/app/chromedriver",
            # c_service = Service(executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
            # 修改为自己的chromedriver路径
            browser = webdriver.Chrome(executable_path=r"/app/chromedriver", chrome_options=c_options)

            browser.get(url)
            master(browser.page_source)
            browser.quit()
            c_service.stop()
            time.sleep(10)
    except Exception:
            print("网络错误，请稍后重试")
            time.sleep(60)




