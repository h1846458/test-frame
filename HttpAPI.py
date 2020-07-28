#!/usr/bin/python
#-*- coding: utf-8 -*-
# @Time    : 2020/7/8 16:45
# @Author  : Rui.Hu
# @File    : HttpAPI.py
from .comm.comms import httprequest
import json
from .comm.comms import getTimeStamp

class HttpTest:
    def __init__(self):
        self.httprequst = ""
        self.text = ""

    def open_requst(self):
        self.httprequst = httprequest()

    def set_ip(self, ip):
        self.httprequst.setIp(ip)

    def set_header(self, k, v):
        self.httprequst.setHeader(k, v)

    def set_port(self, port):
        self.httprequst.setPort(port)

    def set_url(self, url):
        self.httprequst.setUrl(url)

    def get_token(self, url, data):
        return self.httprequst.getToken(url, data)

    def get_requst(self, url):
        if self.httprequst.ip != "":
            self.text = self.httprequst.getRequst(url)
        else:
            print("请先初始化Ip， port， url")

    def post_requst(self, url, data):
        if self.httprequst.ip != "":
            self.text = self.httprequst.postRequest(url, data)
        else:
            print("请先初始化Ip， port， url")

    def http_assert(self, key, message):
        if(self.__isjson()):
            json_object = json.loads(self.text)
            assert json_object[key] == message, "返回码："+json_object[key] + ",对比检验信息：" + message
        else:
            print("请求返回信息不是json格式数据")

    def __isjson(self):
        try:
            json_object = json.loads(self.text)
            return True
        except ValueError as e:
            return False

    def get_text(self):
        return self.text

