# coding=utf-8
from django.core.management import BaseCommand

from core.managing.ban.classes import BanHandler
import csv


class Command(BaseCommand):
    def handle(self, *args, **options):
        # This import was moved here to prevent cyclic import.
        from core.users.models import Users
        # read realtors numbers from file: number_details[0] - realtor phone number,
        # number_details[1] - count of publications by current realtor

        file_with_numbers = open('mappino/grabbers/realtor_numbers_grabber/realtors_numbers.csv', 'r')
        csvreader = csv.reader(file_with_numbers, delimiter=' ', quotechar='|', quoting=csv.QUOTE_NONNUMERIC)

        for number_details in csvreader:
            # if user is not exist ban or add to suspicious list phone number,
            # else ban or add to suspicious list user
            user = Users.objects.filter(mobile_phone=number_details[0])[:1]
            if not user:
                self.stderr.write("No user with this phone number was found in database.")
                # if count of publications by current realtor == 2 add phone number to suspicious list
                if number_details[1] == 2:
                    if BanHandler.contains_suspicious_number(number_details[0]):
                        self.stderr.write('Phone number is already in suspicious list.')
                        continue
                    if BanHandler.add_suspicious_phone_number(number_details[0]):
                        self.stdout.write('OK. Number is added to suspicious list.')
                        continue
                    else:
                        self.stderr.write('Unknown error: phone number was not added to suspicious list.')
                # if count of publications by current realtor > 2 ban phone number
                else:
                    if BanHandler.contains_number(number_details[0]):
                        self.stderr.write('Phone number is already banned.')

                    if BanHandler.ban_phone_number(number_details[0]):
                        self.stdout.write('OK. Phone number banned.')
                    else:
                        self.stderr.write('Unknown error: phone number was not banned.')
            else:
                user = user[0]

                self.stdout.write(u'User: {0}'.format(user.full_name()))

                # if count of publications by current realtor == 2 add user to suspicious list
                if number_details[1] == 2:

                    if BanHandler.check_suspicious_user(user):
                        self.stderr.write('User is already in suspicious list.')

                    if BanHandler.add_suspicious_user(user):
                        self.stdout.write('OK. User is added to suspicious list.')
                    else:
                        self.stderr.write('Unknown error: user was not added to suspicious list.')

                # if count of publications by current realtor > 2 ban user
                else:
                    if BanHandler.check_user(user):
                        self.stderr.write('User is already banned.')

                    if BanHandler.ban_user(user):
                        self.stdout.write('OK. User banned.')
                    else:
                        self.stderr.write('Unknown error: user was not banned.')
