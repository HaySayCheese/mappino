# coding=utf-8
from django.views.generic.base import View
from collective.http.responses import HttpJsonResponse
from core.manager import manager_notifier

class PhotographersOrdersView(View):

    class Post(object):
        @staticmethod
        def ok():
            return HttpJsonResponse({
                'code' : 0,
                'message': "OK"
            })

    @classmethod
    def post(cls, request):
        phone_number = request.POST.get('phone_number')
        manager_notifier.send_photographer_request_notification(phone_number)
        return cls.Post.ok()