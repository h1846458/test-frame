#!/usr/bin/python
#-*- coding: utf-8 -*-
# @Time    : 2020/7/8 16:45
# @Author  : Rui.Hu
# @File    : HttpAPI.py
from .comm.comms import httprequest

class HttpTest:
    def __init__(self):
        self.httprequst = ""
        self.text = ""

    def openrequst(self):
        self.httprequst = httprequest()

    def setip(self, ip):
        self.httprequst.setIp(ip)

    def setheader(self, k, v):
        self.httprequst.setHeader(k, v)

    def setport(self, port):
        self.httprequst.setPort(port)

    def seturl(self, url):
        self.httprequst.setUrl(url)

    def getrequst(self):
        if self.httprequst.ip != "":
            self.text = self.httprequst.getRequst()
        else:
            print("请先初始化Ip， port， url")

    def postrequst(self):
        if self.httprequst.ip != "":
            self.text = self.httprequst.postRequst()
        else:
            print("请先初始化Ip， port， url")

    def httpassert(self, message):
        assert self.text != message, self.text