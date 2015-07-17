#coding=utf-8
import os
import uuid

from PIL import Image
from django.conf import settings

from core.google_cloud_storage import GoogleCSPhotoUploader
from core.users.exceptions import AvatarExceptions


class Avatar(GoogleCSPhotoUploader):
    avatar_size = 180
    min_original_image_size = avatar_size

    bucket_path = 'users/photos/'


    def __init__(self, user):
        self.user = user


    def update(self, image):
        self.remove()

        url =  self.process_and_upload_to_gcs(image)
        self.user.avatar_url = url
        self.user.save()
        return url


    def url(self):
        return self.user.avatar_url


    def remove(self):
        url = self.user.avatar_url
        if not url:
            return


        # clear url anyway
        self.user.avatar_url = ''
        self.user.save()

        filename = url.split('/')[-1]
        path = self.bucket_path + filename

        try:
            self.remove_photo_from_google_cloud_storage(path)
        except:
            pass


    @classmethod
    def process_and_upload_to_gcs(cls, img):
        """
        Processes avatar and uploads it to the GCS.

        :return:
            public links to the avatar.
        """

        # check file size
        if img.size > 5 * 1024 * 1024: # 1024 * 1024 * 5: # 5mb
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
        original_photo_filename = uid + original_photo_extension
        original_image_path = os.path.join(temporary_dir, original_photo_filename)

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
        image_ratio = image.size[0] / float(image.size[1])
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





    #     if ratio > img_ratio:
    #     img = img.resize((size[0], int(round(size[0] * img.size[1] / img.size[0]))),
    #         Image.ANTIALIAS)
    #     # Crop in the top, middle or bottom
    #     if crop_type == 'top':
    #         box = (0, 0, img.size[0], size[1])
    #     elif crop_type == 'middle':
    #         box = (0, int(round((img.size[1] - size[1]) / 2)), img.size[0],
    #             int(round((img.size[1] + size[1]) / 2)))
    #     elif crop_type == 'bottom':
    #         box = (0, img.size[1] - size[1], img.size[0], img.size[1])
    #     else :
    #         raise ValueError('ERROR: invalid value for crop_type')
    #     img = img.crop(box)
    # elif ratio < img_ratio:
    #     img = img.resize((int(round(size[1] * img.size[0] / img.size[1])), size[1]),
    #         Image.ANTIALIAS)
    #     # Crop in the top, middle or bottom
    #     if crop_type == 'top':
    #         box = (0, 0, size[0], img.size[1])
    #     elif crop_type == 'middle':
    #         box = (int(round((img.size[0] - size[0]) / 2)), 0,
    #             int(round((img.size[0] + size[0]) / 2)), img.size[1])
    #     elif crop_type == 'bottom':
    #         box = (img.size[0] - size[0], 0, img.size[0], img.size[1])
    #     else :
    #         raise ValueError('ERROR: invalid value for crop_type')
    #     img = img.crop(box)
    # else :
    #     img = img.resize((size[0], size[1]),
    #         Image.ANTIALIAS)





        try:
            image.save(original_image_path, 'JPEG', quality=100)
        except Exception as e:
            os.remove(original_image_path)
            os.remove(original_image_path)
            raise e


        avatar_bucket_path = cls.upload_photo_to_google_cloud_storage(original_image_path, cls.bucket_path + original_photo_filename)

        # seems to be ok,
        # lets remove temporary images after uploading to the google cloud storage
        os.remove(original_image_path)

        return avatar_bucket_path