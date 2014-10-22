

class TooFrequent(Exception):
    def __init__(self, msg, remain):
        self.remain = remain
        super(TooFrequent, self).__init__(msg)


class InsufficientFunds(Exception): pass