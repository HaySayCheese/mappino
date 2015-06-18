from django.db import models
from apps.main.api.subdomains.validators import ValidateDomain


class Subdomains(models.Model):
	domain = models.CharField(unique=True, validators=ValidateDomain)