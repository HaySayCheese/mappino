#coding=utf-8
from collective.constants import AbstractConstant


class Currencies(AbstractConstant):
    def __init__(self):
        super(Currencies, self).__init__()
        self.set_ids({
            'dol': 0,
            'eur': 1,
            'uah': 2,
        })

    def dol(self):
        return self.ids['dol']


    def eur(self):
        return self.ids['eur']


    def uah(self):
        return self.ids['uah']
CURRENCIES = Currencies()