#coding=utf-8
from django.core.management import BaseCommand

from core.ban.classes import BanHandler


class Command(BaseCommand):
    def handle(self, *args, **options):
        # This import was moved here to prevent cyclic import.
        from core.users.models import Users


        uid = None
        for arg in args:
            if 'uid' in arg:
                try:
                    uid = arg.split('=')[1]
                except (ValueError, IndexError):
                    self.stderr.write('It seems that uid was specified incorrect.')

        if not uid:
            self.stderr.write('Please, specify "uid" parameter. For example, uid=1000.')


        user = Users.objects.filter(id=uid)[:1]
        if not user:
            self.stderr.write("No user with exact id was found in database.")
            return

        user = user[0]


        self.stdout.write('User: {}'.format(user.full_name()))
        if not BanHandler.check_user(user):
            self.stderr.write('User is not banned.')
            return

        if BanHandler.liberate_user(user):
            self.stdout.write('OK. User was liberated successfully.')
        else:
            self.stderr.write('Unknown error: user was not liberated.')


