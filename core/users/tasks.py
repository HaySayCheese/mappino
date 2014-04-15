from celery.exceptions import Reject
from core.users.models import Users
from mappino.celery import app


@app.task
def remove_inactive_account(uid):
	try:
		user = Users.objects.filter(id=uid).only('is_active')[:1][0]
		if not user.is_active:
			user.delete()

	except Exception as e:
		raise Reject(e, requeue=False)