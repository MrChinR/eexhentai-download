# -*- coding = utf-8 -*-
#@Time : 2020/10/3 0:01
#@Author : Chin
#@File : 爬取封面.py
#@Software : PyCharm
from selenium import webdriver #导入包
from bs4 import BeautifulSoup
import re
import os, time, threading
import requests,sys
import urllib.request,urllib.error #置顶URL，获取网页数据
from queue import Queue
from tqdm import tqdm
import logging
from logging import handlers

findImg = re.compile(r'href="(.*?)">Download',re.S)
findUrl = re.compile(r'href="(.*?)" onclick',re.S)
findImg1 = re.compile(r'src="(.*?)" style',re.S)
findPage = re.compile(r'/ <span>(.*?)</span></div><a href',re.S)
findTitle = re.compile(r'<h1>(.*?)</h1>')
findfirstUrl = re.compile(r'<a href="(.*?)"><img')
findsize = re.compile(r'https.*?-(.*?)-')


def main():
    url = input("请输入您要下载的图片的起始页的网址 ：\n")
    baseurl = "%s"%url
    a = input("请输入您要下载的图片那一页的页码（若不需要指定页数请直接回车）：")
    if a == "":
        a = 1
    b = input("请输入您要要下载的最终页的页码（若不需要指定页数请直接回车）：")
    if b == "":
        b = 1
    firsturl = getfirstUrl(url,a)
    path = createPath(firsturl)
    log.logger.info("您要下载的起始页网址为：%s\n您要保存的地址是：%s,本次下载的图片为（全部为1-1）：%s-%s。"%(url,path,str(a),str(b)))
    getData(firsturl, path, a, b)


# 日志
class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }#日志级别关系映射

    def __init__(self,filename,level='info',when='D',interval=1,backCount=3,fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)#设置日志格式
        self.logger.setLevel(self.level_relations.get(level))#设置日志级别
        sh = logging.StreamHandler()#往屏幕上输出
        sh.setFormatter(format_str) #设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,interval=interval,backupCount=backCount,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        #实例化TimedRotatingFileHandler
        #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)#设置文件里写入的格式
        self.logger.addHandler(sh) #把对象加到logger里
        self.logger.addHandler(th)

def getfirstUrl(url,a):
    a = int(a)
    m = a // 40
    n = a % 40
    if n != 0:
        if m >= 1:
            url = url + "?p=%s"%m
    else:
        m -= 1
        if m >= 1:
            url = url + "?p=%s"%m
    html = askURL(url)
    while html == 0:
        html = askURL(url)
    soup = BeautifulSoup(html, "lxml")
    # print(soup)
    item = soup.find_all("div", id="gdt")
    item = str(item)
    # print(item)
    n -= 1
    firstUrl = re.findall(findfirstUrl,item)[n]
    print(firstUrl)
    return firstUrl

