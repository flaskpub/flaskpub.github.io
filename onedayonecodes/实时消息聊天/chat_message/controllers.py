#!/usr/bin/env python
# -*- coding:utf-8 -*-

import web
import message
import json

msgsrv = message.MessageServer()
json_encoder = json.JSONEncoder()
json_encode = json_encoder.encode

class ChatPageController(web.Controller):
    def get(self):
        self.render("templates/message.html", msgs=reversed(msgsrv.messages))

class ChatMessageController(web.Controller):
    @web.asynchronous
    def get(self):
        @msgsrv.listen
        def observer(id, msg):
            update_msg = json_encode({'id':id,'msg':msg})
            try:
                self.finish(update_msg)
            except IOError:
                pass
    
    def post(self):
        name = unicode(self.get_argument("username")).strip()
        content = unicode(self.get_argument("content")).strip()
        msgsrv.add_message("%s: %s" % (name,content))
