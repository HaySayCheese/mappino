import hashlib
import uuid
from django.conf import settings
from django.db import models
from django.dispatch import Signal
from django.utils.timezone import now



class Account(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    tariff_plan_sid = models.PositiveSmallIntegerField()
    tariff_changed = models.DateTimeField(default=None, null=True)

    class Meta:
        abstract = True



class Transactions(models.Model):
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    datetime = models.DateTimeField(auto_created=True)
    type_sid = models.PositiveSmallIntegerField()

    class Meta:
        abstract = True


    @classmethod
    def transactions(cls):
        return cls.objects.all().order_by('-datetime')



class Orders(models.Model):
    class Constants(object):
        class States(object):
            new = 0
            success = 1
            failure = 2
            wait_secure = 3
            sandbox = 4


    #
    # fields
    #
    hash_id = models.TextField(
        default = lambda: hashlib.sha512(str(uuid.uuid4()) + settings.SECRET_KEY).hexdigest(),
        unique = True
    )
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    created = models.DateTimeField(default=now)
    status = models.SmallIntegerField(default=Constants.States.new)


    class Meta:
        abstract = True


    #
    # signals
    #
    accepted = Signal()


    @classmethod
    def orders(cls):
        return cls.objects.all().order_by('-created')


    def accept(self):
        """
        Marks order as successful.
        Emits signal "accepted".
        """
        self.status = self.Constants.States.success
        self.save()

        self.accepted.send(sender=self)