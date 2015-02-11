class Router(object):
    markers_db = 'markers_index'


    def db_for_read(self, model, **hints):
        if model._meta.db_table.startswith('index_'):
            return self.markers_db

        return None


    def db_for_write(self, model, **hints):
        if model._meta.db_table.startswith('index_'):
            return self.markers_db

        return None


    def allow_syncdb(self, db, model):
        if db == self.markers_db:
            return model._meta.db_table.startswith('index_')

        if db == 'default':
            return not model._meta.db_table.startswith('index_')

        return False