#coding=utf-8


class AbstractConstant(object):
    def __init__(self):
        self.ids = {}
        self.count = 0


    def set_ids(self, ids_dict):
        # check for duplicates
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