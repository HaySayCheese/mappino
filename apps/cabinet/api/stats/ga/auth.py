from django.conf import settings
import httplib2
from googleapiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials
import os


CLIENT_KEY = os.path.join(settings.BASE_DIR, 'mappino/keys/ga_private_key.p12')
TOKEN_FILE_NAME = os.path.join(settings.BASE_DIR, 'mappino/keys/runtime/analytics.dat')


key_file = file(CLIENT_KEY, 'rb')
key = key_file.read()
key_file.close()

credentials = None


def initialize_service():
	global credentials


	if credentials is None or credentials.invalid:
		credentials = SignedJwtAssertionCredentials(
			'605654330831-thm3t5hqs10rtbkvga8u0drlm6i7g9im@developer.gserviceaccount.com',
			key, scope='https://www.google.com/analytics/feeds/')

	http = httplib2.Http()
	http = credentials.authorize(http)
	return build(serviceName='analytics', version='v3', http=http)
