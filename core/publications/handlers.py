# coding=utf-8
import os
import uuid

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
    min_original_image_size = (300, 300)

    photo_suffix = '_processed'
    photo_size = (1000, 900)

    big_thumbnail_suffix = '_big_thumb'
    big_thumbnail_size = (280, 350)

    small_thumbnail_suffix = '_small_thumb'
    small_thumbnail_size = (50, 50)

    @classmethod
    def process_and_upload_to_gcs(cls, tid, img):
        """
        Crates thumbnails, saves them to the temporary dir,
        uploads them to the google cloud storage and,
        finally, removes them all from the temp dir.

        :param tid: type id of the publication.
        :param img: image file that should be processed.

        :return:
            public links to the original image, processed photo,
            big thumbnail, and to the small thumbnail.
        """

        # check file size
        if img.size >  1024 * 1024 * 5: # 5mb
            img.close()
            raise PhotosHandlerExceptions.ImageIsTooLarge()

        # check file type
        if 'image/' not in img.content_type:
            img.close()
            raise PhotosHandlerExceptions.UnsupportedImageType('Not an image.')

        # exclude .gif'name': bucket_filename,
        # pillow sometimes generates incorrect thumbs from .gif
        if 'gif' in img.content_type:
            img.close()
            raise PhotosHandlerExceptions.UnsupportedImageType('.gif')

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

        # big thumbnail generation
        image_width, image_height = image.size # image size may change at this pos by thumb() method
        big_thumb_width, big_thumb_height  = cls.big_thumbnail_size

        if image_width > big_thumb_width or image_height > big_thumb_height:
            image.thumbnail(cls.big_thumbnail_size, Image.ANTIALIAS)

        else:
            # Всеодно виконати операцію над зображенням, інакше PIL не збереже файл.
            # Розміри зображення при цьому слід залишити без змін, щоб уникнути небажаного розширення.
            image.thumbnail(image.size, Image.ANTIALIAS)

        big_thumb_name = '{uid}{big_thumb_suffix}.jpg'.format(uid=uid, big_thumb_suffix=cls.big_thumbnail_suffix)
        big_thumb_path = os.path.join(temporary_dir, big_thumb_name)

        # The image is scaled/cropped vertically or horizontally depending on the ratio
        # This is needed to guarantee that thumb will be cropped exactly by it's size
        image_width, image_height = image.size
        image_ratio = image_width / float(image_height)
        ratio = big_thumb_width / float(big_thumb_height)
        if ratio > image_ratio:
            image = image.resize((big_thumb_width, big_thumb_width * image_height / image_width), Image.ANTIALIAS)
            box = (0, (image_height - big_thumb_height) / 2, image_width, (image_height + big_thumb_height) / 2)
            image = image.crop(box)

        elif ratio < image_ratio:
            image = image.resize((big_thumb_height * image_width / image_height, big_thumb_height), Image.ANTIALIAS)
            box = ((image_width - big_thumb_width) / 2, 0, (image_width + big_thumb_width) / 2, image_height)
            image = image.crop(box)

        else:
            image = image.resize((big_thumb_width, big_thumb_height), Image.ANTIALIAS)

        try:
            image.save(big_thumb_path, 'JPEG', quality=100)
        except Exception as e:
            os.remove(original_image_path)
            os.remove(photo_path)
            raise e

        # small thumbnail generation
        image = Image.open(original_image_path) # previous thumb may be smaller than this one
        image_width, image_height = image.size # image size may change at this pos by thumb() method
        small_thumb_width, small_thumb_height  = cls.small_thumbnail_size

        if image_width > small_thumb_width or image_height > small_thumb_height:
            image.thumbnail(cls.small_thumbnail_size, Image.ANTIALIAS)

        else:
            # Всеодно виконати операцію над зображенням, інакше PIL не збереже файл.
            # Розміри зображення при цьому слід залишити без змін, щоб уникнути небажаного розширення.
            image.thumbnail(image.size, Image.ANTIALIAS)

        small_thumb_name = '{uid}{small_thumb_suffix}.jpg'.format(uid=uid, small_thumb_suffix=cls.small_thumbnail_suffix)
        small_thumb_path = os.path.join(temporary_dir, small_thumb_name)

        # The image is scaled/cropped vertically or horizontally depending on the ratio
        # This is needed to guarantee that thumb will be cropped exactly by it's size
        image_width, image_height = image.size
        image_ratio = image_width / float(image_height)
        ratio = small_thumb_width / float(small_thumb_height)
        if ratio > image_ratio:
            image = image.resize((small_thumb_width, small_thumb_width * image_height / image_width), Image.ANTIALIAS)
            box = (0, (image_height - small_thumb_height) / 2, image_width, (image_height + small_thumb_height) / 2)
            image = image.crop(box)

        elif ratio < image_ratio:
            image = image.resize((small_thumb_height * image_width / image_height, small_thumb_height), Image.ANTIALIAS)
            box = ((image_width - small_thumb_width) / 2, 0, (image_width + small_thumb_width) / 2, image_height)
            image = image.crop(box)

        else:
            image = image.resize(cls.small_thumbnail_size, Image.ANTIALIAS)

        try:
            image.save(small_thumb_path, 'JPEG', quality=100)
        except Exception as e:
            os.remove(original_image_path)
            os.remove(photo_path)
            os.remove(big_thumb_path)
            raise e


        raise Exception('"upload_photo_to_google_cloud_storage" signature was changed')

        original_image_bucket_path = cls.upload_photo_to_google_cloud_storage(tid, original_image_path, )
        photo_bucket_path = cls.upload_photo_to_google_cloud_storage(tid, photo_path, )
        big_thumb_bucket_path = cls.upload_photo_to_google_cloud_storage(tid, big_thumb_path, )
        small_thumb_bucket_path = cls.upload_photo_to_google_cloud_storage(tid, small_thumb_path, )

        # seems to be ok,
        # lets remove temporary images after uploading to the google cloud storage
        os.remove(original_image_path)
        os.remove(photo_path)
        os.remove(big_thumb_path)
        os.remove(small_thumb_path)

        return original_image_bucket_path, \
               photo_bucket_path, \
               big_thumb_bucket_path, \
               small_thumb_bucket_path