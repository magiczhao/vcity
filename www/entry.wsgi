#!/usr/bin/env python
import json
import os
import sys
import web
import logging
path = os.path.dirname(__file__)
sys.path.append("%s/../logic/" % path)
sys.path.append("%s/../lib/" % path)

import logs
import serrcode
from webutils import GetParameter, GetProjectRoot
import suser
urls = ("/.*", "SocialEntry")

REQUEST_MAP = {
        "login" : "suser.Login",
        "get_user" : "suser.Get",
        "register" : "suser.Register",
        "add_score" : "suser.AddScore",
        "user_location" : "suser.Location",
        "get_subject" : "ssubject.Get",
        "set_subject" : "ssubject.Set",
        "get_feeds" : "sfeeds.GetList",
        "publish_feed" : "sfeeds.Publish",
        "comment_feed" : "sfeeds.Comment",
        "get_feed" : "sfeeds.Get",
        "get_messages" : "smessage.GetList",
        "publish_message" : "smessage.Publish",
        "comment_message" : "smessage.Comment",
        }

def DefaultOperation(input):
    errno = serrcode.UNKNOWN_OPERATION
    return {"retcode" : errno, "message" : serrcode.Strerror(errno)}

def UnknownError():
    errno = serrcode.UNKNOWN_OPERATION
    return {"retcode" : errno, "message" : serrcode.Strerror(errno)}

class SocialEntry:
    def GET(self):
        input = web.input()
        web.header("Content-Type", "application/json; charset=utf-8")
        request_type = GetParameter(input, "type", "login")
        output = None
        if request_type in REQUEST_MAP:
            module, function = REQUEST_MAP[request_type].split(".")
            logging.debug("module:%s, function:%s" % (module, function))
            if module in sys.modules:
                module_object = sys.modules[module]
                function_object = getattr(module_object, function)
                output = function_object(input)
        else:
            output = DefaultOperation(input)
        if output is None:
            output = UnknownError() 
        return json.dumps(output, ensure_ascii=False)

# run wsgi application
logs.SetupLog(dir = "%s/logs" % (GetProjectRoot()), project_name = "social")
application = web.application(urls, globals(), autoreload = True).wsgifunc()

if __name__ == "__main__":
    pass

