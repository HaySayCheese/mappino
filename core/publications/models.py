#coding=utf-8
from core.currencies.constants import CURRENCIES
from core.publications.models_abstract import *
from core.publications.constants import *
from core.publications.exceptions import *
from core.publications.objects_constants.flats import *
from core.publications.objects_constants.garages import *
from core.publications.objects_constants.houses import *
from core.publications.objects_constants.lands import *
from core.publications.objects_constants.rooms import *
from core.publications.objects_constants.trades import *


class FlatsPhotos(PhotosModel):
    class Meta:
        db_table = 'img_flats_photos'

    # fields
    publication = models.ForeignKey('FlatsHeads', db_index=True)

    # class variables
    tid = OBJECTS_TYPES.flat()


class FlatsSaleTerms(SaleTermsModel):
    class Meta:
        db_table = 'o_flats_sale_terms'


class FlatsRentTerms(LivingRentTermsModel):
    class Meta:
        db_table = 'o_flats_rent_terms'


class FlatsBodies(BodyModel):
    class Meta:
        db_table = 'o_flats_bodies'

    substitutions = {
        'market_type': {
            MARKET_TYPES.new_building(): u'новостройка',
            MARKET_TYPES.secondary_market(): u'вторичный',
        },
        'building_type': {
            FLAT_BUILDING_TYPES.panel(): u'панель',
            FLAT_BUILDING_TYPES.brick(): u'кирпич',
            FLAT_BUILDING_TYPES.khrushchovka(): u'хрущевка',
            FLAT_BUILDING_TYPES.monolith(): u'монолит',
            FLAT_BUILDING_TYPES.pre_revolutionary(): u'дореволюционный',
            FLAT_BUILDING_TYPES.small_family(): u'малосемейка',
            FLAT_BUILDING_TYPES.individual_project(): u'индивидуальный проект',
        },
        'flat_type': {
            FLAT_TYPES.small_family(): u'малосемейка',
            FLAT_TYPES.separate(): u'отдельная',
            FLAT_TYPES.communal(): u'коммунальная',
            FLAT_TYPES.two_level(): u'двухуровневая',
            FLAT_TYPES.studio(): u'студия',
        },
        'rooms_planning': {
            FLAT_ROOMS_PLANNINGS.adjacent(): u'смежная',
            FLAT_ROOMS_PLANNINGS.separate(): u'раздельная',
            FLAT_ROOMS_PLANNINGS.separate_adjacent(): u'раздельно-смежная',
            FLAT_ROOMS_PLANNINGS.free(): u'свободная',
        },
        'condition': {
            OBJECT_CONDITIONS.cosmetic_repair(): u'косметический ремонт',
            OBJECT_CONDITIONS.living(): u'жилое',
            OBJECT_CONDITIONS.euro_repair(): u'евроремонт',
            OBJECT_CONDITIONS.design_repair(): u'дизайнерский ремонт',
            OBJECT_CONDITIONS.cosmetic_repair_needed(): u'требуется косметический ремонт',
            OBJECT_CONDITIONS.unfinished_repair(): u'неоконченный ремонт',
            OBJECT_CONDITIONS.for_finishing(): u'под чистовую отделку',
        },
        'floor_types': {
            FLOOR_TYPES.mansard(): u'мансардное помещение',
            FLOOR_TYPES.ground(): u'цокольное помещение'
        },
    }


    market_type_sid = models.SmallIntegerField(default=MARKET_TYPES.secondary_market()) # тип ринку
    building_type_sid = models.SmallIntegerField(default=FLAT_BUILDING_TYPES.panel()) # тип будинку
    custom_building_type = models.TextField(null=True)
    condition_sid = models.SmallIntegerField(default=OBJECT_CONDITIONS.living()) # загальний стан

    total_area = models.FloatField(null=True)
    living_area = models.FloatField(null=True)
    kitchen_area = models.FloatField(null=True)

    floors_count = models.SmallIntegerField(null=True)
    floor = models.SmallIntegerField(null=True) # номер поверху
    floor_type_sid = models.SmallIntegerField(default=FLOOR_TYPES.floor()) # тип поверху: мансарда, цоколь, звичайний поверх і т.д

    rooms_count = models.PositiveSmallIntegerField(null=True)
    rooms_planning_sid = models.SmallIntegerField(default=FLAT_ROOMS_PLANNINGS.separate()) # планування кімнат

    ceiling_height = models.FloatField(null=True) # висота стелі
    # Опалення
    heating_type_sid = models.SmallIntegerField(default=HEATING_TYPES.central())
    custom_heating_type = models.TextField(null=True) # якщо нічого не вказано в heating_type_sid
    # якщо вибрано ідивідуальний тип опалення в heating_type_sid
    ind_heating_type_sid = models.SmallIntegerField(default=INDIVIDUAL_HEATING_TYPES.gas())
    custom_ind_heating_type = models.TextField(null=True) # якщо нічого не вказано в ind_heating_type_sid

    # Інші зручності
    electricity = models.BooleanField(default=False)
    gas = models.BooleanField(default=False)
    hot_water = models.BooleanField(default=False)
    cold_water = models.BooleanField(default=False)

    security_alarm = models.BooleanField(default=False)
    fire_alarm = models.BooleanField(default=False)
    lift = models.BooleanField(default=False)
    add_facilities = models.TextField(null=True) # дод. відомості про зручності

    # Комунікації
    phone = models.BooleanField(default=False)
    internet = models.BooleanField(default=False)
    mobile_coverage = models.BooleanField(default=False) # покриття моб. операторами
    cable_tv = models.BooleanField(default=False) # кабельне / супутникове тб

    # Дод. будівлі
    garage = models.BooleanField(default=False) # гараж / паркомісце
    playground = models.BooleanField(default=False)
    add_buildings = models.TextField(null=True)

    #-- validation
    def check_extended_fields(self):
        if self.floor_type_sid == FLOOR_TYPES.floor() and self.floor is None:
            raise EmptyFloor('Floor is None.')
        if self.total_area is None:
            raise EmptyTotalArea('Total area is None.')
        if self.living_area is None:
            raise EmptyLivingArea('Living area is None.')
        if self.rooms_count is None:
            raise EmptyRoomsCount('Rooms count is None.')


    #-- output
    def print_market_type(self):
        return self.substitutions['market_type'][self.market_type_sid]


    def print_building_type(self):
        building_type = self.substitutions['building_type'].get(self.building_type_sid)
        if building_type:
            return building_type

        if self.building_type_sid == FLAT_BUILDING_TYPES.custom() and self.custom_building_type:
            return self.custom_building_type
        return u''


    def print_condition(self):
        return self.substitutions['condition'][self.condition_sid]


    def print_rooms_planning(self):
        return self.substitutions['rooms_planning'][self.rooms_planning_sid]


    def print_floor(self):
        # Поле "этаж" пропущено в floor_types умисно, щоб воно зайвий раз не потрапляло у видачу.
        floor_type = self.substitutions['floor_types'].get(self.floor_type_sid, u'')
        if floor_type:
            return floor_type
        return unicode(self.floor)


    def print_floors_count(self):
        if not self.floors_count:
            return u''
        return unicode(self.floors_count)


    def print_total_area(self):
        if not self.total_area:
            return u''
        return "{:.2f}".format(self.total_area).rstrip('0').rstrip('.') + u' м²'


    def print_living_area(self):
        if not self.living_area:
            return u''
        return "{:.2f}".format(self.living_area).rstrip('0').rstrip('.') + u' м²'


    def print_kitchen_area(self):
        if not self.kitchen_area:
            return u''
        return "{:.2f}".format(self.kitchen_area).rstrip('0').rstrip('.') + u' м²'


    def print_rooms_count(self):
        if self.rooms_planning_sid == FLAT_ROOMS_PLANNINGS.free() or not self.rooms_count:
            return u''
        return unicode(self.rooms_count)


    def print_facilities(self):
        facilities = u''

        # Опалення (пункт "невідомо" не виводиться)
        if self.heating_type_sid == HEATING_TYPES.none():
            facilities += u'отопление отсутствует'
        elif self.heating_type_sid == HEATING_TYPES.central():
            facilities += u'центральное отопление'
        elif self.heating_type_sid == HEATING_TYPES.individual():
            facilities += u'индивидуальное отопление'
            if self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.electricity():
                facilities += u' (электричество)'
            elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.gas():
                facilities += u' (газ)'
            elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.firewood():
                facilities += u' (дрова)'
            elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.other():
                if self.custom_ind_heating_type is not None:
                    facilities += u' ('+self.custom_ind_heating_type + u')'
        elif self.heating_type_sid == HEATING_TYPES.other():
            facilities += u'отопление — ' + self.custom_heating_type

        if self.electricity:
            facilities += u', электричество'
        if self.gas:
            facilities += u', газ'
        if self.hot_water:
            facilities += u', гарячая вода'
        if self.cold_water:
            facilities += u', холодная вода'

        if self.security_alarm and self.fire_alarm:
            facilities += u', охранная и пожарная сигнализации'
        else:
            if self.security_alarm:
                facilities += u', охранная сигнализация'
            if self.fire_alarm:
                facilities += u', пожарная сигнализация'
        if self.lift:
            facilities += u', лифт'

        if self.add_facilities:
            facilities = facilities + '. ' + self.add_facilities

        if facilities[:2] == u', ':
            facilities = facilities[2:]
        return facilities if facilities else u''


    def print_communications(self):
        communications = u''
        if self.phone:
            communications += u', телефон'
        if self.internet:
            communications += u', интернет'
        if self.mobile_coverage:
            communications += u', покрытие мобильными операторами'
        if self.cable_tv:
            communications += u', кабельное телевидение'

        if communications:
            return communications[2:] + u'.'
        return u''


    def print_provided_add_buildings(self):
        buildings = u''
        if self.garage:
            buildings += u', гараж / паркоместо'
        if self.playground:
            buildings += u', детская площадка'

        if self.add_buildings:
            buildings += u'. ' + self.add_buildings

        if buildings:
            return buildings[2:]
        return u''


