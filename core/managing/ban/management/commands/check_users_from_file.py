# coding=utf-8
from django.core.management import BaseCommand

from core.managing.ban.classes import BanHandler
import csv


class Command(BaseCommand):
    def handle(self, *args, **options):
        # This import was moved here to prevent cyclic import.
        from core.users.models import Users
        file_with_numbers = open('../../../../../grabber/realtors_numbers.txt', 'r')
        csvreader = csv.reader(file_with_numbers, delimiter=' ', quotechar='|', quoting=csv.QUOTE_NONNUMERIC)
        for number_details in csvreader:
            user = Users.objects.filter(mobile_phone=number_details[0])[:1]
            if not user:
                self.stderr.write("No user with exact id was found in database.")
                return
            user = user[0]

            self.stdout.write('User: {}'.format(user.full_name()))

            if number_details[1] == 2:

                if BanHandler.check_suspicious_user(user):
                    self.stderr.write('User is already in suspicious list.')
                    return

                if BanHandler.add_suspicious_user(user):
                    self.stdout.write('OK. User is added to suspicious list.')
                else:
                    self.stderr.write('Unknown error: user was not added to suspicious list.')
            else:
                if BanHandler.check_user(user):
                    self.stderr.write('User is already banned.')
                    return

                if BanHandler.ban_user(user):
                    self.stdout.write('OK. User banned.')
                else:
                    self.stderr.write('Unknown error: user was not banned.')
