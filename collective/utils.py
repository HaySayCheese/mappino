# coding=utf-8
import hashlib
import random
import string
import uuid


def generate_sha256_unique_id(value, salt=None):
    """
    :type value str
    :param value: value that should be uses as a base for hashing.

    :type salt str
    :param salt: salt that should be added to the digest.
                 if salt is None - than it wil lbe generated automatically in random way.

    :returns:
         str that contains sha256 hash from value salted with uuid4
    """
    if not salt:
        salt = ''.join([random.choice(string.ascii_letters + string.digits) for x in range(32)])

    hash_object = hashlib.sha256()
    hash_object.update(uuid.uuid4().hex)
    hash_object.update(value)
    hash_object.update(salt)

    return hash_object.hexdigest()