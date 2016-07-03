#!/usr/bin/env python
# -*- coding:utf-8 -*-

import uuid

unique_id = lambda: str(uuid.uuid1())

class MessageServer(object):
    """消息服务器
    @param id: 服务器标识, 默认为 UUID
    """
    servers = {}
    
    def __init__(self, id=None):
        self.id = id if id else unique_id()
        self.observers = []
        self.messages = []
        self.__class__.servers[id] = self
    
    def listen(self, success_callback):
        self.observers.append(success_callback)
        return success_callback
    
    def add_message(self, message, id=None):
        if not id:
            id = unique_id()
        try:
            self.messages.append((id,message))
            [callback(id, message) for callback in self.observers]
        finally:
            self.observers = []
    
    
    