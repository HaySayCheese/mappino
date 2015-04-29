# coding=utf-8
import os

from httplib2 import Http
from oauth2client.client import SignedJwtAssertionCredentials
from googleapiclient.discovery import build
from django.conf import settings

from mappino.passwords import GOOGLE_CS_SERVICE_ACCOUNT, GOOGLE_A_SERVICE_ACCOUNT


__storage_credentials = None
__storage_key_path = os.path.join(settings.BASE_DIR, 'mappino/keys/gcs_private_key.p12')
__storage_scope = 'https://www.googleapis.com/auth/devstorage.read_write'

__analytics_credentials = None
__analytics_key_path = os.path.join(settings.BASE_DIR, 'mappino/keys/ga_private_key.p12')
__analytics_scope = 'https://www.google.com/analytics/feeds/'


def init_google_cloud_storage():
    """
    :returns: google cloud storage API client.
    """
    global __storage_credentials

    if __storage_credentials is None or __storage_credentials.invalid:
        with open(__storage_key_path, 'rb') as key_file:
            key = key_file.read()

        __storage_credentials = SignedJwtAssertionCredentials(GOOGLE_CS_SERVICE_ACCOUNT, key, scope=__storage_scope)


    http = __storage_credentials.authorize(Http())
    return build(serviceName='storage', version='v1', http=http)


def init_google_analytics():
    """
    :returns: google analytics API client.
    """
    global __analytics_credentials

    if __analytics_credentials is None or __analytics_credentials.invalid:
        with open(__analytics_key_path, 'rb') as key_file:
            key = key_file.read()

        __analytics_credentials = SignedJwtAssertionCredentials(GOOGLE_A_SERVICE_ACCOUNT, key, scope=__analytics_scope)


    http = __analytics_credentials.authorize(Http())
    return build(serviceName='analytics', version='v3', http=http)