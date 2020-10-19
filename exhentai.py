#-*- coding = utf-8 -*-
#@Time : 2020/10/3 0:01
#@Author : Chin
#@File : 爬取封面.py
#@Software : PyCharm
from selenium import webdriver #导入包
from bs4 import BeautifulSoup
import re
import os
import requests
import urllib.request,urllib.error #置顶URL，获取网页数据
from io import BytesIO
import gzip
import sys

findImg = re.compile(r'href="(.*?)">Download',re.S)
findUrl = re.compile(r'href="(.*?)" onclick',re.S)
findImg1 = re.compile(r'src="(.*?)" style',re.S)
findPage = re.compile(r'/ <span>(.*?)</span></div><a href',re.S)
findTitle = re.compile(r'<h1>(.*?)</h1>')


def main():
    url = input("请输入您要下载的图片第一页的网址 ：")
    baseurl = "%s"%url
    path = createPath(baseurl)
    getData(baseurl,path)
    # imgdownload(datalist,0)



def askURL_sel(url):
    path = r"E:\DEMO\douban\test1\msedgedriver.exe"
    driver = webdriver.Edge(executable_path=path)  #打开浏览器
    driver.get(url)  #输入url
    html = driver.page_source
    # print(html)
    return (html)

def askURL(url):
    head = {  # 模拟浏览器头部信息
        "cookie": "ipb_member_id=3803652; ipb_pass_hash=9f10ab7cbb8c43925381f85c95e39cb5; igneous=dfcef6f48; sl=dm_1; sk=hzfupteqlae4eujx2q47bds5wfra",
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）
    i = 0
    try:
        request = urllib.request.Request(url, headers=head)
        response = urllib.request.urlopen(request,timeout=5)
        html = response.read().decode("utf-8")
        return (html)
    # except:
    #     #解码压缩过的源代码
    #     # print("yon")
    #     request = urllib.request.Request(url, headers=head)
    #     response = urllib.request.urlopen(request,timeout=5)
    #     a = response.read()
    #     buff = BytesIO(a)  # 解码源代码
    #     f = gzip.GzipFile(fileobj=buff)
    #     html = f.read().decode("UTF-8")
    except:
        return i

def getData(url,path):
    datalist = []
    i = 0
    html = askURL(url)
    soup = BeautifulSoup(html, "lxml")
    # print(soup)
    item = soup.find_all("div", class_="sn")
    item = str(item)
    page = re.findall(findPage, item)[0]
    page = int(page)
    while i < page:
        html = askURL(url)
        i += 1
        if html == 0:
            i -= 1
            continue
        soup = BeautifulSoup(html, "lxml")
        try:
            # 原图
            item = soup.find_all("div",id="i7")
            data = []
            item = str(item)
            # print(item)
            img = re.findall(findImg,item)[0]
            img = str(img)
            img = img.replace("amp;","")
            print(img)
            imgdown(img, i, path)
            datalist.append(img)
            # print(datalist)
        except:
            # 压缩图
            item1 = soup.find_all("div", id="i3")
            item1 = str(item1)
            img = re.findall(findImg1,item1)[0]
            print(img)
            imgdown(img, i, path)
            datalist.append(img)
        item1 = soup.find_all("div",id="i3")
        item1 = str(item1)
        # print(item1)
        url = re.findall(findUrl,item1)[0]
        # print(url)
        # print(datalist)
        # 写入文件
        # file_handle = open('1.txt', mode='w+')
        # for ii in datalist:
        #     ii = str(ii) + "\n"
        #     file_handle.write(ii)
    return datalist

def getData_sel(url):
    datalist = []
    for i in range(1,41):
        url1 = url + str(i)
        print(url1)
        html = askURL_sel(url1)
        soup = BeautifulSoup(html, "lxml")
        for item in soup.find_all("img",id_="img"):
            data = []
            item = str(item)
            # print(item)
            img = re.findall(findImg,item)[0]
            print(str(img))
            datalist.append(img)
    return datalist

def createPath(url):
    html = askURL(url)
    soup = BeautifulSoup(html, "lxml")
    item = soup.find_all("div", class_="sni")
    item = str(item)
    title = re.findall(findTitle, item)[0]
    # print(title)
    path = "./%s" % title
    if not os.path.exists(path):  # 判断,是否存在此路径,若不存在则创建,注意这个创建的是文件夹
        os.mkdir(path)
        print("创建文件夹 %s"%title)
    return path


def imgdown(data,i,path):
    head = {  # 模拟浏览器头部信息
        "cookie": "ipb_member_id=3803652; ipb_pass_hash=9f10ab7cbb8c43925381f85c95e39cb5; igneous=dfcef6f48; sl=dm_1; sk=hzfupteqlae4eujx2q47bds5wfra",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36 Edg/86.0.622.43",
        "Host": "exhentai.org"
    }
    print("正在下载第 %d 张图片..."%i)
    res = requests.get(url=data,headers=head).content
    with open(path + "/" + str(i) + ".jpg", 'wb')as f:  # 以wb方式打开文件,b就是binary的缩写,代表二进制
        f.write(res)

def imgdownload(datalist,i):
    head = {  # 模拟浏览器头部信息
        "cookie": "ipb_member_id=3803652; ipb_pass_hash=9f10ab7cbb8c43925381f85c95e39cb5; igneous=dfcef6f48; sl=dm_1; sk=hzfupteqlae4eujx2q47bds5wfra",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36 Edg/86.0.622.43",
        "Host": "exhentai.org"
    }
    path = "./Pixiv R18 Apr 2019 Toplist"
    if not os.path.exists(path):  # 判断,是否存在此路径,若不存在则创建,注意这个创建的是文件夹
        os.mkdir(path)
    for data in datalist:
        i += 1
        print("正在下载第 %d 张图片..."%i)
        res = requests.get(url=data,headers=head).content
        with open(path + "/" + str(i) + ".jpg", 'wb')as f:  # 以wb方式打开文件,b就是binary的缩写,代表二进制
            f.write(res)

if __name__ == '__main__':
    main()