class FlatsHeads(AbstractHeadModel):
    class Meta:
        db_table = 'o_flats_heads'

    tid = OBJECTS_TYPES.flat()
    photos_model = FlatsPhotos

    body = models.ForeignKey(FlatsBodies)
    sale_terms = models.OneToOneField(FlatsSaleTerms)
    rent_terms = models.OneToOneField(FlatsRentTerms)


class HousesPhotos(PhotosModel):
    class Meta:
        db_table = 'img_houses_photos'

    # fields
    publication = models.ForeignKey('HousesHeads', db_index=True)

    # class variables
    tid = OBJECTS_TYPES.house()


class HousesSaleTerms(SaleTermsModel):
    class Meta:
        db_table = 'o_houses_sale_terms'

    sale_type_sid = models.SmallIntegerField(default=HOUSE_SALE_TYPES.all_house())


class HousesRentTerms(LivingRentTermsModel):
    class Meta:
        db_table = 'o_houses_rent_terms'

    rent_type_sid = models.SmallIntegerField(default=HOUSE_RENT_TYPES.all_house())


    def print_terms(self):
        terms = super(HousesRentTerms, self).print_terms()

        if self.rent_type_sid == HOUSE_RENT_TYPES.part():
            return u'Часть дома, ' + terms
        return terms


class HousesBodies(BodyModel):
    class Meta:
        db_table = 'o_houses_bodies'

    substitutions = {
        'market_type': {
            MARKET_TYPES.new_building(): u'новостройка',
            MARKET_TYPES.secondary_market(): u'вторичный',
        },
        'condition': {
            OBJECT_CONDITIONS.cosmetic_repair(): u'косметический ремонт',
            OBJECT_CONDITIONS.living(): u'жилое',
            OBJECT_CONDITIONS.euro_repair(): u'евроремонт',
            OBJECT_CONDITIONS.design_repair(): u'дизайнерский ремонт',
            OBJECT_CONDITIONS.cosmetic_repair_needed(): u'требуется косметический ремонт',
            OBJECT_CONDITIONS.unfinished_repair(): u'неоконченный ремонт',
            OBJECT_CONDITIONS.for_finishing(): u'под чистовую отделку',
        },
    }


    market_type_sid = models.SmallIntegerField(default=MARKET_TYPES.secondary_market()) # Тип ринку
    condition_sid = models.SmallIntegerField(default=OBJECT_CONDITIONS.living()) # загальний стан

    total_area = models.FloatField(null=True)
    living_area = models.FloatField(null=True)
    kitchen_area = models.FloatField(null=True)

    mansard = models.BooleanField(default=False) # мансарда
    ground = models.BooleanField(default=False) # цокольний поверх
    lower_floor = models.BooleanField(default=False) # підвал

    floors_count = models.SmallIntegerField(null=True)
    rooms_count = models.PositiveSmallIntegerField(null=True)

    # Опалення
    heating_type_sid = models.SmallIntegerField(default=HEATING_TYPES.individual())
    custom_heating_type = models.TextField(null=True) # якщо нічого не вказано в heating_type_sid
    # якщо вибрано ідивідуальний тип опалення в heating_type_sid
    ind_heating_type_sid = models.SmallIntegerField(default=INDIVIDUAL_HEATING_TYPES.gas())
    custom_ind_heating_type = models.TextField(null=True) # якщо нічого не вказано в ind_heating_type_sid

    # Інші зручності
    electricity = models.BooleanField(default=False)
    gas = models.BooleanField(default=False)
    sewerage = models.BooleanField(default=False) # каналізація

    hot_water = models.BooleanField(default=False)
    cold_water = models.BooleanField(default=False)
    security_alarm = models.BooleanField(default=False)
    fire_alarm = models.BooleanField(default=False)
    add_facilities = models.TextField(null=True) # дод. відомості про зручності

    # Комунікації
    phone = models.BooleanField(default=False)
    internet = models.BooleanField(default=False)
    mobile_coverage = models.BooleanField(default=False) # покриття моб. операторами
    cable_tv = models.BooleanField(default=False) # кабельне / супутникове тб

    # Дод. будівлі
    garage = models.BooleanField(default=False) # гараж / паркомісце
    fence = models.BooleanField(default=False) # огорожа
    terrace = models.BooleanField(default=False)
    well = models.BooleanField(default=False) # колодязь
    alcove = models.BooleanField(default=False) # альтанка
    kaleyard = models.BooleanField(default=False) # огород
    garden = models.BooleanField(default=False) # сад
    pool = models.BooleanField(default=False)
    cellar = models.BooleanField(default=False) # погреб
    add_buildings = models.TextField(null=True)


    # validation
    def check_extended_fields(self):
        if self.total_area is None:
            raise EmptyTotalArea('Total area is None.')
        if self.living_area is None:
            raise EmptyLivingArea('Living area is None.')
        if self.floors_count is None:
            raise EmptyFloorsCount('Floors count is None.')
        if self.rooms_count is None:
            raise EmptyRoomsCount('Rooms count is None.')


    # output
    def print_market_type(self):
        return self.substitutions['market_type'][self.market_type_sid]


    def print_condition(self):
        return self.substitutions['condition'][self.condition_sid]


    def print_total_area(self):
        if not self.total_area:
            return u''
        return "{:.2f}".format(self.total_area).rstrip('0').rstrip('.') + u' м²'


    def print_living_area(self):
        if not self.living_area:
            return u''
        return "{:.2f}".format(self.living_area).rstrip('0').rstrip('.') + u' м²'


    def print_kitchen_area(self):
        if not self.kitchen_area:
            return u''
        return "{:.2f}".format(self.kitchen_area).rstrip('0').rstrip('.') + u' м²'


    def print_floors_count(self):
        if not self.floors_count:
            return u''

        floors = u''
        if self.ground:
            floors += u', цоколь'
        if self.lower_floor:
            floors += u', подвал'
        if self.mansard:
            floors += u', мансарда'

        if floors and self.floors_count:
            return unicode(self.floors_count) + u' (' + floors[2:] + u')'
        return unicode(self.floors_count)


    def print_rooms_count(self):
        if not self.rooms_count:
            return u''
        return unicode(self.rooms_count)


    def print_facilities(self):
        facilities = u''

        # Опалення (пункт "невідомо" не виводиться)
        if self.heating_type_sid == HEATING_TYPES.none():
            facilities += u'отопление отсутствует'
        elif self.heating_type_sid == HEATING_TYPES.central():
            facilities += u'центральное отопление'
        elif self.heating_type_sid == HEATING_TYPES.individual():
            facilities += u'индивидуальное отопление'
            if self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.electricity():
                facilities += u' (электричество)'
            elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.gas():
                facilities += u' (газ)'
            elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.firewood():
                facilities += u' (дрова)'
            elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.other():
                if self.custom_ind_heating_type is not None:
                    facilities += u' ('+self.custom_ind_heating_type + u')'
        elif self.heating_type_sid == HEATING_TYPES.other():
            facilities += u'отопление: ' + self.custom_heating_type

        if self.electricity:
            facilities += u', электричество'
        if self.gas:
            facilities += u', газ'
        if self.hot_water:
            facilities += u', гарячая вода'
        if self.cold_water:
            facilities += u', холодная вода'
        if self.sewerage:
            facilities += u', канализация'

        if self.security_alarm and self.fire_alarm:
            facilities += u', охранная и пожарная сигнализации'
        else:
            if self.security_alarm:
                facilities += u', охранная сигнализация'
            if self.fire_alarm:
                facilities += u', пожарная сигнализация'


        if self.add_facilities:
            facilities = facilities + '. ' + self.add_facilities

        if facilities[:2] == u', ':
            facilities = facilities[2:]
        return facilities if facilities else u''


    def print_communications(self):
        communications = u''
        if self.phone:
            communications += u', телефон'
        if self.internet:
            communications += u', интернет'
        if self.mobile_coverage:
            communications += u', покрытие мобильными операторами'
        if self.cable_tv:
            communications += u', кабельное телевидение'

        if communications:
            return communications[2:]  + u'.'
        return u''


    def print_provided_add_buildings(self):
        buildings = u''
        if self.fence:
            buildings += u', ограждение участка'
        if self.well:
            buildings += u', колодец'
        if self.garage:
            buildings += u', гараж'
        if self.pool:
            buildings += u', бассейн'
        if self.terrace:
            buildings += u', терраса'
        if self.cellar:
            buildings += u', погреб'
        if self.alcove:
            buildings += u', беседка'
        if self.kaleyard:
            buildings += u', огород'
        if self.garden:
            buildings += u', сад'

        if self.add_buildings:
            buildings += u'. ' + self.add_buildings

        if buildings:
            return buildings[2:]
        return u''


