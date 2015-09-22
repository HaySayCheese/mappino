# coding=utf-8


class ResourceThrottled(Exception): pass
class SMSSendingThrottled(ResourceThrottled): pass