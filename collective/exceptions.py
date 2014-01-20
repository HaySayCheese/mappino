class AlreadyExist(Exception):
    pass

class ObjectAlreadyExist(AlreadyExist):
    pass

class RecordAlreadyExists(AlreadyExist):
    pass

class RecordDoesNotExists(Exception):
    pass


class ParseError(Exception):
    pass



class IntervalError(Exception):
    pass