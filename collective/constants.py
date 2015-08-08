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


class Constant(object):
    @classmethod
    def values(cls):
        return cls.__dict().values()


    @classmethod
    def keys(cls):
        return cls.__dict().keys()


    @classmethod
    def iteritems(cls):
        return cls.__dict().iteritems()


    @classmethod
    def __dict(cls):
        result = {}
        for k, v in vars(cls).iteritems():


            if not isinstance(k, basestring):
                if not isinstance(v, basestring):
                    result[k] = v

                elif not v[:2] == '__':
                    result[k] = v

            else:
                if not k[:2] == '__':
                    if not isinstance(v, basestring):
                        result[k] = v

                    elif not v[:2] == '__':
                        result[k] = v

        return result