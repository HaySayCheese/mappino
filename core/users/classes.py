#coding=utf-8
import os
import uuid

from PIL import Image
from django.conf import settings

from core.google_cloud_storage import GoogleCSPhotoUploader
from core.users.exceptions import AvatarExceptions


class Avatar(GoogleCSPhotoUploader):
    avatar_suffix = '_processed'
    avatar_size = 180

    original_image_suffix = '_original'
    min_original_image_size = avatar_size

    bucket_path = GoogleCSPhotoUploader.bucket + '/users/photos/'


    def __init__(self, user):
        self.user = user


    def update(self, image):
        url =  self.process_and_upload_to_gcs(image)
        self.user.avatar_url = url
        self.user.save()
        return url


    def url(self):
        return self.user.avatar_url


    @classmethod
    def process_and_upload_to_gcs(cls, img):
        """
        Processes avatar and uploads it to the GCS.

        :return:
            public links to the avatar.
        """

        # check file size
        if img.size > 1: # 1024 * 1024 * 5: # 5mb
            img.close()
            raise AvatarExceptions.ImageIsTooLarge()

        # check file type
        if 'image/' not in img.content_type:
            img.close()
            raise AvatarExceptions.UnsupportedImageType('Not an image.')

        # exclude .gif'name': bucket_filename,
        # pillow sometimes generates incorrect thumbs from .gif
        if 'gif' in img.content_type:
            img.close()
            raise AvatarExceptions.UnsupportedImageType('.gif')

        # photo processing
        temporary_dir = os.path.join(settings.BASE_DIR, 'media/')
        if not os.path.exists(temporary_dir):
            os.makedirs(temporary_dir)

        # uuid is common for all photos and thumbs
        uid = unicode(uuid.uuid4())

        # original photo saving
        original_photo_extension = os.path.splitext(img.name)[1].lower()
        original_photo_name = uid + cls.original_image_suffix + original_photo_extension
        original_image_path = os.path.join(temporary_dir, original_photo_name)

        with open(original_image_path, 'wb+') as original_img:
            for chunk in img.chunks():
                original_img.write(chunk)

        # avatar photo generation
        try:
            image = Image.open(original_image_path)
            if image.mode != "RGB":
                image = image.convert("RGB")

        except IOError:
            os.remove(original_image_path)
            raise AvatarExceptions.ProcessingFailed('Unknown I/O error.')

        image_width, image_height = image.size
        avatar_width, avatar_height, = cls.avatar_size, cls.avatar_size


        # checking if received image is bigger than minimum allowed size.
        if image_width < cls.min_original_image_size or image_height < cls.min_original_image_size:
            os.remove(original_image_path)
            raise AvatarExceptions.ImageIsTooSmall()


        # the image is scaled/cropped vertically or horizontally depending on the ratio
        image_ratio = avatar_width / float(avatar_height)
        ratio = 1
        if ratio > image_ratio:
            image = image.resize(
                (image.size, cls.avatar_size * image.size[1] / image.size[0]), Image.ANTIALIAS)
            box = (0, (image.size[1] - cls.avatar_size) / 2, image.size[0], (image.size[1] + cls.avatar_size) / 2)
            image = image.crop(box)

        elif ratio < image_ratio:
            image = image.resize(
                (cls.avatar_size * image.size[0] / image.size[1], cls.avatar_size), Image.ANTIALIAS)
            box = ((image.size[0] - cls.avatar_size) / 2, 0, (image.size[0] + cls.avatar_size) / 2, image.size[1])
            image = image.crop(box)
        else:
            image = image.resize((cls.avatar_size, cls.avatar_size), Image.ANTIALIAS)


        photo_name = '{uid}{photo_suffix}.jpg'.format(uid=uid, photo_suffix=cls.avatar_suffix)
        photo_path = os.path.join(temporary_dir, photo_name)

        try:
            image.save(photo_path, 'JPEG', quality=100)
        except Exception as e:
            os.remove(original_image_path)
            os.remove(photo_path)
            raise e


        avatar_bucket_path = cls.upload_photo_to_google_cloud_storage(photo_path, cls.bucket_path + photo_name)

        # seems to be ok,
        # lets remove temporary images after uploading to the google cloud storage
        os.remove(original_image_path)
        os.remove(photo_path)

        return avatar_bucket_path