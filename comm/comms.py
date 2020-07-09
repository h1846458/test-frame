#!/usr/bin/python
#-*- coding: utf-8 -*-
# @Time    : 2020/5/20 10:18
# @Author  : Rui.Hu
# @File    : comms.py

import cv2 as cv
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import base64
import pymysql
import requests
import json
import time
import datetime
import random

def cv2ImgAddText(img, text, left, top, textColor=(0, 255, 0), textSize=80):
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype("font/simsun.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text((left, top), text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv.cvtColor(np.asarray(img), cv.COLOR_RGB2BGR)

def setimageData(imagepath):
    with open(imagepath, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        s = base64_data.decode()
        #print('data:image/jpeg;base64:%s' % s.split(",")[0])
    img = Image.open(imagepath)
    return img.size, s.split(",")[0]

def getTimeStamp(n):
    return int(time.time() * 1000 - 1728000000) + n * 3600000

def getRandom():
    x1 = random.randint(0, 9)
    x2 = 10 * random.randint(0, 9)
    x3 = 100 * random.randint(0, 9)
    x4 = 1000 * random.randint(0, 9)
    x5 = 10000 * random.randint(0, 9)
    return x1 + x2 + x3 + x4 + x5


class httprequest:
    def __init__(self):
        self.ip = ""
        self.port = ""
        self.url = ""
        self.header = {
              'Accept': 'application/json,application/xml,application/xhtml+xml,text/html;q=0.9,image/webp,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate',
              'Authorization': 'Basic',
              'Accept-Language': 'zh-CN,zh',
              'Connection': 'keep-alive',
              'Content-Type': 'application/json;charset=utf-8',
              'User-Agent': "Mozilla/5.0"
        }
        self.httpurl = ''

    def setIp(self, ip):
        self.ip = ip

    def setPort(self, port):
        self.port = port

    def getUrl(self, url):
        return "http://" + self.ip + ":" + str(self.port) + url

    def setHeader(self, key, v):
        self.header[key] = v

    def setUrl(self, url):
        self.url = url
    def getRequst(self):
        httpurl = self.getUrl(self.url)
        req = requests.get(httpurl, headers=self.header)
        text = req.text
        #text = json.loads(text)
        return text

    def getToken(self, data):
        httpurl = self.getUrl(self.url)
        req = requests.post(url=httpurl, headers=self.header, data=data)
        text = req.text
        text = json.loads(text)
        self.setHeader("Authorization", text['data']['accessToken'])

    def postRequest(self, data):
        httpurl = self.getUrl(self.url)
        req = requests.post(url=httpurl, headers=self.header, data=data)
        text = req.text
        text = json.loads(text)
        return text


class mySqldb:
    def __init__(self, ip, port, login, password, db):
        self.ip = ip
        self.port = port
        self.login = login
        self.password = password
        self.db = db
        self.sql = ''

    def conectDb(self):
        self.sql = pymysql.connect(host=self.ip, port=self.port, user=self.login, passwd=self.password, db=self.db, charset='utf8')

    def getData(self, cmd):
        cursor = self.sql.cursor()
        cursor.execute(cmd)
        vlist = cursor.fetchall()
        return vlist

    def closeConect(self):
        self.sql.close()