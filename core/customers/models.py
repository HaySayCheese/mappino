import hashlib
import uuid

from django.db import models
from collective.utils import generate_sha256_unique_id


class Customers(models.Model):
    phone_number = models.TextField(null=False, unique=True)
    hash_id = models.TextField()

    class Meta:
        db_table = 'customers'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.hash_id = generate_sha256_unique_id(self.phone_number)
        super(Customers, self).save(force_insert, force_update, using, update_fields)

