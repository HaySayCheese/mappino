# coding=utf-8
import os
from django.core.management import BaseCommand
from django.utils.timezone import now

from core import redis_connections
from core.users.notifications.sms_dispatcher.models import SendQueue
from core.users.notifications.sms_dispatcher.senders.queued import FromQueueSender


class Command(BaseCommand):
    """
    Sends all queued sms notifications that are queued for today.
    It's also will send all notifications, that was not sent before.
    """

    @staticmethod
    def check_pid(pid):
        """ Check For the existence of a unix pid. """
        try:
            os.kill(pid, 0)
        except OSError:
            return False

        return True

    def handle(self, *args, **options):
        redis = redis_connections['cache']
        current_sender_pid = int(redis.get('sms_queue_sender'))
        if current_sender_pid is not None and self.check_pid(current_sender_pid):
            print('It seems that queue sender is already running.')
            exit(-1)

        else:
            redis.set('sms_queue_sender', os.getpid())

        today = now().date()
        enqueued_records = SendQueue.enqueued_for(today)
        if not enqueued_records:
            print('No enqueued SMS notifications for today.\n'
                  'It\'s also no missed notifications from earlier dates.')

        else:
            while enqueued_records:
                print('Notifications sending started...')

                for record in enqueued_records:
                    if FromQueueSender.process_transaction(record.phone_number, record.message):
                        print(u'Message sent: {message}; Phone number: {number}'.format(
                            message=record.message, number=record.phone_number))

                        record.delete()

                # get more new records if available
                enqueued_records = SendQueue.enqueued_for(today)

        print('Notifications sending has been finished.')

