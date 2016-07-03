#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.web
import tornado.ioloop

IOLoopServer = tornado.ioloop.IOLoop.instance()
Application = tornado.web.Application
Controller = tornado.web.RequestHandler
StaticController = tornado.web.StaticFileHandler
asynchronous = tornado.web.asynchronous
