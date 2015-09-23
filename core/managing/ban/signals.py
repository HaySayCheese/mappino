#coding=utf-8
from django import dispatch


class BanHandlerSignals(object):
    # :args:
    #   user - record of the Users models
    user_banned = dispatch.Signal(providing_args='user')

    # :args:
    #   user - record of the Users models
    user_liberated = dispatch.Signal(providing_args='user')

    # :args:
    #   user - record of the Users models
    user_is_suspicious = dispatch.Signal(providing_args='user')
