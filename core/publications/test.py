# coding=utf-8
try:
    import datetime
    from datetime import timedelta as td
    import uuid

    from core.markers_handler.models import SegmentsIndex
    from django.test import TestCase
    from core.publications.constants import MARKET_TYPES, OBJECT_CONDITIONS, FLOOR_TYPES, HEATING_TYPES, \
        INDIVIDUAL_HEATING_TYPES, LIVING_RENT_PERIODS, OBJECTS_TYPES, OBJECT_STATES

    from core.publications.objects_constants.flats import FLAT_BUILDING_TYPES, FLAT_TYPES, FLAT_ROOMS_PLANNINGS
    from models import FlatsHeads, FlatsBodies, FlatsRentTerms, FlatsPhotos

    from core.users.models import Users
except Exception as e:
    pass

class TestCalendarRentFlat(TestCase):

    def setUp(self):
        #First we create user
        self.user = Users.objects.create(
            id = 1,
            hash_id = lambda: uuid.uuid4().hex,
            is_active = True,

            is_moderator = True,
            is_manager = True,


            # required
            first_name = "Test Name", # unique=True
            last_name = "Test last Name", # unique=True
            email = "testemail@gmail.com", # unique=True
            mobile_phone = "+380990164345", # unique=True

            # other contacts
            add_mobile_phone = None, # null=True, unique=True
            work_email = None, # null=True
            skype = "Test_skype", # null=True
            landline_phone = None, # null=True
            add_landline_phone = None, # therefore it can not be unique.

            # other fields
            avatar_url = None,
            )

        publication_body_object = FlatsBodies.objects.create(
            id = 1,
            title = "This is my test title",
            description  = "This is my test description",
            market_type_sid = MARKET_TYPES.secondary_market(), # -> 1
            building_type_sid = FLAT_BUILDING_TYPES.brick(), # -> 2
            custom_building_type = None,
            build_year = 1975,
            flat_type_sid = FLAT_TYPES.separate(), # ->2,
            rooms_planning_sid = FLAT_ROOMS_PLANNINGS.separate(), # -> 1
            condition_sid = OBJECT_CONDITIONS.living(), # ->1

            floor = 2, #
            floor_type_sid = FLOOR_TYPES.floor(), # -> 0
            floors_count = 5,
            ceiling_height = 2.5,

            total_area = 250, # null = True
            living_area = 200, # null = True
            kitchen_area = 30, # null=True

            rooms_count = 3, # null=True
            bedrooms_count = 1, # null=True
            vcs_count = 1, # null=True
            balconies_count = 1, # null=True
            loggias_count = 1, # null=True


            # Опалення
            heating_type_sid = HEATING_TYPES.central(), # -> 2
            custom_heating_type = None, # якщо нічого не вказано в heating_type_sid
            # якщо вибрано ідивідуальний тип опалення в heating_type_sid
            ind_heating_type_sid = INDIVIDUAL_HEATING_TYPES.gas(), # ->2
            custom_ind_heating_type = None, # якщо нічого не вказано в ind_heating_type_sid

            # Інші зручності
            electricity = True,
            gas = True,
            hot_water = True,
            cold_water = True,

            security_alarm = True,
            fire_alarm = True,
            lift = True,
            add_facilities = None, # null=True # дод. відомості про зручності

            # Комунікації
            phone = True,
            internet = True,
            mobile_coverage = True, # покриття моб. операторами
            cable_tv = True,  # кабельне / супутникове тб

            # Дод. будівлі
            garage = True, # гараж / паркомісце
            playground = True,
            add_buildings = None, #null=True

            # Поряд знаходиться
            kindergarten = True,
            school = True,
            market = True,
            transport_stop = True,
            entertainment = True, # розважальні установи
            sport_center = True,
            park = True,
            add_showplaces = None, #null=True
        )

        # Prepare data for fields with date
        date_from = datetime.datetime.now().date()
        date_to  = datetime.datetime.now().date() + datetime.timedelta(days = 5)
        delta = date_to - date_from
        rent_dates = [date_from + td(days=i) for i in range(1,delta.days)]

        rent_term_object = FlatsRentTerms.objects.create(
            id = 1,
            price = 150, # null = True,
            is_conract = False,
            period_sid = LIVING_RENT_PERIODS.monthly(), # -> 1
            # days_reserved = ArrayField(models.DateField)
            persons_count = 2, # null=True

            family = True,
            foreigners = True,
            smoking = False,
            pets = True,
            add_terms = "Hey ho test add terms",

            furniture = True,
            refrigerator = True,
            tv = True,
            washing_machine = True,
            conditioner = True,
            home_theater = True,

            entrance_dates = [date_from], # null = True
            departure_dates = [date_to], # null=True
            rent_dates = rent_dates, # null=True

        )
        self.head = FlatsHeads.objects.create(
            id = 1,
            tid = OBJECTS_TYPES.flat(), # ->1
            hash_id = lambda: uuid.uuid4().hex,
            owner = self.user.id,
            photos_model = FlatsPhotos,
            body = publication_body_object.id,
            sale_terms = None,
            rent_terms = rent_term_object.id,
            state_sid = OBJECT_STATES.published(), # -> 0
            for_sale = False,
            for_rent = True,
            created = date_from - delta,
            modified = date_from - delta,
            published = date_from - delta,
            deleted = None, # null=True
            actual = None, # null=True

            #-- map coordinates
            degree_lat = "50", # null=True
            degree_lng = "30", # null=True

            segment_lat = "44", # null=True
            segment_lng = "52", # null=True

            pos_lat = '2132617533195', # null=True
            pos_lng = '8831625282764', # null=True
            address = "вулиця Ковальчука, 177, Чернівці, Чернівецька область, Украина" # null=True
        )

        print self

    def CheckAdd(self):
        self.assertEqual(self.head.id, 1)
