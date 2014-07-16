import re
from django.core.exceptions import ValidationError


def ValidateDomain(domain):
	if not re.match('\w+', domain):
		raise ValidationError('Domain does not passed regular expression check.')