class HousesHeads(AbstractHeadModel):
    class Meta:
        db_table = 'o_houses_heads'

    tid = OBJECTS_TYPES.house()
    photos_model = HousesPhotos

    body = models.ForeignKey(HousesBodies)
    sale_terms = models.OneToOneField(HousesSaleTerms)
    rent_terms = models.OneToOneField(HousesRentTerms)


class RoomsPhotos(PhotosModel):
    class Meta:
        db_table = 'img_rooms_photos'

    # fields
    publication = models.ForeignKey('RoomsHeads', db_index=True)

    # photos
    tid = OBJECTS_TYPES.room()


class RoomsSaleTerms(SaleTermsModel):
    class Meta:
        db_table = 'o_rooms_sale_terms'


class RoomsRentTerms(LivingRentTermsModel):
    class Meta:
        db_table = 'o_rooms_rent_terms'


    def check_required_fields(self):
        """
        Перевіряє чи обов’язкові поля не None, інакше - генерує виключну ситуацію.
        Не перевіряє інформацію в полях на коректність, оскільки передбачається,
        що некоректні дані не можуть потрапити в БД через обробники зміни даних.

        Даний метод перевизначає аналогічний метод класу LivingRentTermsModel,
        оскільки той не проводить перевірку кполя "к-сть місць", а для кімнат
        дана характеристика є важливою.

        Дану перевірку неможна включити в базовий метод через те,
        що тоді вона пошириться в тому числі і на квартири, а там к-сть місць не є обов’язковою.
        """
        if self.price is None:
            raise EmptyRentPrice('Rent price is None.')
        if self.persons_count is None:
            raise EmptyPersonsCount('Persons count is None.')


class RoomsBodies(BodyModel):
    class Meta:
        db_table = 'o_rooms_bodies'

    substitutions = {
        'market_type': {
            MARKET_TYPES.new_building(): u'новостройка',
            MARKET_TYPES.secondary_market(): u'вторичный',
        },
        'building_type': {
            ROOMS_BUILDINGS_TYPES.panel(): u'панель',
            ROOMS_BUILDINGS_TYPES.brick(): u'кирпич',
            ROOMS_BUILDINGS_TYPES.khrushchovka(): u'хрущевка',
            ROOMS_BUILDINGS_TYPES.monolith(): u'монолит',
            ROOMS_BUILDINGS_TYPES.pre_revolutionary(): u'дореволюционный',
            ROOMS_BUILDINGS_TYPES.small_family(): u'малосемейка',
            ROOMS_BUILDINGS_TYPES.individual_project(): u'индивидуальный проект',
        },
        'rooms_planning': {
            FLAT_ROOMS_PLANNINGS.adjacent(): u'смежная',
            FLAT_ROOMS_PLANNINGS.separate(): u'раздельная',
            FLAT_ROOMS_PLANNINGS.separate_adjacent(): u'раздельно-смежная',
        },
        'condition': {
            OBJECT_CONDITIONS.cosmetic_repair(): u'косметический ремонт',
            OBJECT_CONDITIONS.living(): u'жилое',
            OBJECT_CONDITIONS.euro_repair(): u'евроремонт',
            OBJECT_CONDITIONS.design_repair(): u'дизайнерский ремонт',
            OBJECT_CONDITIONS.cosmetic_repair_needed(): u'требуется косметический ремонт',
            OBJECT_CONDITIONS.unfinished_repair(): u'неоконченный ремонт',
            OBJECT_CONDITIONS.for_finishing(): u'под чистовую отделку',
        },
        'floor_types': {
            FLOOR_TYPES.mansard(): u'мансарда',
            FLOOR_TYPES.ground(): u'цоколь'
        },
    }


    market_type_sid = models.SmallIntegerField(default=MARKET_TYPES.secondary_market()) # Тип ринку
    condition_sid = models.SmallIntegerField(default=OBJECT_CONDITIONS.living()) # загальний стан
    area = models.FloatField(null=True)

    floor = models.SmallIntegerField(null=True) # номер поверху
    floor_type_sid = models.SmallIntegerField(default=FLOOR_TYPES.floor()) # тип поверху: мансарда, цоколь, звичайний поверх і т.д
    floors_count = models.SmallIntegerField(null=True)


    # Інші зручності
    electricity = models.BooleanField(default=False)
    gas = models.BooleanField(default=False)
    hot_water = models.BooleanField(default=False)
    cold_water = models.BooleanField(default=False)
    lift = models.BooleanField(default=False)
    add_facilities = models.TextField(null=True) # дод. відомості про зручності

    # Комунікації
    phone = models.BooleanField(default=False)
    internet = models.BooleanField(default=False)
    mobile_coverage = models.BooleanField(default=False) # покриття моб. операторами
    cable_tv = models.BooleanField(default=False) # кабельне / супутникове тб


    # validation
    def check_extended_fields(self):
        if self.floor_type_sid == FLOOR_TYPES.floor() and self.floor is None:
            raise EmptyFloor('Floor is None.')

        if self.area is None:
            raise EmptyTotalArea('Total area is None.')


    # output
    def print_market_type(self):
        return self.substitutions['market_type'][self.market_type_sid]


    def print_floor(self):
        floor_type = self.substitutions['floor_types'].get(self.floor_type_sid, u'')
        if floor_type:
            return floor_type
        return unicode(self.floor)


    def print_floors_count(self):
        if self.floors_count is None:
            return u''
        return unicode(self.floors_count)


    def print_condition(self):
        return self.substitutions['condition'][self.condition_sid]


    def print_area(self):
        if self.area is None:
            return u''
        return "{:.2f}".format(self.area).rstrip('0').rstrip('.') + u' м²'


    def print_facilities(self):
        facilities = u''

        if self.electricity:
            facilities += u', электричество'
        if self.gas:
            facilities += u', газ'
        if self.hot_water:
            facilities += u', гарячая вода'
        if self.cold_water:
            facilities += u', холодная вода'
        if self.lift:
            facilities += u', лифт'

        if self.add_facilities:
            facilities = facilities + '. ' + self.add_facilities

        if facilities[:2] == u', ':
            facilities = facilities[2:]
        return facilities if facilities else u''


    def print_communications(self):
        communications = u''
        if self.phone:
            communications += u', телефон'
        if self.internet:
            communications += u', интернет'
        if self.mobile_coverage:
            communications += u', покрытие мобильными операторами'
        if self.cable_tv:
            communications += u', кабельное телевидение'

        if communications:
            return communications[2:]  + u'.'
        return u''


