#coding=utf-8
import hashlib

import os
from PIL import Image
from django.conf import settings

from collective.exceptions import RuntimeException
from core.billing.abstract_models import FREE_PUBLICATIONS_COUNT
from core.users.exceptions import InvalidImageFormat, TooSmallImage
import core.publications.constants



class Avatar(object):
    destination = 'users/avatars/'
    directory = settings.MEDIA_ROOT + destination
    size = 180 #px


    def __init__(self, user):
        self.user = user


    def update(self, file):
        # check if destination dir is exists
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
            if not os.path.exists(self.directory):
                raise RuntimeException("Can't create destination directories.")

        # check file type
        if 'image/' not in file.content_type:
            file.close()
            raise InvalidImageFormat()

        # exclude .gif (pillow sometimes generates incorrect thumbs from .gif)
        if 'gif' in file.content_type:
            file.close()
            raise InvalidImageFormat()

        # saving the image
        salt = '94034782133244956047'
        uid_hash = hashlib.sha384(str(self.user.id) + salt).hexdigest()


        # Temporary image path is used to save newly uploaded image on the drive,
        # and to not rewrite existing user avatar before all checks and processing will be executed.
        temp_image_name = uid_hash + '.tmp.jpg'
        temp_image_path = os.path.join(self.directory, temp_image_name)
        with open(temp_image_path, 'wb+') as avatar:
            for chunk in file.chunks():
                avatar.write(chunk)

        # processing and scaling
        try:
            avatar = Image.open(temp_image_path)
        except IOError:
            os.remove(temp_image_path)
            raise RuntimeException('Unknown I/O error.')

        # check the minimum image size
        if (avatar.size[0] < self.size) or (avatar.size[1] < self.size):
            os.remove(temp_image_path)
            raise TooSmallImage()

        # the image is scaled/cropped vertically or horizontally depending on the ratio
        image_ratio = avatar.size[0] / float(avatar.size[1])
        ratio = 1
        if ratio > image_ratio:
            avatar = avatar.resize(
                (self.size, self.size * avatar.size[1] / avatar.size[0]), Image.ANTIALIAS)
            box = (0, (avatar.size[1] - self.size) / 2, avatar.size[0], (avatar.size[1] + self.size) / 2)
            avatar = avatar.crop(box)

        elif ratio < image_ratio:
            avatar = avatar.resize(
                (self.size * avatar.size[0] / avatar.size[1], self.size), Image.ANTIALIAS)
            box = ((avatar.size[0] - self.size) / 2, 0, (avatar.size[0] + self.size) / 2, avatar.size[1])
            avatar = avatar.crop(box)
        else:
            avatar = avatar.resize((self.size, self.size), Image.ANTIALIAS)

        # saving
        image_name = uid_hash + '.jpg'
        image_path = os.path.join(self.directory, image_name)

        avatar.save(temp_image_path, 'JPEG', quality=100)
        os.rename(temp_image_path, image_path)
        self.user.avatar_url = ''.join([settings.MEDIA_URL, self.destination, image_name])
        self.user.save()


    def url(self):
        return self.user.avatar_url



class Publications(object):
    def __init__(self, user):
        self.user = user


    def paid_count(self):
        """
        За поточною тарифною моделлю, декілька оголошень, що були опубліковані найраніше,
        вважаються безкоштовними для користувача.

        Даний метод повертає к-сть платних оголошень, які є в користувача.
        """
        count = 0
        for model in core.publications.constants.HEAD_MODELS.values():
            count += model.objects.filter(owner=self.user, is_paid=True).count()
        return count


    def free_count(self):
        """
        За поточною тарифною моделлю, декілька оголошень, що були опубліковані найраніше,
        вважаються безкоштовними для користувача.

        Даний метод повертає к-сть безкоштовних оголошень, які є в користувача.
        """
        count = 0
        for model in core.publications.constants.HEAD_MODELS.values():
            count += model.objects.filter(owner=self.user, is_paid=False).count()
        return count


    def total_count(self):
        """
        Повертає загальну к-сть оголошень всіх типів для поточного користувача.
        """
        count = 0
        for model in core.publications.constants.HEAD_MODELS.values():
            count += model.objects.filter(owner=self.user).count()
        return count


    def ensure_free_publications(self):
        """
        За поточною тарифною моделлю, декілька оголошень, що були опубліковані найраніше,
        вважаються безкоштовними для користувача.

        Даний метод призначений відновити цю к-сть оголошень, вибравши декілька найстаріших.
        Наприклад, після видалення одного з оголошень.
        """
        while self.free_count() < FREE_PUBLICATIONS_COUNT:
            oldest_record = None
            for model in core.publications.constants.HEAD_MODELS.values():
                try:
                    record = model.objects.filter(is_paid=True).only('created').order_by('created')[:1][0]
                except IndexError:
                    continue

                if oldest_record is None:
                    oldest_record = record
                else:
                    if record.created < oldest_record.created:
                        oldest_record = record

            if oldest_record is None:
                # user have no publications at all
                return

            oldest_record.is_paid = False
            oldest_record.save()


    def turn_off_paid_publications(self):
        """
        Зніме всі платні та опубліковані оголошення з публікації.
        Присвоїть всім їм статус "Вимкнено за відсутністю коштів на рахунку".
        """
        for model in core.publications.constants.HEAD_MODELS.values():
            for publication in model.objects.filter(owner=self.user, is_paid=True).only('id'):
                publication.turn_off_for_non_payment()