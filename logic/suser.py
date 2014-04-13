#-*-coding:utf-8 -*-
import json

def Login(input):
    return {"retcode":0, "user":"magic",}

def Get(input):
    return {"retcode":0, "user":{
        "name":"magic", "register":"2014-04-01",
        "from":"qq", "id":"88888888", "level":10
    }}

def Register(input):
    return {"retcode":0, "user":"magic"}

def AddScore(input):
    return {"retcode":0, "score":10}

def Location(input):
    return {"retcode":0, "location":{"altitude":10,"latitude":10}}
