import os
import hashlib

from PIL import Image
from django.conf import settings
from collective.exceptions import RuntimeException


class UserAvatar(object):
	# exceptions
	class TooLargeImage(RuntimeException):
		pass

	class TooSmallImage(RuntimeException):
		pass

	class InvalidImageFormat(RuntimeException):
		pass


	# constants
	destination = 'users/avatars/'
	dir = settings.MEDIA_ROOT + destination
	size = 200


	def __init__(self, user):
		self.user = user


	def update(self, file):
		# check if destination dir is exists
		if not os.path.exists(self.dir):
			os.makedirs(self.dir)
			if not os.path.exists(self.dir):
				raise RuntimeException("Can't create destination directories.")

		# check file type
		if 'image/' not in file.content_type:
			file.close()
			raise self.InvalidImageFormat()

		# exclude .gif (pillow sometimes generates incorrect thumbs from .gif)
		if 'gif' in file.content_type:
			file.close()
			raise self.InvalidImageFormat()

		# saving the image
		salt = '94034782133244956047'
		uid_hash = hashlib.sha384(str(self.user.id) + salt).hexdigest()


		# Temporary image path is used to save newly uploaded image on the drive,
		# and to not rewrite existing user avatar before all checks and processing will be executed.
		temp_image_name = uid_hash + '.tmp.jpg'
		temp_image_path = os.path.join(self.dir, temp_image_name)
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
			raise self.TooSmallImage()

		# the image is scaled/cropped vertically or horizontally depending on the ratio
		ratio = 1
		image_ratio = avatar.size[0] / float(avatar.size[1])
		if ratio > image_ratio:
			avatar = avatar.resize((self.size, self.size * avatar.size[1] / avatar.size[0]), Image.ANTIALIAS)
			box = (0, (avatar.size[1] - self.size) / 2, avatar.size[0], (avatar.size[1] + self.size) / 2)
			avatar = avatar.crop(box)

		elif ratio < image_ratio:
			avatar = avatar.resize((self.size * avatar.size[0] / avatar.size[1], self.size), Image.ANTIALIAS)
			box = ((avatar.size[0] - self.size) / 2, 0, (avatar.size[0] + self.size) / 2, avatar.size[1])
			avatar = avatar.crop(box)

		else:
			avatar = avatar.resize((self.size, self.size), Image.ANTIALIAS)

		# saving
		image_name = uid_hash + '.jpg'
		image_path = os.path.join(self.dir, image_name)

		avatar.save(image_path, 'JPEG', quality=100)
		os.rename(temp_image_path, image_path)
		self.user.avatar_url = ''.join([settings.MEDIA_URL, self.destination, image_name])
		self.user.save()


	def url(self):
		return self.user.avatar_url