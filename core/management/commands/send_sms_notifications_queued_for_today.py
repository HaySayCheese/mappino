# coding=utf-8
from django.core.management import BaseCommand
from django.utils.timezone import now

from core.users.notifications.sms_dispatcher.models import SendQueue
from core.users.notifications.sms_dispatcher.senders.queued import FromQueueSender


class Command(BaseCommand):
    def handle(self, *args, **options):
        today = now().date()
        enqueued_records = SendQueue.enqueued_for(today)
        if not enqueued_records:
            print('No enqueued SMS notifications for today.\n'
                  'It\'s also no missed notifications from earlier dates.')

        else:
            print('Notifications sending started...')

            for record in enqueued_records:
                if FromQueueSender.process_transaction(record.phone_number, record.message):
                    print('Message sent: {message}; Phone number: {number}'.format(
                        message=record.message, number=record.phone_number))

                    record.delete()

            print('Notifications sending has been finished.')
