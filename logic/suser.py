#-*-coding:utf-8 -*-
import json
import os
import sys
import time
if len(os.path.dirname(__file__)) > 0:
    path = os.path.dirname(__file__)
else:
    path = os.getcwd()
sys.path.append("%s/../logic/clazz/" % path)
sys.path.append("%s/../lib/" % path)
import vuser
import webutils

def Login(input):
    uid = webutils.GetParameter(input, "uid", "")
    usr = vuser.VUser(uid)
    usr.Load()
    return {"id": uid, "name":usr.nickname, "icon":usr.icon}

def Get(input):
    uid = webutils.GetParameter(input, "uid", "")
    usr = vuser.VUser(uid)
    usr.Load()
    return {"user":{
        "name": usr.name, "register":usr.birthday,
        "from":usr.GetSource(), "id":usr.id,
    }}

def Register(input):
    uid = webutils.GetParameter(input, "uid", "")
    usr = vuser.VUser(uid)
    try:
        usr.Load()
    except VCityException:
        pass
    if usr.IsExists:
        raise VCityException("usr already exists")
    usr.nickname = webutils.GetParameter(input, "name", "")
    usr.register_date = time()
    usr.Validate()
    usr.Save()
    return {"retcode":0, "uid":uid}

def AddScore(input):
    return {"retcode":0, "score":10}

def Location(input):
    return {"retcode":0, "location":{"altitude":10,"latitude":10}}
