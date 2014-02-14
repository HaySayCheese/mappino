#coding=utf-8
from core.publications.constants import OBJECTS_TYPES
from core.publications.models_signals import updated as publication_model_updated
from core.search.tasks import update_house_index
from mappino.celery import app
from mappino.wsgi import redis_connections



class SearchManager(object):
	def __init__(self):
		self.redis = redis_connections['cache']
		self.prefix = 'search_idx_task_'
		self.update_interval = 60 * 3 # secs

		publication_model_updated.connect(self.model_updated)


	def model_updated(self, **kwargs):
		try:
			tid = kwargs['tid']
			hid = kwargs['hid']
			key = self.task_digest(tid, hid)

			# Якщо в черзі вже зареєстровано запит на зміну даного оголошення - зняти задачу,
			# оскільки є вірогідність, що користувач продовжить редагувати оголошення,
			# а це, в свою чергу, спричинить небажану багаторазову перебудову індекса.
			task_id = self.redis.get(key)
			if task_id is not None:
				app.control.revoke(task_id)

			# Зареєструвати нову відкладену задачу на оновлення індекса
			if tid == OBJECTS_TYPES.house():
				task = update_house_index.apply_async([hid, ], countdown=self.update_interval)
			else:
				# todo
				raise Exception('Todo')

			pipe = self.redis.pipeline()
			pipe.set(key, task.id)
			pipe.expire(key, self.update_interval)
			pipe.execute()
		except Exception:
			# Всі виключні ситуації подавляються умисно.
			# Таким чином, навіть якщо celery чи sphinx відпадуть - це ніяк не вплине на роботу інших,
			# пов’язаних із цією підсистем і запит принаймні виконається.
			# Про виключні ситуації в даному модулі слід повідомляти в лог або адмінам на email.
			# todo: add log record here or email
			pass


	def task_digest(self, tid, hid):
		return self.prefix + unicode(tid) + ':' +  unicode(hid)
