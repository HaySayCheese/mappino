# coding=utf-8
from collective.constants import AbstractConstant



class ObjectTypes(AbstractConstant):
    def __init__(self):
        super(ObjectTypes, self).__init__()
        self.set_ids({
            # Жилая недвижимость
            'flat': 0,
            'house': 1,
            'room': 2,

            # Коммерческая недвижимость
            'land': 3,
            'garage': 4,
            'office': 5,
            'trade': 6,
            'warehouse': 7,
            'business': 8,
        })
        self.commercial_estate = [
            self.ids['land'],
            self.ids['garage'],
            self.ids['office'],
            self.ids['trade'],
            self.ids['warehouse'],
            self.ids['business'],
        ]
        self.daily_rent=[
            self.ids['flat'],
            self.ids['house'],
            self.ids['room'],
        ]

    # жилая недвижимость
    def flat(self):
        return self.ids['flat']


    def house(self):
        return self.ids['house']


    def room(self):
        return self.ids['room']


    # ком. недвижимость
    def land(self):
        return self.ids['land']


    def garage(self):
        return self.ids['garage']


    def office(self):
        return self.ids['office']


    def trade(self):
        return self.ids['trade']


    def warehouse(self):
        return self.ids['warehouse']


    def business(self):
        return self.ids['business']
OBJECTS_TYPES = ObjectTypes()




class ObjectDBIndexRentTypes(AbstractConstant):
    def __init__(self):
        super(ObjectDBIndexRentTypes, self).__init__()
        self.set_ids({
                'flat': 0,
                'house': 1,
                'room': 2,
            })

    def flat(self):
        return self.ids['flat']


    def house(self):
        return self.ids['house']


    def room(self):
        return self.ids['room']
OBJECTS_DB_INDEX_RENT_TYPES = ObjectDBIndexRentTypes()


class ObjectStates(AbstractConstant):
    def __init__(self):
        super(ObjectStates, self).__init__()
        self.set_ids({
            'published': 0,
            'unpublished': 1,
            'deleted': 2,

            # todo: розібратись із цим  #'in_verification_queue': 100,  #'robot_verification': 101,
            #'robot_verification_failed': 102,
            #'moderator_verification': 111,
            #'moderator_verification_failed': 112,
            #'in_publication_queue': 200
        })


    def published(self):
        return self.ids['published']


    def unpublished(self):
        return self.ids['unpublished']


    def deleted(self):
        return self.ids['deleted']

OBJECT_STATES = ObjectStates()



class ObjectConditions(AbstractConstant):
    def __init__(self):
        super(ObjectConditions, self).__init__()
        self.set_ids({
            'cosmetic_repair': 0,  # косметичний ремонт
            'living': 1,
            'euro_repair': 2,  # євро-ремонт
            'design_repair': 3,
            'cosmetic_repair_needed': 4,
            'unfinished_repair': 5,
            'for_finishing': 6,  # під чистову обробку
        })


    def cosmetic_repair(self):
        return self.ids['cosmetic_repair']


    def euro_repair(self):
        return self.ids['euro_repair']


    def living(self):
        return self.ids['living']


    def design_repair(self):
        return self.ids['design_repair']


    def cosmetic_repair_needed(self):
        return self.ids['cosmetic_repair_needed']


    def unfinished_repair(self):
        return self.ids['unfinished_repair']


    def for_finishing(self):
        return self.ids['for_finishing']

OBJECT_CONDITIONS = ObjectConditions()



class FloorTypes(AbstractConstant):
    def __init__(self):
        super(FloorTypes, self).__init__()
        self.set_ids({
        'floor': 0,
        'mansard': 1,
        'ground': 2,  # цоколь
        })


    def floor(self):
        return self.ids['floor']


    def mansard(self):
        return self.ids['mansard']


    def ground(self):
        return self.ids['ground']

FLOOR_TYPES = FloorTypes()



class TransactionTypes(AbstractConstant):
    def __init__(self):
        super(TransactionTypes, self).__init__()
        self.set_ids({
        'all_estate': 0,  # за все
        'square_meter': 1,  # за м2
        })


    def for_all(self):
        return self.ids['all_estate']


    def for_square_meter(self):
        return self.ids['square_meter']

SALE_TRANSACTION_TYPES = TransactionTypes()



class LivingRentPeriods(AbstractConstant):
    def __init__(self):
        super(LivingRentPeriods, self).__init__()
        self.set_ids({
        'daily': 0,
        'monthly': 1,
        'long_period': 2
        })


    def daily(self):
        return self.ids['daily']


    def monthly(self):
        return self.ids['monthly']


    def long_period(self):
        return self.ids['long_period']

