#coding=utf-8
from celery.exceptions import Reject
from core.users.models import Users
from mappino.celery import app


@app.task
def remove_inactive_account(uid):
	"""
	Запускається одразу після створення облікового запису користувача для того,
	щоб автоматично видалити його через деякий час, якщо він так і не був активований.
	"""
	try:
		user = Users.objects.filter(id=uid).only('is_active')[:1][0]
		if not user.is_active:
			user.delete()

	except Exception as e:
		# За будь-якої помилки скасувати задачу
		raise Reject(e, requeue=False)