class RoomsHeads(AbstractHeadModel):
    class Meta:
        db_table = 'o_rooms_heads'

    tid = OBJECTS_TYPES.room()
    photos_model = RoomsPhotos

    body = models.ForeignKey(RoomsBodies)
    sale_terms = models.OneToOneField(RoomsSaleTerms)
    rent_terms = models.OneToOneField(RoomsRentTerms)


class TradesSaleTerms(SaleTermsModel):
    class Meta:
        db_table = 'o_trades_sale_terms'


class TradesRentTerms(CommercialRentTermsModel):
    class Meta:
        db_table = 'o_trades_rent_terms'


class TradesPhotos(PhotosModel):
    class Meta:
        db_table = 'img_trades_photos'

    # fields
    publication = models.ForeignKey('TradesHeads')

    # class variables
    tid = OBJECTS_TYPES.trade()


class TradesBodies(BodyModel):
    class Meta:
        db_table = 'o_trades_bodies'

    substitutions = {
        'market_type': {
            MARKET_TYPES.new_building(): u'новостройка',
            MARKET_TYPES.secondary_market(): u'вторичный',
        },
        'building_type': {
            TRADE_BUILDING_TYPES.residential(): u'жилое',
            TRADE_BUILDING_TYPES.entertainment(): u'ТРЦ',
            TRADE_BUILDING_TYPES.business(): u'бизнес-центр',
            TRADE_BUILDING_TYPES.administrative(): u'административное',
            TRADE_BUILDING_TYPES.separate(): u'отдельное',
        },
        'condition': {
            OBJECT_CONDITIONS.cosmetic_repair(): u'косметический ремонт',
            OBJECT_CONDITIONS.living(): u'жилое',
            OBJECT_CONDITIONS.euro_repair(): u'евроремонт',
            OBJECT_CONDITIONS.design_repair(): u'дизайнерский ремонт',
            OBJECT_CONDITIONS.cosmetic_repair_needed(): u'требуется косметический ремонт',
            OBJECT_CONDITIONS.unfinished_repair(): u'неоконченный ремонт',
            OBJECT_CONDITIONS.for_finishing(): u'под чистовую отделку',
        },
        'floor_types': {
            FLOOR_TYPES.mansard(): u'мансарда',
            FLOOR_TYPES.ground(): u'цоколь'
        },
    }


    market_type_sid = models.SmallIntegerField(default=MARKET_TYPES.secondary_market()) # Тип ринку
    building_type_sid = models.SmallIntegerField(default=TRADE_BUILDING_TYPES.entertainment())
    build_year = models.PositiveSmallIntegerField(null=True)
    condition_sid = models.SmallIntegerField(default=OBJECT_CONDITIONS.cosmetic_repair()) # загальний стан

    floor = models.SmallIntegerField(null=True) # номер поверху
    floor_type_sid = models.SmallIntegerField(default=FLOOR_TYPES.floor()) # тип поверху: мансарда, цоколь, звичайний поверх і т.д
    floors_count = models.SmallIntegerField(null=True)
    mansard = models.BooleanField(default=False) # мансарда
    ground = models.BooleanField(default=False) # цокольний поверх
    lower_floor = models.BooleanField(default=False) # підвал

    halls_count = models.PositiveSmallIntegerField(null=True)
    halls_area = models.FloatField(null=True)
    total_area = models.FloatField(null=True)
    closed_area = models.BooleanField(default=False)

    wcs_count = models.PositiveSmallIntegerField(null=True)
    ceiling_height = models.FloatField(null=True) # висота стелі


    # Опалення
    heating_type_sid = models.SmallIntegerField(default=HEATING_TYPES.central())
    custom_heating_type = models.TextField(null=True) # якщо нічого не вказано в heating_type_sid
    # якщо вибрано ідивідуальний тип опалення в heating_type_sid
    ind_heating_type_sid = models.SmallIntegerField(default=INDIVIDUAL_HEATING_TYPES.gas())
    custom_ind_heating_type = models.TextField(null=True) # якщо нічого не вказано в ind_heating_type_sid

    # Інші зручності
    electricity = models.BooleanField(default=False)
    gas = models.BooleanField(default=False)
    sewerage = models.BooleanField(default=False)

    hot_water = models.BooleanField(default=False)
    cold_water = models.BooleanField(default=False)
    ventilation = models.BooleanField(default=False)

    security_alarm = models.BooleanField(default=False)
    fire_alarm = models.BooleanField(default=False)
    security = models.BooleanField(default=False)

    add_facilities = models.TextField(null=True) # дод. відомості про зручності

    # Комунікації
    phone = models.BooleanField(default=False)
    phone_lines_count = models.PositiveSmallIntegerField(null=True)
    internet = models.BooleanField(default=False)
    mobile_coverage = models.BooleanField(default=False) # покриття моб. операторами
    cable_tv = models.BooleanField(default=False) # кабельне / супутникове тб
    lan = models.BooleanField(default=False)

    # Дод. будівлі
    parking = models.BooleanField(default=False) # гараж / паркомісце
    open_air = models.BooleanField(default=False)
    add_buildings = models.TextField(null=True)

    # Поряд знаходиться
    transport_stop = models.BooleanField(default=False)
    market = models.BooleanField(default=False)
    cafe = models.BooleanField(default=False)
    bank = models.BooleanField(default=False)
    cash_machine = models.BooleanField(default=False)
    entertainment = models.BooleanField(default=False) # розважальні установи
    add_showplaces = models.TextField(null=True)


    # validation
    def check_extended_fields(self):
        if self.floor_type_sid == FLOOR_TYPES.floor() and self.floor is None:
            raise EmptyFloor('Floor is None.')

        if self.halls_area is None:
            raise EmptyHallsArea('Halls area is None.')


    # output
    def print_market_type(self):
        return self.substitutions['market_type'][self.market_type_sid]


    def print_building_type(self):
        return self.substitutions['building_type'][self.building_type_sid]


    def print_condition(self):
        return self.substitutions['condition'][self.condition_sid]


    #-- output numeric fields
    def print_build_year(self):
        if self.build_year is None:
            return u''
        return unicode(self.build_year) + u' г.'


    def print_floor(self):
        # Поле "этаж" пропущено в floor_types умисно, щоб воно зайвий раз не потрапляло у видачу.
        floor_type = self.substitutions['floor_types'].get(self.floor_type_sid, u'')
        if floor_type:
            return floor_type
        return unicode(self.floor)


    def print_floors_count(self):
        if not self.floors_count:
            return u''

        floors = u''
        if self.ground:
            floors += u', цоколь'
        if self.lower_floor:
            floors += u', подвал'
        if self.mansard:
            floors += u', мансарда'

        if floors and self.floors_count:
            return unicode(self.floors_count) + u' (' + floors[2:] + u')'
        return unicode(self.floors_count)


    def print_halls_count(self):
        if self.halls_count is None:
            return u''
        return unicode(self.halls_count)


    def print_halls_area(self):
        if self.halls_area is None:
            return u''
        return "{:.2f}".format(self.halls_area).rstrip('0').rstrip('.') + u' м²'


    def print_total_area(self):
        if self.total_area is None:
            return u''

        total_area = "{:.2f}".format(self.total_area).rstrip('0').rstrip('.') + u' м²'
        if self.closed_area:
            total_area += u' (закрытая терр.)'
        return total_area


    def print_wcs_count(self):
        if self.wcs_count is None:
            return u''
        return unicode(self.wcs_count)


    def print_ceiling_height(self):
        if self.ceiling_height is None:
            return u''

        if self.ceiling_height == int(self.ceiling_height):
            return unicode(int(self.ceiling_height)) + u' м'
        return unicode(self.ceiling_height) + u' м'


    #-- output formatted strings
    def print_facilities(self):
        facilities = u''

        # Опалення (пункт "невідомо" не виводиться)
        if self.heating_type_sid == HEATING_TYPES.none():
            facilities += u'отопление отсутствует'
        elif self.heating_type_sid == HEATING_TYPES.central():
            facilities += u'центральное отопление'
        elif self.heating_type_sid == HEATING_TYPES.individual():
            facilities += u'индивидуальное отопление'
            if self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.electricity():
                facilities += u' (электричество)'
            elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.gas():
                facilities += u' (газ)'
            elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.firewood():
                facilities += u' (дрова)'
            elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.other():
                if self.custom_ind_heating_type is not None:
                    facilities += u' ('+self.custom_ind_heating_type + u')'
        elif self.heating_type_sid == HEATING_TYPES.other():
            facilities += u'отопление: ' + self.custom_heating_type

        if self.electricity:
            facilities += u', электричество'
        if self.gas:
            facilities += u', газ'
        if self.sewerage:
            facilities += u', канализация'
        if self.hot_water:
            facilities += u', гарячая вода'
        if self.cold_water:
            facilities += u', холодная вода'
        if self.ventilation:
            facilities += u', вентиляция'

        if self.security_alarm and self.fire_alarm:
            facilities += u', охранная и пожарная сигнализации'
        else:
            if self.security_alarm:
                facilities += u', охранная сигнализация'
            if self.fire_alarm:
                facilities += u', пожарная сигнализация'

        if self.security:
            facilities += u', охрана'

        if self.add_facilities:
            facilities = facilities + '. ' + self.add_facilities

        if facilities[:2] == u', ':
            facilities = facilities[2:]
        return facilities if facilities else u''


    def print_add_facilities(self):
        if self.add_facilities is None:
            return u''
        return self.add_facilities


    def print_communications(self):
        communications = u''
        if self.phone:
            communications += u', телефон'
            if self.phone_lines_count:
                communications += u' (количество линий - ' + unicode(self.phone_lines_count) + u')'

        if self.internet:
            communications += u', интернет'
        if self.mobile_coverage:
            communications += u', покрытие мобильными операторами'
        if self.cable_tv:
            communications += u', кабельное телевидение'
        if self.lan:
            communications += u', локальная сеть'

        if communications:
            return communications[2:] + u"."
        return u''


    def print_provided_add_buildings(self):
        buildings = u''
        if self.parking:
            buildings += u', парковка'
        if self.open_air:
            buildings += u', открытая площадка'

        if self.add_buildings:
            buildings += u'. ' + self.add_buildings

        if buildings:
            return buildings[2:]
        return buildings[2:] if buildings else u''


    def print_showplaces(self):
        showplaces = u''
        if self.transport_stop:
            showplaces += u', остановка общ. транспорта'
        if self.bank:
            showplaces += u', отделения банка'
        if self.cash_machine:
            showplaces += u', банкомат'
        if self.cafe:
            showplaces += u', кафе / ресторан'
        if self.market:
            showplaces += u', рынок / супермаркет'
        if self.entertainment:
            showplaces += u', развлекательные заведения'

        if self.add_showplaces:
            showplaces += '. ' + self.add_showplaces

        if showplaces:
            return showplaces[2:]
        return u''


