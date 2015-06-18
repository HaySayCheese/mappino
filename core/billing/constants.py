from collective.constants import AbstractConstant



class TariffPlansIDs(AbstractConstant):
    def __init__(self):
        super(TariffPlansIDs, self).__init__()
        self.set_ids({
            'pay_as_you_go':    0,
            'realtor':          1,
            'agency':           2,
        })


    def pay_as_you_go(self):
        return self.ids['pay_as_you_go']


    def realtor(self):
        return self.ids['realtor']


    def agency(self):
        return self.ids['agency']

TARIFF_PLANS_IDS = TariffPlansIDs()



class RealtorsTransactionsTypes(AbstractConstant):
    def __init__(self):
        super(RealtorsTransactionsTypes, self).__init__()
        self.set_ids({
            # pay as you go
            'contacts_requested':   0,

            # fixed payment
            'fixed_payment':        100,

            # charged
            'charged':              200,

            # other payments
            'delta_for_days_used':  300,
        })


    def contacts_requested(self):
        return self.ids['contacts_requested']


    def fixed_payment(self):
        return self.ids['fixed_payment']


    def charged(self):
        return self.ids['charged']


    def delta_for_days_used(self):
        return self.ids['delta_for_days_used']

REALTORS_TRANSACTIONS_TYPES = RealtorsTransactionsTypes()