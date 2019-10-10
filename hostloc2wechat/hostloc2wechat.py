# -*- encoding: utf-8 -*-

import requests
from requests.adapters import HTTPAdapter
import js2py
import re
from lxml import etree
import time


def getcookies():
    url = 'https://www.hostloc.com/forum.php?mod=forumdisplay&fid=45&filter=author&orderby=dateline'
    js = js2py.EvalJs()
    headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'}

    try:
        aesjs = requests.get("https://www.hostloc.com/aes.min.js", headers=headers, timeout=5).text
    except Exception:
        return 'ReturnNothing'
    js.execute(aesjs)
    getcookie = requests.get(url).text
    getcookie_script = re.findall("<script>(.*?)</script>",getcookie)
    js.execute(getcookie_script[0].split("document")[0])
    data = js.toHex(js.slowAES.decrypt(js.c, 2, js.a, js.b))
    cookie = "L7DFW=" + data
    print(cookie)
    return cookie


hostloc_list = {"hello"}
cookiestr = getcookies()
try:
    while True:
        post_url = 'https://sc.ftqq.com/SCU63887T9e4e136f886e****************************f2.send?'
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
        xmlContent = etree.HTML(r.content)
        hrefList = xmlContent.xpath("//div[@class='threadlist']/ul/li/a/text()")
        author = xmlContent.xpath("//span[@class='by']/text()")
        number = xmlContent.xpath("//span[@class='num']/text()")
        href = xmlContent.xpath("//div[@class='threadlist']/ul/li/a/@href")
        for i in range(len(number)):
            if number[i] == '0':
                if str(hrefList[i * 2].replace("\r\n", "")) not in hostloc_list:
                    hostloc_list.add(str(hrefList[i * 2].replace("\r\n", "")))
                    text = hrefList[i * 2].replace("\r\n", "")
                    pid = re.findall(r'\d{6}', href[i])
                    url = "https://www.hostloc.com/thread-{}-1-1.html".format(int(pid[0]))
                    text_url = post_url + "text=" + text + " by " + author[i] + '&desp=[点我打开网页](' + url + ")"
                    requests.get(text_url)
                else:
                    pass
            else:
                pass
        time.sleep(30)

except Exception:
    pass