class TradesHeads(CommercialHeadModel):
    class Meta:
        db_table = 'o_trades_heads'

    tid = OBJECTS_TYPES.trade()
    photos_model = TradesPhotos

    body = models.ForeignKey(TradesBodies)
    sale_terms = models.OneToOneField(TradesSaleTerms)
    rent_terms = models.OneToOneField(TradesRentTerms)


class OfficesSaleTerms(SaleTermsModel):
    class Meta:
        db_table = 'o_offices_sale_terms'


class OfficesRentTerms(CommercialRentTermsModel):
    class Meta:
        db_table = 'o_offices_rent_terms'

    furniture = models.BooleanField(default=False)
    conditioner = models.BooleanField(default=False)

    def print_facilities(self):
        facilities = u''
        if self.furniture:
            facilities += u', мебель'
        if self.conditioner:
            facilities += u', кондиционер'

        if facilities:
            return facilities[2:] + u'.'
        return u''


class OfficesPhotos(PhotosModel):
    class Meta:
        db_table = 'img_offices_photos'

    # fields
    publication = models.ForeignKey('OfficesHeads')

    # class variables
    tid = OBJECTS_TYPES.office()


class OfficesBodies(BodyModel):
    class Meta:
        db_table = 'o_offices_bodies'

    substitutions = {
        'market_type': {
            MARKET_TYPES.new_building(): u'новостройка',
            MARKET_TYPES.secondary_market(): u'вторичный',
        },
        'building_type': {
            TRADE_BUILDING_TYPES.residential(): u'жилое',
            TRADE_BUILDING_TYPES.business(): u'бизнес-центр',
            TRADE_BUILDING_TYPES.entertainment(): u'ТРЦ',
            TRADE_BUILDING_TYPES.administrative(): u'административное',
            TRADE_BUILDING_TYPES.separate(): u'отдельное',
        },
        'condition': {
            OBJECT_CONDITIONS.cosmetic_repair(): u'косметический ремонт',
            OBJECT_CONDITIONS.euro_repair(): u'евроремонт',
            OBJECT_CONDITIONS.design_repair(): u'дизайнерский ремонт',
            OBJECT_CONDITIONS.cosmetic_repair_needed(): u'требуется косметический ремонт',
            OBJECT_CONDITIONS.unfinished_repair(): u'неоконченный ремонт',
            OBJECT_CONDITIONS.for_finishing(): u'под чистовую отделку',
        },
        'floor_types': {
            FLOOR_TYPES.mansard(): u'мансарда',
            FLOOR_TYPES.ground(): u'цоколь'
        },
    }


    market_type_sid = models.SmallIntegerField(default=MARKET_TYPES.secondary_market()) # Тип ринку
    building_type_sid = models.SmallIntegerField(default=TRADE_BUILDING_TYPES.business())
    build_year = models.PositiveSmallIntegerField(null=True)
    condition_sid = models.SmallIntegerField(default=OBJECT_CONDITIONS.cosmetic_repair()) # загальний стан

    floor = models.SmallIntegerField(null=True) # номер поверху
    floor_type_sid = models.SmallIntegerField(default=FLOOR_TYPES.floor()) # тип поверху: мансарда, цоколь, звичайний поверх і т.д
    floors_count = models.SmallIntegerField(null=True)

    cabinets_count = models.PositiveSmallIntegerField(null=True)
    cabinets_area = models.FloatField(null=True)
    total_area = models.FloatField(null=True)
    closed_area = models.BooleanField(default=False)

    ceiling_height = models.FloatField(null=True) # висота стелі


    # Опалення
    heating_type_sid = models.SmallIntegerField(default=HEATING_TYPES.central())
    custom_heating_type = models.TextField(null=True) # якщо нічого не вказано в heating_type_sid
    # якщо вибрано ідивідуальний тип опалення в heating_type_sid
    ind_heating_type_sid = models.SmallIntegerField(default=INDIVIDUAL_HEATING_TYPES.gas())
    custom_ind_heating_type = models.TextField(null=True) # якщо нічого не вказано в ind_heating_type_sid

    # Інші зручності
    hot_water = models.BooleanField(default=False)
    cold_water = models.BooleanField(default=False)
    kitchen = models.BooleanField(default=False)

    security_alarm = models.BooleanField(default=False)
    fire_alarm = models.BooleanField(default=False)
    security = models.BooleanField(default=False)

    add_equipment = models.TextField(null=True) # наявність техніки та меблів
    add_facilities = models.TextField(null=True) # дод. відомості про зручності

    # Комунікації
    phone = models.BooleanField(default=False)
    phone_lines_count = models.PositiveSmallIntegerField(null=True)
    internet = models.BooleanField(default=False)
    mobile_coverage = models.BooleanField(default=False) # покриття моб. операторами
    cable_tv = models.BooleanField(default=False) # кабельне / супутникове тб
    lan = models.BooleanField(default=False)

    # Дод. будівлі
    parking = models.BooleanField(default=False) # гараж / паркомісце
    open_air = models.BooleanField(default=False)
    add_buildings = models.TextField(null=True)


    # validation
    def check_extended_fields(self):
        if self.floor_type_sid == FLOOR_TYPES.floor() and self.floor is None:
            raise EmptyFloor('Floor is None.')
        if self.cabinets_count is None:
            raise EmptyCabinetsCount('Cabinets count is None.')


    # output
    def print_market_type(self):
        return self.substitutions['market_type'][self.market_type_sid]


    def print_building_type(self):
        return self.substitutions['building_type'][self.building_type_sid]


    def print_build_year(self):
        if not self.build_year:
            return u''
        return unicode(self.build_year) + u' г.'


    def print_condition(self):
        return self.substitutions['condition'][self.condition_sid]


    def print_floor(self):
        # Поле "этаж" пропущено в floor_types умисно, щоб воно зайвий раз не потрапляло у видачу.
        floor_type = self.substitutions['floor_types'].get(self.floor_type_sid, u'')
        if floor_type:
            return floor_type
        return unicode(self.floor)


    def print_floors_count(self):
        if not self.floors_count:
            return u''
        return unicode(self.floors_count)


    def print_cabinets_count(self):
        if not self.cabinets_count:
            return u''
        return unicode(self.cabinets_count)


    def print_total_area(self):
        if not self.total_area:
            return u''

        total_area = "{:.2f}".format(self.total_area).rstrip('0').rstrip('.') + u' м²'
        if self.closed_area:
            total_area += u' (закрытая терр.)'
        return total_area


    def print_wcs_count(self):
        if not self.wcs_count:
            return u''
        return unicode(self.wcs_count)


    def print_ceiling_height(self):
        if self.ceiling_height is None:
            return u''

        if self.ceiling_height == int(self.ceiling_height):
            return unicode(int(self.ceiling_height)) + u' м'
        return unicode(self.ceiling_height) + u' м'


    #-- output formatted strings
    def print_facilities(self):
        facilities = u''

        # Опалення (пункт "невідомо" не виводиться)
        if self.heating_type_sid == HEATING_TYPES.none():
            facilities += u'отопление отсутствует'
        elif self.heating_type_sid == HEATING_TYPES.central():
            facilities += u'центральное отопление'
        elif self.heating_type_sid == HEATING_TYPES.individual():
            facilities += u'индивидуальное отопление'
            if self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.electricity():
                facilities += u' (электричество)'
            elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.gas():
                facilities += u' (газ)'
            elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.firewood():
                facilities += u' (дрова)'
            elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.other():
                if self.custom_ind_heating_type is not None:
                    facilities += u' ('+self.custom_ind_heating_type + u')'
        elif self.heating_type_sid == HEATING_TYPES.other():
            facilities += u'отопление: ' + self.custom_heating_type

        if self.kitchen:
            facilities += u', кухня'
        if self.hot_water:
            facilities += u', гарячая вода'
        if self.cold_water:
            facilities += u', холодная вода'

        if self.security_alarm and self.fire_alarm:
            facilities += u', охранная и пожарная сигнализации'
        else:
            if self.security_alarm:
                facilities += u', охранная сигнализация'
            if self.fire_alarm:
                facilities += u', пожарная сигнализация'

        if self.security:
            facilities += u', охрана'

        if self.add_facilities:
            facilities = facilities + '. ' + self.add_facilities

        if facilities[:2] == u', ':
            facilities = facilities[2:]
        return facilities if facilities else u''


    def print_communications(self):
        communications = u''
        if self.phone:
            communications += u', телефон'
            if self.phone_lines_count:
                communications += u' (количество линий - ' + unicode(self.phone_lines_count) + u')'

        if self.internet:
            communications += u', интернет'
        if self.mobile_coverage:
            communications += u', покрытие мобильными операторами'
        if self.cable_tv:
            communications += u', кабельное телевидение'
        if self.lan:
            communications += u', локальная сеть'

        if communications:
            return communications[2:] + u"."
        return u''


    def print_provided_add_buildings(self):
        buildings = u''
        if self.parking:
            buildings += u', парковка'
        if self.open_air:
            buildings += u', открытая площадка'

        if self.add_buildings:
            buildings += u'.' + self.add_buildings

        return buildings[2:] if buildings else u''


