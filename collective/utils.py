# coding=utf-8
import hashlib
import random
import string
import uuid


def generate_sha256_unique_id(value, salt=None):
    """
    :returns:
         str that contains sha256 hash from value salted with uuid4
    """
    if not salt:
        salt = ''.join([symbol for symbol in random.choice(string.ascii_letters + string.digits)])

    hash_object = hashlib.sha256()
    hash_object.update(str(uuid.uuid4()))
    hash_object.update(value)
    hash_object.update(salt)

    return str(hash_object.digest())