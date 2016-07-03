#!/usr/bin/env python
# -*- coding:utf-8 -*-

from web import Application,IOLoopServer,StaticController
import controllers

app = Application([
    (r"/", controllers.ChatPageController),
    (r"/message/", controllers.ChatMessageController),
    (r"/static/(.*)", StaticController, {'path':'static/'}),
])

if __name__ == "__main__":
    app.listen(80)
    IOLoopServer.start()