LIVING_RENT_PERIODS = LivingRentPeriods()



class CommercialRentPeriods(AbstractConstant):
    def __init__(self):
        super(CommercialRentPeriods, self).__init__()
        self.set_ids({
        'monthly': 0,
        'long_period': 1
        })


    def monthly(self):
        return self.ids['monthly']


    def long_period(self):
        return self.ids['long_period']

COMMERCIAL_RENT_PERIODS = CommercialRentPeriods()



class MarketType(AbstractConstant):
    def __init__(self):
        super(MarketType, self).__init__()
        self.set_ids({
        'new_building': 0,
        'secondary_market': 1,
        })


    def new_building(self):
        return self.ids['new_building']


    def secondary_market(self):
        return self.ids['secondary_market']

MARKET_TYPES = MarketType()



class HeatingTypes(AbstractConstant):
    def __init__(self):
        super(HeatingTypes, self).__init__()
        self.set_ids({
        'other': 0,
        'individual': 1,
        'central': 2,
        'unknown': 3,
        'none': 4,
        })


    def other(self):
        return self.ids['other']


    def individual(self):
        return self.ids['individual']


    def central(self):
        return self.ids['central']


    def unknown(self):
        return self.ids['unknown']


    def none(self):
        return self.ids['none']

HEATING_TYPES = HeatingTypes()



class IndividualHeatingTypes(AbstractConstant):
    def __init__(self):
        super(IndividualHeatingTypes, self).__init__()
        self.set_ids({
        'other': 0,
        'electricity': 1,
        'gas': 2,
        'firewood': 3,
        })


    def other(self):
        return self.ids['other']


    def electricity(self):
        return self.ids['electricity']


    def gas(self):
        return self.ids['gas']


    def firewood(self):
        return self.ids['firewood']

INDIVIDUAL_HEATING_TYPES = IndividualHeatingTypes()



class RedLineValues(AbstractConstant):
    def __init__(self):
        super(RedLineValues, self).__init__()
        self.set_ids({
        'yes': 0,
        'no': 1,
        'unknown': 2,
        })


    def yes(self):
        return self.ids['yes']


    def no(self):
        return self.ids['no']


    def unknown(self):
        return self.ids['unknown']

RED_LINE_VALUES = RedLineValues()


from core.publications.models import FlatsHeads, HousesHeads, RoomsHeads, \
        TradesHeads, OfficesHeads, WarehousesHeads, BusinessesHeads, GaragesHeads, LandsHeads

HEAD_MODELS = {
    OBJECTS_TYPES.flat(): FlatsHeads,
    OBJECTS_TYPES.house(): HousesHeads,
    OBJECTS_TYPES.room(): RoomsHeads,

    OBJECTS_TYPES.trade(): TradesHeads,
    OBJECTS_TYPES.office(): OfficesHeads,
    OBJECTS_TYPES.warehouse(): WarehousesHeads,
    OBJECTS_TYPES.business(): BusinessesHeads,

    OBJECTS_TYPES.garage(): GaragesHeads,
    OBJECTS_TYPES.land(): LandsHeads,
}



from core.publications.models import FlatsPhotos, HousesPhotos, RoomsPhotos, \
    TradesPhotos, OfficesPhotos, WarehousesPhotos, BusinessesPhotos, GaragesPhotos, LandsPhotos

PHOTOS_MODELS = {
    OBJECTS_TYPES.flat(): FlatsPhotos,
    OBJECTS_TYPES.house(): HousesPhotos,
    OBJECTS_TYPES.room(): RoomsPhotos,

    OBJECTS_TYPES.trade(): TradesPhotos,
    OBJECTS_TYPES.office(): OfficesPhotos,
    OBJECTS_TYPES.warehouse(): WarehousesPhotos,
    OBJECTS_TYPES.business(): BusinessesPhotos,

    OBJECTS_TYPES.garage(): GaragesPhotos,
    OBJECTS_TYPES.land(): LandsPhotos,
}

# from core.markers_handler.models import FlatsRentIndex,HousesRentIndex,RoomsRentIndex
#
# DB_INDEX_RENT_TYPES = {
#     OBJECTS_DB_INDEX_RENT_TYPES.flat(): FlatsRentIndex,
#     OBJECTS_DB_INDEX_RENT_TYPES.house(): HousesRentIndex,
#     OBJECTS_DB_INDEX_RENT_TYPES.room(): RoomsRentIndex
#
# }