def askURL(url):
    head = {  # 模拟浏览器头部信息
        "cookie": r"%s"%cookie,
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    i = 0
    try:
        request = urllib.request.Request(url, headers=head)
        response = urllib.request.urlopen(request,timeout=8)
        html = response.read().decode("utf-8")
        return (html)
    except:
        return i

def getData(url,path,a,b):
    datalist = []
    html = askURL(url)
    soup = BeautifulSoup(html, "lxml")
    item = soup.find_all("div", class_="sn")
    item = str(item)
    page1 = re.findall(findPage, item)[0]
    page1 = int(page1)
    i = int(a)
    # print(i)
    page2 = int(b)
    url_queue = Queue()
    if page2 == 1:
        page = page1
    else:
        page = page2
    while i <= page:
        html = askURL(url)
        if html == 0:
            continue
        soup = BeautifulSoup(html, "lxml")
        try:
            item = soup.find_all("div",id="i7")
            item = str(item)
            img = re.findall(findImg,item)[0]
            img = str(img)
            img = img.replace("amp;","")
            # print(img)
            # imgdown(img, i, path)
            # single_thread_download(img, i, path)
            ManyDownload(url_queue,img, i, path,1)
            datalist.append(img)
        except:
            item1 = soup.find_all("div", id="i3")
            item1 = str(item1)
            img = re.findall(findImg1,item1)[0]
            # print(img)
            # imgdown(img, i, path)
            # single_thread_download(img, i, path)
            ManyDownload(url_queue,img, i, path,2)
            datalist.append(img)
        item1 = soup.find_all("div",id="i3")
        item1 = str(item1)
        url = re.findall(findUrl,item1)[0]
        i += 1
    return datalist


def createPath(url):
    html = askURL(url)
    soup = BeautifulSoup(html, "lxml")
    item = soup.find_all("div", class_="sni")
    item = str(item)
    title = re.findall(findTitle, item)[0]
    p = input("请输入您想要保存的文件完整路径： \n")
    path = "%s\%s" % (p,title)
    aa = ['?', '╲', '/', '*', '<', '>', '|']
    for itm in aa:
        path = path.replace(itm,'_')
    print(path)
    if not os.path.exists(path):  # 判断,是否存在此路径,若不存在则创建,注意这个创建的是文件夹
        os.mkdir(path)
        print("创建文件夹 %s"%title)
    return path


def imgdown(data,i,path):
    head = {  # 模拟浏览器头部信息
        "cookie": r"%s"%cookie,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36 Edg/86.0.622.43",
        "Host": "exhentai.org"
    }
    if os.path.exists(path + "/" + str(i) + ".jpg"):
        print("第 %d 张图片已存在。"%i)
        return
    print("第 %d 张图片加入下载线程..."%i)
    res = requests.get(url=data,headers=head).content
    with open(path + "/" + str(i) + ".jpg", 'wb')as f:  # 以wb方式打开文件,b就是binary的缩写,代表二进制
        f.write(res)

def single_thread_download(url, a ,dst, m):
    """
    @param: url to download file
    @param: dst place to put the file
    """
    # file_size = int(urlopen(url).info().get('Content-Length', -1))
    dst = dst + "/" + str(a) + ".jpg"
    header = {"cookie": r"%s" % cookie,
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36 Edg/86.0.622.43",
              "Host": "exhentai.org"
              }
    # file_size = int(requests.head(url).headers['Content-Length'])
    if m == 1:
        aaa = str(requests.head(url, headers=header).headers)
        size = re.findall(findsize, aaa)[0]
    if m == 2:
        aaa = url
        size = re.findall(findsize, aaa)[0]
    file_size = int(size)
    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)
        print("第 %d 张图片已存在。" % a)
    else:
        print("第 %d 张图片加入下载线程..." % a)
        first_byte = 0
    if first_byte >= file_size:
        return file_size
    header = {"Range": "bytes=%s-%s" % (first_byte, file_size),
              "cookie": r"%s" % cookie,
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36 Edg/86.0.622.43",
              "Host": "exhentai.org"
              }
    # pbar = tqdm(
    #     total=file_size, initial=first_byte,
    #     unit='B', unit_scale=True, desc=str(a) + ".jpg")  #url.split('/')[-1]
    req = requests.get(url, headers=header, stream=True)
    with(open(dst, 'ab')) as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    #             pbar.update(1024)
    # pbar.close()

def ManyDownload(url_queue,img, i, path,m):
    url_queue.put(img)
    for item in range(10):
        if url_queue.empty() == True:
            break
        url_img = url_queue.get()
        t = threading.Thread(target=single_thread_download, name='th-' + str(i),kwargs={'url': url_img,'a': i,'dst': path,'m': m})
        t.start()


if __name__ == '__main__':
    log = Logger('all.log', level='info')
    try:
        if not os.path.exists("./cookie.txt"):  # 判断,是否存在此路径,若不存在则创建,注意这个创建的是文件夹
            cookie = input("请输入您的cookie ：\n")
            file_handle = open('cookie.txt', mode='w+')
            file_handle.write(cookie)
            file_handle.close()
        else:
            with open('cookie.txt') as file:
                cookie = file.read()
                # print(cookie)
                file.close()
    # lock = threading.Lock()
        main()
    except Exception as e:
        log.logger.error(e)
