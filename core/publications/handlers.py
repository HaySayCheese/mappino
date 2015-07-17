# coding=utf-8
import uuid

import os
from PIL import Image
from django.conf import settings

from core.publications.exceptions import PhotosHandlerExceptions
from core.google_cloud_storage import GoogleCSPhotoUploader


class PublicationsPhotosHandler(GoogleCSPhotoUploader):
    """
    This class handles photo processing for the publications.
    Allows to create thumbnails and slides for the publications
    and upload them to the google cloud storage.
    """

    bucket = 'mappino'
    bucket_root_path = 'models/photos/'

    original_image_suffix = '_original'
    min_original_image_size = (600, 500)

    photo_suffix = '_processed'
    photo_size = (1000, 900)

    thumbnail_suffix = '_big_thumb'
    thumbnail_size = (350, 250)


    @classmethod
    def process_and_upload_to_gcs(cls, tid, image):
        """
        Crates thumbnails, saves them to the temporary dir,
        uploads them to the google cloud storage and,
        finally, removes them all from the temp dir.

        :param tid: type id of the publication.
        :param image: image file that should be processed.

        :return:
            public links to the original image, processed photo,
            big thumbnail, and to the small thumbnail.
        """

        # check file size
        if image.size >  1024 * 1024 * 5: # 5mb
            image.close()
            raise PhotosHandlerExceptions.ImageIsTooLarge()

        # check file type
        if 'image/' not in image.content_type:
            image.close()
            raise PhotosHandlerExceptions.UnsupportedImageType('Not an image.')

        # exclude .gif'name': bucket_filename,
        # pillow sometimes generates incorrect thumbs from .gif
        if 'gif' in image.content_type:
            image.close()
            raise PhotosHandlerExceptions.UnsupportedImageType('.gif')

        # photo processing
        temporary_dir = os.path.join(settings.BASE_DIR, 'media/')
        if not os.path.exists(temporary_dir):
            os.makedirs(temporary_dir)

        # uuid is common for all photos and thumbs
        uid = unicode(uuid.uuid4())

        # original photo saving
        original_photo_extension = os.path.splitext(image.name)[1].lower()
        original_photo_name = uid + cls.original_image_suffix + original_photo_extension
        original_image_path = os.path.join(temporary_dir, original_photo_name)

        with open(original_image_path, 'wb+') as original_img:
            for chunk in image.chunks():
                original_img.write(chunk)

        # big photo generation
        try:
            image = Image.open(original_image_path)
            if image.mode != "RGB":
                image = image.convert("RGB")

        except IOError:
            os.remove(original_image_path)
            raise PhotosHandlerExceptions.ProcessingFailed('Unknown I/O error.')

        image_width, image_height = image.size
        photo_width, photo_height, = cls.photo_size

        # checking if received image is bigger than minimum allowed size.
        if image_width < cls.min_original_image_size[0] or image_height < cls.min_original_image_size[1]:
            os.remove(original_image_path)
            raise PhotosHandlerExceptions.ImageIsTooSmall()

        elif image_width > photo_width or image_height > photo_height:
            image.thumbnail(cls.photo_size, Image.ANTIALIAS)

        else:
            # Всеодно виконати операцію над зображенням, інакше PIL не збереже файл.
            # Розміри зображення при цьому слід залишити без змін, щоб уникнути небажаного розширення.
            image.thumbnail(image.size, Image.ANTIALIAS)


        photo_name = '{uid}{photo_suffix}.jpg'.format(uid=uid, photo_suffix=cls.photo_suffix)
        photo_path = os.path.join(temporary_dir, photo_name)

        try:
            image.save(photo_path, 'JPEG', quality=100)
        except Exception as e:
            os.remove(original_image_path)
            os.remove(photo_path)
            raise e

        # ...
        # watermark_name = original_uid + 'wm.jpg'
        # watermark_path = os.path.join(destination_dir, watermark_name)
        # todo: генерація зображення з водяним знаком
        # ...

        # thumbnail generation
        image_width, image_height = image.size # image size may change at this pos by thumb() method
        thumb_width, thumb_height  = cls.thumbnail_size

        if image_width > thumb_width or image_height > thumb_height:
            image.thumbnail(cls.thumbnail_size, Image.ANTIALIAS)

        else:
            # Всеодно виконати операцію над зображенням, інакше PIL не збереже файл.
            # Розміри зображення при цьому слід залишити без змін, щоб уникнути небажаного розширення.
            image.thumbnail(image.size, Image.ANTIALIAS)

        thumb_name = '{uid}{thumb_suffix}.jpg'.format(uid=uid, thumb_suffix=cls.thumbnail_suffix)
        thumb_path = os.path.join(temporary_dir, thumb_name)

        # The image is scaled/cropped vertically or horizontally depending on the ratio
        # This is needed to guarantee that thumb will be cropped exactly by it's size


        image = Image.open(original_image_path)
        if image.mode != "RGB":
            image = image.convert("RGB")

        image_width, image_height = image.size # image size may change at this pos by thumb() method

        image_ratio = image_width / float(image_height)
        ratio = thumb_width / float(thumb_height)


        if ratio > image_ratio:
            size = thumb_width, thumb_height
            box = (0, (image.size[1] - size[1]) / 2, image.size[0], (image.size[1] + size[1]) / 2)
            image = image.resize((size[0], size[0] * image.size[1] / image.size[0]), Image.ANTIALIAS)

            image = image.crop(box)

        elif ratio < image_ratio:
            size = thumb_width, thumb_height

            image = image.resize((size[1] * image.size[0] / image.size[1], size[1]), Image.ANTIALIAS)
            box = ((image.size[0] - size[0]) / 2, 0, (image.size[0] + size[0]) / 2, image.size[1])
            image = image.crop(box)

        else:
            image = image.resize((thumb_width, thumb_height), Image.ANTIALIAS)


        try:
            image.save(thumb_path, 'JPEG', quality=100)
        except Exception as e:
            os.remove(original_image_path)
            os.remove(photo_path)
            raise e



        bucket_path = os.path.join(cls.bucket_root_path, str(tid))

        original_image_bucket_path = cls.upload_photo_to_google_cloud_storage(
            original_image_path, os.path.join(bucket_path, original_photo_name))

        photo_bucket_path = cls.upload_photo_to_google_cloud_storage(
            photo_path, os.path.join(bucket_path, photo_name))

        big_thumb_bucket_path = cls.upload_photo_to_google_cloud_storage(
            thumb_path, os.path.join(bucket_path, thumb_name))

        # seems to be ok,
        # lets remove temporary images after uploading to the google cloud storage
        os.remove(original_image_path)
        os.remove(photo_path)
        os.remove(thumb_path)

        return original_image_bucket_path, \
               photo_bucket_path, \
               big_thumb_bucket_path