class Router(object):
	def db_for_read(self, model, **hints):
		if model._meta.app_label == 'markers_handler':
			return 'markers_index'
		return None


	def db_for_write(self, model, **hints):
		if model._meta.app_label == 'markers_handler':
			return 'markers_index'
		return None


	def allow_relation(self, obj1, obj2, **hints):
		if obj1._meta.app_label == 'markers_handler' or obj2._meta.app_label == 'markers_handler':
			return True
		return None


	def allow_migrate(self, db, model):
		if db == 'markers_index':
			return model._meta.app_label == 'markers_handler'
		elif model._meta.app_label == 'markers_handler':
			return False
		return None