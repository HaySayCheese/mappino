from django.core.management import BaseCommand

from core.billing.models import RealtorsAccounts



class Command(BaseCommand):
    def handle(self, *args, **options):
        print 'Started...'
        for account in RealtorsAccounts.all_with_fixed_plan():
            try:
                print 'Realtor: {0}, (Account ID: {1})'.format(account.user.full_name(), account.id)
                print 'Balance: {0}'.format(account.balance)
                account.process_fixed_payment()
                print 'New balance: {0}'.format(account.balance)

                print 'Success.'
                # todo: add log record here

            except Exception as e:
                print 'Error: {0}'.format(e)
                # todo: add log record here
        print 'Complete.'