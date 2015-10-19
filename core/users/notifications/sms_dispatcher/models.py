import phonenumbers
from django.db import models


class SendQueue(models.Model):
    """
    Customers doesn't like to receive notifications in middle of the night,
    but almost all processing of the customer's data will be done at night.

    So this queue is used to collect users sms notifications and to sent them
    in acceptable time interval of the day.
    """

    date_enqueued = models.DateField()
    message = models.TextField()
    phone_number = models.TextField()

    class Meta:
        db_table = 'users_notifications_sms_queue'

    @classmethod
    def enqueue(cls, message, phone_number, date_queued):
        """
        Adds message to the queue.

        :param message: body of the SMS.
        :param phone_number: number which should receive notification.
        :param date_queued: date when notification should be sent.
        """

        if not message:
            raise ValueError('Message can not be empty.')

        if not phone_number:
            raise ValueError('Phone number can not be empty.')

        try:
            parsed_number = phonenumbers.parse(phone_number)
            parsed_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        except phonenumbers.NumberParseException:
            raise ValueError('Phone number can not be parsed.')

        record = cls.objects.create(
            date_enqueued=date_queued, message=message, phone_number=parsed_number)
        return record

    @classmethod
    def enqueued_for(cls, date, include_previous_dates=True):
        """
        :param date: date to which messages was attached.
        :param include_previous_dates: if True all missed messages that was enqueue earlier will be included.
        :returns: all messages that should be sent on the :date.
        """

        if include_previous_dates:
            return cls.objects.filter(date_enqueued__lte=date)
        else:
            return cls.objects.filter(date_enqueued=date)






