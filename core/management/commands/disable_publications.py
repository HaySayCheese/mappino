from django.core.management import BaseCommand
from django.db import transaction

from core.billing.models import RealtorsAccounts



class Command(BaseCommand):
    def handle(self, *args, **options):
        if not args:
            print 'Please, specify account ids (or ids)'


        with transaction.atomic():
            for account_id in args:
                account = RealtorsAccounts.objects.get(id=account_id)

                print 'Realtor: {0}, (Account ID: {1})'.format(account.user.full_name(), account.id)
                account.user.publications.turn_off_publications()
                print 'Disabled'