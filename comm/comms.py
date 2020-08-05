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
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json,os
import time
import redis
import random
import robot.utils.dotdict
import platform
from ctypes import *
facelist = []
class faceframe(Structure):
    _fields_ =[
        ('x', c_int),
        ('y', c_int),
        ('w', c_int),
        ('h', c_int),
        ('confidence', c_uint),
        ('angle', c_uint),
        ('base64origin', c_char_p),
        ('base64crop', c_char_p)
    ]

CALLBACK = CFUNCTYPE(None, POINTER(faceframe), c_char_p)

def CropImage4File(imagepath, faceinfo=[]):
    (path, filename) = os.path.split(imagepath)
    dest = os.path.join(path.decode("utf-8"), str(int(time.time()*1000)) + ".jpg")
    if os.path.isfile(imagepath):
        image = cv.imread(imagepath.decode("utf-8"))
        a = int(faceinfo[0])  # x start
        b = int(faceinfo[0]) + int(faceinfo[2])            # x end0
        c = int(faceinfo[1])   # y start
        d = int(faceinfo[1]) + int(faceinfo[3])             # y end
        cropImg = image[c:d, a:b]  # 裁剪图像
        pform = filename[-4:]
        base_str_crop = cv.imencode(pform.decode('utf-8'), cropImg)[1].tostring()
        base_str_origin = cv.imencode(pform.decode('utf-8'), image)[1].tostring()
        base64_origin = base64.b64encode(base_str_origin)
        base64_crop = base64.b64encode(base_str_crop)
        cv.imwrite(dest, cropImg)  # 写入图像路径
        return base64_origin, base64_crop
        #print(base64_str)
        #cv.imwrite(dest, cropImg)  # 写入图像路径

def _callback(para, imagepath):
    obj = para.__getitem__(0)
    facedict = {'x': obj.x,
                'y': obj.y,
                'w': obj.w,
                'h': obj.h,
                'confidence': obj.confidence,
                'angle': obj.angle,
                'base64origin': str(obj.base64origin, encoding='utf-8'),
                'base64crop': str(obj.base64crop, encoding='utf-8')
                }
    facelist.append(facedict)
    #faceinfo = [obj.x, obj.y, obj.w, obj.h]
    #tu_face = CropImage4File(imagepath, faceinfo)
    #print(facedict)

class facedetectdll:
    def __init__(self):
        self.libface = None
        if platform.system() == "Windows":
            self.libface = cdll.LoadLibrary("facedetec.dll")
        elif platform.system() == "Linux":
            self.libface = cdll.LoadLibrary("./so/cppdll.so")
        else:
            print(f"unknown platform.")
        return
    def facedetect(self, callback, imagepath):
        if(self.libface !=None):
            self.libface.facedetect.argtypes = [CALLBACK, c_char_p]
            self.libface.facedetect.restype = c_int
            imagepath = bytes(imagepath, "utf-8")
            #ret_str = self.libface.facedetect(imagepath).decode("utf8")
        return self.libface.facedetect(callback, imagepath)

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

def getimageData(imagepath, fl = 'header'):
    with open(imagepath, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        s = base64_data.decode()
        #print('data:image/jpeg;base64:%s' % s.split(",")[0])
    img = Image.open(imagepath)
    if(fl !='header'):
        return img.size, s  #.split(",")[0]
    else:
        if(s[0:3] == "iVB"):
            return img.size, "data:image/png;base64," + s
        elif(s[0:3] == "/9j"):
            return img.size, "data:image/jpeg;base64," + s

def getTimeStamp():
    return int(time.time() * 1000)

def getfacedetect(imagepath):
    faces = facedetectdll()
    callBackFunc = CALLBACK(_callback)
    #ret_str = faceframe()
    ret_str = faces.facedetect(callBackFunc, imagepath)
    if(ret_str ==0):
        return facelist

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
        #print(self.header)

    def setUrl(self, url):
        self.url = url


    def getRequst(self, url):
        httpurl = self.getUrl(url)
        print(self.header)
        req = requests.get(httpurl, headers=self.header)
        text = req.text
        #text = json.loads(text)
        return text

    def getToken(self, url, data):
        if (type(data) == robot.utils.dotdict.DotDict):
            data = json.dumps(data)
        elif (type(data) == type("")):
            data = json.loads(data)
        else:
            print("传入的数据格式不对=======================")
            return False
        httpurl = self.getUrl(url)
        req = requests.post(url=httpurl, headers=self.header, data=data)
        text = req.text
        #print(text)
        text = json.loads(text)
        return [text['data']['accessToken'], text['data']['businessId']]

    def postRequest(self, url, data):
        #index = robot.utils.dotdict.DotDict()
        if(type(data) == robot.utils.dotdict.DotDict or type(data) == dict):
            data = json.dumps(data)
        elif(type(data) == type("")):
            data = json.loads(data)
        else:
            print("传入的数据格式不对=======================")
            return False
        httpurl = self.getUrl(url)
        req = requests.post(url=httpurl, headers=self.header, data=data)
        text = req.text
        #text = json.loads(text)
        return text

    def uploadfile(self, url, multipart_encoder):
        # 这里根据服务器需要的参数格式进行修改
        self.header['Content-Type'] = multipart_encoder.content_type
        httpurl = self.getUrl(url)
        r = requests.post(url=httpurl, data=multipart_encoder, headers=self.header)
        text = r.text
        return text

    def setbody(self, filepath, index=None):
        if(index != None):
            multipart_encoder = MultipartEncoder(fields={'villageId': str(index), 'multipartFile': ('multipartFile', open(filepath, 'rb'), 'application/octet-stream')})
        else:
            multipart_encoder = MultipartEncoder(fields={'multipartFile': ('multipartFile', open(filepath, 'rb'), 'application/octet-stream')})
        return multipart_encoder

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

class redisdb:
    def __init__(self, ip, port, db, password, url):
        self.ip = ip
        self.port = port
        self.db = db
        self.passwd = password
        self.pool = ''
        self.url = url

    def connectRedis(self):
        self.pool = redis.ConnectionPool(host=self.ip, port=self.port, db=self.db, password=self.passwd)

    def getValue(self):
        req = requests.get("http://" + self.ip + self.url)
        text = req.json()
        #pool = redis.ConnectionPool(host=self.ip, port=self.port, db=10, password="1qaz!QAZ")
        CaptchaKey = text['data']['captchaKey']
        key = "VerifyCaptcha:" + text['data']['captchaKey']
        r = redis.StrictRedis(connection_pool=self.pool)
        value = str(r.get(key), encoding='utf-8')
        r.close()
        return [CaptchaKey, value]

    def closeRedis(self):
        pass

def getVerificationcode(ip, url):
    pt = 6379
    db = 10
    passwds = "1qaz!QAZ"
    red = redisdb(ip, pt, db, passwds, url)
    red.connectRedis()
    value = red.getValue()
    #CaptchaKey = red.captchaKey
    return value

class addstr:
	def __init__(self,value = ""):
		self.data = value
	def __add__(self,other):
		self.data += other


'''if __name__ == '__main__':
    tmp = "D:\\ProgramData\\Anaconda3\\envs\\CW-test-frame\\Lib\\site-packages\\CwtestLibrary\\comm\\opk.jpg"
    stl = getfacedetect(tmp)
    nparr = np.fromstring(base64.b64decode(facelist[0]['base64crop']), np.uint8)
    img_np = cv.imdecode(nparr, cv.IMREAD_COLOR)
    cv.imshow("test", img_np)
    cv.waitKey(0)'''