class OfficesHeads(CommercialHeadModel):
    class Meta:
        db_table = 'o_offices_heads'

    tid = OBJECTS_TYPES.office()
    photos_model = OfficesPhotos

    body = models.ForeignKey(OfficesBodies)
    sale_terms = models.OneToOneField(OfficesSaleTerms)
    rent_terms = models.OneToOneField(OfficesRentTerms)


class WarehousesSaleTerms(SaleTermsModel):
    class Meta:
        db_table = 'o_warehouses_sale_terms'


class WarehousesRentTerms(CommercialRentTermsModel):
    class Meta:
        db_table = 'o_warehouses_rent_terms'

    furniture = models.BooleanField(default=False)
    air_conditioning = models.BooleanField(default=False)


class WarehousesPhotos(PhotosModel):
    class Meta:
        db_table = 'img_warehouses_photos'

    # fields
    publication = models.ForeignKey('WarehousesHeads')

    # class variables
    tid = OBJECTS_TYPES.warehouse()


class WarehousesBodies(BodyModel):
    class Meta:
        db_table = 'o_warehouses_bodies'

    substitutions = {
        'market_type': {
            MARKET_TYPES.new_building(): u'новостройка',
            MARKET_TYPES.secondary_market(): u'вторичный',
        },
    }


    market_type_sid = models.SmallIntegerField(default=MARKET_TYPES.secondary_market()) # Тип ринку
    halls_area = models.FloatField(null=True)
    plot_area = models.FloatField(null=True) # площа участку
    open_space = models.BooleanField(default=False) # вільне плаування
    closed_area = models.BooleanField(default=False) # закрита територія

    # Опалення
    heating_type_sid = models.SmallIntegerField(default=HEATING_TYPES.central())
    custom_heating_type = models.TextField(null=True) # якщо нічого не вказано в heating_type_sid
    # якщо вибрано ідивідуальний тип опалення в heating_type_sid
    ind_heating_type_sid = models.SmallIntegerField(default=INDIVIDUAL_HEATING_TYPES.gas())
    custom_ind_heating_type = models.TextField(null=True) # якщо нічого не вказано в ind_heating_type_sid

    # Інші зручності
    electricity = models.BooleanField(default=False)
    gas = models.BooleanField(default=False)
    sewerage = models.BooleanField(default=False)

    hot_water = models.BooleanField(default=False)
    cold_water = models.BooleanField(default=False)
    ventilation = models.BooleanField(default=False)

    security_alarm = models.BooleanField(default=False)
    fire_alarm = models.BooleanField(default=False)
    security = models.BooleanField(default=False)

    add_facilities = models.TextField(null=True) # дод. відомості про зручності

    # Комунікації
    phone = models.BooleanField(default=False)
    phone_lines_count = models.PositiveSmallIntegerField(null=True)
    internet = models.BooleanField(default=False)
    mobile_coverage = models.BooleanField(default=False) # покриття моб. операторами
    lan = models.BooleanField(default=False)

    # Дод. будівлі
    parking = models.BooleanField(default=False) # гараж / паркомісце
    ramp = models.BooleanField(default=False) # авторампа
    storeroom = models.BooleanField(default=False) # підсобка
    offices = models.BooleanField(default=False)
    cathead = models.BooleanField(default=False) # кран-балка
    wc = models.BooleanField(default=False) # уборна
    add_buildings = models.TextField(null=True) # дод. відомості про зручності

    # підїздні шляхи
    railway = models.BooleanField(default=False)
    asphalt = models.BooleanField(default=False)
    concrete = models.BooleanField(default=False)
    ground = models.BooleanField(default=False)
    add_driveways = models.TextField(null=True)

    # Поряд знаходиться
    transport_stop = models.BooleanField(default=False)
    market = models.BooleanField(default=False)
    cafe = models.BooleanField(default=False)
    bank = models.BooleanField(default=False)
    cash_machine = models.BooleanField(default=False)
    refueling = models.BooleanField(default=False) # автозапрака
    railway_station = models.BooleanField(default=False)
    add_showplaces = models.TextField(null=True)


    # validation
    def check_extended_fields(self):
        if self.area is None:
            raise EmptyHallsArea('Halls area is None.')
        if self.plot_area is None:
            raise EmptyPlotArea('Halls count is None.')


    # output
    def print_title(self):
        if not self.title:
            return u''
        return self.title


    def print_description(self):
        if not self.description:
            return u''
        return self.description


    def print_market_type(self):
        return self.substitutions['market_type'][self.market_type_sid]


    def print_halls_area(self):
        if not self.area:
            return u''

        area = "{:.2f}".format(self.area).rstrip('0').rstrip('.') + u' м²'
        if self.open_space:
            area += u' (свободная планировка)'
        return area


    def print_plot_area(self):
        if not self.plot_area:
            return u''

        area = "{:.2f}".format(self.plot_area).rstrip('0').rstrip('.') + u' м²'
        if self.closed_area:
            area += u' (закрытая терр.)'
        return area


    def print_facilities(self):
        facilities = u''

        # Опалення (пункт "невідомо" не виводиться)
        if self.heating_type_sid == HEATING_TYPES.none():
            facilities += u'отопление отсутствует'
        elif self.heating_type_sid == HEATING_TYPES.central():
            facilities += u'центральное отопление'
        elif self.heating_type_sid == HEATING_TYPES.individual():
            facilities += u'индивидуальное отопление'
            if self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.electricity():
                facilities += u' (электричество)'
            elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.gas():
                facilities += u' (газ)'
            elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.firewood():
                facilities += u' (дрова)'
            elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.other():
                if self.custom_ind_heating_type is not None:
                    facilities += u' ('+self.custom_ind_heating_type + u')'
        elif self.heating_type_sid == HEATING_TYPES.other():
            facilities += u'отопление: ' + self.custom_heating_type

        if self.electricity:
            facilities += u', электричество'
        if self.gas:
            facilities += u', газ'
        if self.sewerage:
            facilities += u', канализация'
        if self.hot_water:
            facilities += u', гарячая вода'
        if self.cold_water:
            facilities += u', холодная вода'
        if self.ventilation:
            facilities += u', вентиляция'

        if self.security_alarm and self.fire_alarm:
            facilities += u', охранная и пожарная сигнализации'
        else:
            if self.security_alarm:
                facilities += u', охранная сигнализация'
            if self.fire_alarm:
                facilities += u', пожарная сигнализация'

        if self.security:
            facilities += u', охрана'

        if self.add_facilities:
            facilities += u'. ' + self.add_facilities

        if facilities[:2] == u', ':
            facilities = facilities[2:]
        return(facilities) if facilities else u''


    def print_communications(self):
        communications = u''
        if self.phone:
            communications += u', телефон'
            if self.phone_lines_count:
                communications += u' (количество линий - ' + unicode(self.phone_lines_count) + u')'

        if self.internet:
            communications += u', интернет'
        if self.mobile_coverage:
            communications += u', покрытие мобильными операторами'
        if self.lan:
            communications += u', локальная сеть'

        if communications:
            return communications[2:] + u"."
        return u''


    def print_provided_add_buildings(self):
        buildings = u''
        if self.ramp:
            buildings += u', авторампа'
        if self.parking:
            buildings += u', парковка'
        if self.cathead:
            buildings += u', кран-балка'
        if self.offices:
            buildings += u', офисные помещения'
        if self.storeroom:
            buildings += u', подсобка / кладовая'
        if self.wc:
            buildings += u', уборная'

        if self.add_buildings:
            buildings += u'. ' + self.add_buildings

        return buildings[2:] + u'.' if buildings else u''


    def print_driveways(self):
        driveways = u''
        if self.railway:
            driveways += u', Ж/Д ветка'
        if self.asphalt:
            driveways += u', асфальт'
        if self.concrete:
            driveways += u', бетон'
        if self.ground:
            driveways += u', грунт'

        if self.add_driveways:
            driveways += u'. ' + self.add_driveways

        return driveways[2:] if driveways else u''


    def print_showplaces(self):
        showplaces = u''
        if self.transport_stop:
            showplaces += u', остановка общ. транспорта'
        if self.bank:
            showplaces += u', отделения банка'
        if self.cash_machine:
            showplaces += u', банкомат'
        if self.cafe:
            showplaces += u', кафе'
        if self.market:
            showplaces += u', рынок / супермаркет'
        if self.railway:
            showplaces += u', Ж/Д станция'
        if self.refueling:
            showplaces += u', заправка'

        if self.add_showplaces:
            showplaces += u'. ' + self.add_showplaces

        if showplaces:
            return showplaces[2:]
        return u''


