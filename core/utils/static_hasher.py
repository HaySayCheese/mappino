import gzip
import os
import uuid
import hashlib

from shutil import copyfile, rmtree
from django.conf import settings



DEST_DIRNAME = 'hash'

hashed_links = {}
groups_files = {}



def init():
	rmtree(os.path.join(settings.STATIC_ROOT, DEST_DIRNAME))
	os.mkdir(os.path.join(settings.STATIC_ROOT, DEST_DIRNAME))



def hash_static(href, group=None, extension=None):
	link = hashed_links.get(href)
	if link is not None:
		return link


	hash_filename = ''
	destination_dir = os.path.join(settings.STATIC_ROOT, DEST_DIRNAME)
	destination_url = os.path.join(settings.STATIC_URL,  DEST_DIRNAME)

	if group is None:
		while True:
			content = open(os.path.join(settings.STATIC_ROOT, href), 'rb').read()
			hash = hashlib.md5(content).hexdigest()[:15]

			original_extension = os.path.splitext(href)[1]
			hash_filename = hash + original_extension
			if not os.path.exists(os.path.join(destination_dir, hash_filename)):
				break

		destination_file = os.path.join(destination_dir, hash_filename)
		if os.path.exists(destination_file):
			link = os.path.join(destination_url, hash_filename)
			return link

		source_file = os.path.join(settings.STATIC_ROOT, href)
		copyfile(source_file, destination_file)

		# gzip
		f_in = open(destination_file, 'rb')
		f_out = gzip.open(destination_file + '.gz', 'wb', 7)
		f_out.writelines(f_in)
		f_out.close()
		f_in.close()

		link = os.path.join(destination_url, hash_filename)
		hashed_links[href] = link
		return link


	else:
		hash_filename = groups_files.get(group)
		if hash_filename is None:
			hash_filename = hashlib.md5(uuid.uuid4().hex).hexdigest()[:15] + '.' + extension
			groups_files[group] = hash_filename
			file = open(os.path.join(destination_dir, hash_filename), "w")
			file.seek(0)

		else:
			file = open(os.path.join(destination_dir, hash_filename), "a")
			file.write('\n')

		source_file = open(os.path.join(settings.STATIC_ROOT, href), "r")
		for line in source_file:
			file.write(line)

		file.close()
		source_file.close()

		link = os.path.join(destination_url, hash_filename)
		return link