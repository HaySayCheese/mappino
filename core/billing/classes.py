#coding=utf-8
import threading

from django.conf import settings
from core.billing.models import RealtorsAccounts



class BillingManager(object):
    def __init__(self):
        if not settings.THIS_NODE_HANDLES_BILLING:
            return

        self.timeout = 60*60

        # Важливо, щоб метод process_timer вперше був викликаний з під іншого потоку,
        # бо інакше - виникає помилка імпорту модуля users
        threading.Timer(self.timeout, self.process_timer).start()


    def process_timer(self):
        # Даний імпорт не зайвий,
        # він необхідний в потоці, який займається обрахунками біллінгу.
        import core.users


        RealtorsAccounts.process_fixed_realtors_plans()
        threading.Timer(self.timeout, self.process_timer).start()