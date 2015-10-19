# coding=utf-8
from django.utils.timezone import now

from core.users.notifications.sms_dispatcher.models import SendQueue
from core.users.notifications.sms_dispatcher.senders.base import BaseSMSSender


class FromQueueSender(BaseSMSSender):
    @staticmethod
    def enqueue_message(message, phone_number, date):
        return SendQueue.enqueue(message, phone_number, date)
