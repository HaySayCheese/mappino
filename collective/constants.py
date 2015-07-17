class AbstractConstant(object):
    def __init__(self):
        self.ids = {}

    def set_ids(self, ids_dict):
        if len(set(ids_dict.values())) < len(ids_dict.values()):
            raise ValueError('Duplicate id detected.')
        self.ids = ids_dict
        self.count = len(self.ids.keys())

    # system functions
    def records(self):
        return self.ids

    def values(self):
        return self.ids.values()

    def keys(self):
        return self.ids.keys()