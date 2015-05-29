# coding=utf-8
import io

from googleapiclient.http import MediaIoBaseUpload
from core.google_api_auth import init_google_cloud_storage


class GoogleCSPhotoUploader(object):
    bucket = 'mappino'


    @classmethod
    def upload_photo_to_google_cloud_storage(cls, path, cache_control_seconds=8035200):
        """
        Uploads file from "file_path" to the google cloud storage.

        :type path: str, unicode
        :param path: path to the file that should be uploaded.

        :type cache_control_seconds: int
        :param cache_control_seconds: max time image cache time.
        """
        image = open(path)
        media = MediaIoBaseUpload(io.BytesIO(image.read()), 'image/jpg')
        metadata = {
            'name': cls.bucket + path,
            'cacheControl': cache_control_seconds,
            'predefinedAcl': 'publicRead',
        }

        storage = init_google_cloud_storage()
        resp = storage.objects().insert(
            bucket = cls.bucket,
            name = cls.bucket + path,
            body = metadata,
            media_body = media
        ).execute()

        if 'selfLink' in resp:
            return '{domain}/{bucket}/{path}'.format(
                domain = 'https://storage.googleapis.com',
                bucket = cls.bucket,
                path = cls.bucket + path,
            )

        else:
            raise RuntimeError('File was not uploaded properly.')


    @classmethod
    def remove_photo_from_google_cloud_storage(cls, bucket_file_path):
        """
        :type bucket_file_path str, unicode
        :param bucket_file_path:
        """
        try:
            root_index = bucket_file_path.index(cls.bucket)
        except ValueError:
            raise ValueError('It seems that storage does not contains such bucket or filepath.')

        storage = init_google_cloud_storage()
        storage.objects().delete(
            bucket_name=cls.bucket,
            object=bucket_file_path[root_index:]
        )