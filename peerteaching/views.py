from datetime import datetime
from time import sleep
from django.shortcuts import render
from wikidata.client import Client
from enum import Enum
from django.template.defaulttags import register
import json as simplejson
import ssl
import urllib.request
import os
import threading

#防止10060错误
ssl._create_default_https_context = ssl._create_unverified_context

@register.filter
def get_range(value):
    return range(value)

def index_out(request):
    # 从session 中取出 str json
    data = request.session.pop('jdata',False)
    # print("session11111", data, type(data))

    # str json 转为 json 对象
    json_dict = simplejson.loads(data)

    # return render(request,'output.html',{"data":data,"img_src":img_src})
