#-*- coding:utf-8 -*-
import requests
import re


def getHeaders(url, regex):
    headers={'User-Agent':
        'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36'}

    content = requests.get(url, headers = headers, timeout=10 ).text
    # print(content)
    info = re.findall(regex, content)
    for i in info:
        print(i)

if __name__ == '__main__':
    print("****************本科生院*****************")
    getHeaders('http://www.bkjx.sdu.edu.cn/default.site', 
        r'class="zxtz-bt" >\n(.*?)</div>')
    getHeaders('http://www.bkjx.sdu.edu.cn/default.site',
        r'title="(.*?)"')
    print("****************学生在线*****************")
    getHeaders('https://online.sdu.edu.cn/',
        r'<li><a target="_blank" title="(.*?)"')

    input()
 