class WarehousesHeads(CommercialHeadModel):
    class Meta:
        db_table = 'o_warehouses_heads'

    tid = OBJECTS_TYPES.warehouse()
    photos_model = WarehousesPhotos

    body = models.ForeignKey(WarehousesBodies)
    sale_terms = models.OneToOneField(WarehousesSaleTerms)
    rent_terms = models.OneToOneField(WarehousesRentTerms)


class GaragesSaleTerms(SaleTermsModel):
    class Meta:
        db_table = 'o_garages_sale_terms'


class GaragesRentTerms(CommercialRentTermsModel):
    class Meta:
        db_table = 'o_garages_rent_terms'


class GaragesPhotos(PhotosModel):
    class Meta:
        db_table = 'img_garages_photos'

    # fields
    publication = models.ForeignKey('GaragesHeads')

    # class variables
    tid = OBJECTS_TYPES.garage()


class GaragesBodies(BodyModel):
    class Meta:
        db_table = 'o_garages_bodies'

    substitutions = {
        'market_type': {
            MARKET_TYPES.new_building(): u'новостройка',
            MARKET_TYPES.secondary_market(): u'вторичный',
        },
    }


    market_type_sid = models.SmallIntegerField(default=MARKET_TYPES.secondary_market()) # Тип ринку
    area = models.FloatField(null=True)
    ceiling_height = models.FloatField(null=True) # висота стелі
    pit = models.BooleanField(default=False) # яма

    # Інші зручності
    electricity = models.BooleanField(default=False)
    gas = models.BooleanField(default=False)

    hot_water = models.BooleanField(default=False)
    cold_water = models.BooleanField(default=False)
    ventilation = models.BooleanField(default=False)

    security_alarm = models.BooleanField(default=False)
    fire_alarm = models.BooleanField(default=False)
    security = models.BooleanField(default=False)
    add_facilities = models.TextField(null=True) # дод. відомості про зручності


    # validation
    def check_extended_fields(self):
        if self.area is None:
            raise EmptyTotalArea('Total area is None.')


    # output
    def print_title(self):
        if not self.title:
            return u''
        return self.title


    def print_description(self):
        if not self.description:
            return u''
        return self.description


    def print_market_type(self):
        return self.substitutions['market_type'][self.market_type_sid]


    def print_area(self):
        if not self.area:
            return u''
        return "{:.2f}".format(self.area).rstrip('0').rstrip('.') + u' м²'


    def print_ceiling_height(self):
        if self.ceiling_height is None:
            return u''

        if self.ceiling_height == int(self.ceiling_height):
            return unicode(int(self.ceiling_height)) + u' м'
        return unicode(self.ceiling_height) + u' м'


    def print_facilities(self):
        facilities = u''

        if self.electricity:
            facilities += u', электричество'
        if self.gas:
            facilities += u', газ'
        if self.hot_water:
            facilities += u', гарячая вода'
        if self.cold_water:
            facilities += u', холодная вода'
        if self.ventilation:
            facilities += u', вентиляция'

        if self.security_alarm and self.fire_alarm:
            facilities += u', охранная и пожарная сигнализации'
        else:
            if self.security_alarm:
                facilities += u', охранная сигнализация'
            if self.fire_alarm:
                facilities += u', пожарная сигнализация'

        if self.security:
            facilities += u', охрана'

        if self.add_facilities:
            facilities += u'.' + self.add_facilities

        if facilities[:2] == u', ':
            facilities = facilities[2:]
        return(facilities + u'.') if facilities else u''


