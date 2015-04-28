from django.db import models
import hashlib
import uuid


class Customers(models.Model):
    phone_number = models.TextField(null=False, unique=True)
    hash_id = models.TextField()

    class Meta:
        db_table = 'customers'

    def save(self, *args, **kwargs):
        self.hash_id = self.__create_hash_id()
        super(Customers, self).save(*args, **kwargs)

    def __create_hash_id(self):
        """
        :returns:
             str object that contains sha256 generated from phone_number and uuid4
        """
        hash_object = hashlib.sha256
        hash_object.update(str(uuid.uuid4())+self.phone_number)
        return str(hash_object.digest())

