from django.db import models



FREE_PUBLICATIONS_COUNT = 2.0

class Account(models.Model):
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    debt = models.DecimalField(max_digits=20, decimal_places=5, default=0)
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