class GaragesHeads(AbstractHeadModel):
    class Meta:
        db_table = 'o_garages_heads'

    tid = OBJECTS_TYPES.garage()
    photos_model = GaragesPhotos

    body = models.ForeignKey(GaragesBodies)
    sale_terms = models.OneToOneField(GaragesSaleTerms)
    rent_terms = models.OneToOneField(GaragesRentTerms)


class LandsSaleTerms(SaleTermsModel):
    class Meta:
        db_table = 'o_lands_sale_terms'


class LandsRentTerms(CommercialRentTermsModel):
    class Meta:
        db_table = 'o_lands_rent_terms'


class LandsPhotos(PhotosModel):
    class Meta:
        db_table = 'img_lands_photos'

    # fields
    publication = models.ForeignKey('LandsHeads')

    # class variables
    tid = OBJECTS_TYPES.land()


class LandsBodies(BodyModel):
    class Meta:
        db_table = 'o_lands_bodies'

    destination_sid = models.SmallIntegerField(null=True)
    area = models.FloatField(null=True)
    closed_area = models.BooleanField(default=False)

    # Інші зручності
    electricity = models.BooleanField(default=False)
    gas = models.BooleanField(default=False)
    water = models.BooleanField(default=False)
    sewerage = models.BooleanField(default=False)
    add_facilities = models.TextField(null=True) # дод. відомості про зручності

    # Додаткові побудови
    well = models.BooleanField(default=False)
    add_buildings = models.TextField(null=True)

    # Поряд знаходяться
    transport_stop = models.BooleanField(default=False)
    market = models.BooleanField(default=False)
    cafe = models.BooleanField(default=False)
    bank = models.BooleanField(default=False)
    cash_machine = models.BooleanField(default=False)
    entertainment = models.BooleanField(default=False) # розважальні установи
    add_showplaces = models.TextField(null=True)


    # validation
    def check_extended_fields(self):
        if self.area is None:
            raise EmptyTotalArea('Total area is None.')


    # output
    def print_title(self):
        if not self.title:
            return u''
        return self.title


    def print_description(self):
        if self.description is None:
            return u''
        return self.description


    def print_area(self):
        if self.area is None:
            return u''

        area = "{:.2f}".format(self.area).rstrip('0').rstrip('.') + u' м²'
        if self.closed_area:
            area += u' (закр. територия)'
        return area


    def print_driveways(self):
        driveways = u''
        if self.driveways_sid == LAND_DRIVEWAYS.asphalt():
            driveways = u'асфальт'+ u'.'
        elif self.driveways_sid == LAND_DRIVEWAYS.ground():
            driveways = u'грунт'+ u'.'
        return driveways


    def print_facilities(self):
        facilities = u''

        if self.electricity:
            facilities += u', электричество'
        if self.gas:
            facilities += u', газ'
        if self.water:
            facilities += u', вода'
        if self.sewerage:
            facilities += u', канализация'

        if facilities[:2] == u', ':
            facilities = facilities[2:]
        return(facilities + u'.') if facilities else u''


    def print_provided_add_buildings(self):
        buildings = u''
        if self.well:
            buildings += u'колодец / скважина'

        if self.add_buildings:
            buildings += '. ' + self.add_buildings

        return buildings + u'.' if buildings else u''


    def print_showplaces(self):
        showplaces = u''
        if self.transport_stop:
            showplaces += u', остановка общ. транспорта'
        if self.bank:
            showplaces += u', отделения банка'
        if self.cash_machine:
            showplaces += u', банкомат'
        if self.cafe:
            showplaces += u', кафе / ресторан'
        if self.market:
            showplaces += u', рынок / супермаркет'
        if self.entertainment:
            showplaces += u', развлекательные заведения'

        if self.add_showplaces:
            showplaces += u'.' + self.add_showplaces

        if showplaces:
            return showplaces[2:]
        return u''


class LandsHeads(AbstractHeadModel):
    class Meta:
        db_table = 'o_lands_heads'

    tid = OBJECTS_TYPES.land()
    photos_model = LandsPhotos

    body = models.ForeignKey(LandsBodies)
    sale_terms = models.OneToOneField(LandsSaleTerms)
    rent_terms = models.OneToOneField(LandsRentTerms)


HEAD_MODELS = {
    OBJECTS_TYPES.flat():       FlatsHeads,
    OBJECTS_TYPES.house():      HousesHeads,
    OBJECTS_TYPES.room():       RoomsHeads,

    OBJECTS_TYPES.trade():      TradesHeads,
    OBJECTS_TYPES.office():     OfficesHeads,
    OBJECTS_TYPES.warehouse():  WarehousesHeads,

    OBJECTS_TYPES.garage():     GaragesHeads,
    OBJECTS_TYPES.land():       LandsHeads,
}
PHOTOS_MODELS = {
    OBJECTS_TYPES.flat():       FlatsPhotos,
    OBJECTS_TYPES.house():      HousesPhotos,
    OBJECTS_TYPES.room():       RoomsPhotos,

    OBJECTS_TYPES.trade():      TradesPhotos,
    OBJECTS_TYPES.office():     OfficesPhotos,
    OBJECTS_TYPES.warehouse():  WarehousesPhotos,

    OBJECTS_TYPES.garage():     GaragesPhotos,
    OBJECTS_TYPES.land():       LandsPhotos,
}