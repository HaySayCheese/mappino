# coding=utf-8
from django.core import serializers

from core.publications.constants import OBJECTS_TYPES


class PublishedDataSource(object):
    def __init__(self):
        self.data_generators = {
            # living
            OBJECTS_TYPES.flat():       self.compose_flat_description,
            OBJECTS_TYPES.house():      self.compose_house_description,
            OBJECTS_TYPES.room():       self.compose_room_description,

            # commercial
            OBJECTS_TYPES.trade():      self.compose_trade_description,
            OBJECTS_TYPES.office():     self.compose_office_description,
            OBJECTS_TYPES.warehouse():  self.compose_warehouse_description,

            # other
            OBJECTS_TYPES.garage():     self.compose_garage_description,
            OBJECTS_TYPES.land():       self.compose_land_description,
        }


    def format(self, tid, publication_head):
        """
        :type tid: int
        :param tid: type id of the publication.

        :type publication_head: AbstractHeadModel
        :param publication_head: head-record of the publication.

        :rtype: dict
        :return:
            dict with two main sections:
                head - all system information about publication, such as photos and tags.
                data - formatted text information about publication.

        :raise: RuntimeException - broken list of data generators.
        """
        data = {
            'photos': [photo.photo_url for photo in publication_head.photos().only('photo_url')]
        }

        description_generator = self.data_generators[tid]
        # noinspection PyCallingNonCallable
        data.update(description_generator(publication_head))

        # clearing the results from all empty and None entries, that potentially can occurs
        data = {k: v for k, v in data.iteritems() if v}

        return data


    @staticmethod
    def compose_flat_description(p):
        description = {
            'title': p.body.print_title(),
            'description': p.body.print_description(),

            'market_type': p.body.print_market_type(),
            'building_type': p.body.print_building_type(),
            'condition': p.body.print_condition(),

            'total_area': p.body.print_total_area(),
            'living_area': p.body.print_living_area(),
            'kitchen_area': p.body.print_kitchen_area(),

            'floor': p.body.print_floor(),
            'floors_count': p.body.print_floors_count(),

            'rooms_count': p.body.print_rooms_count(),
            'rooms_planning': p.body.print_rooms_planning() ,
            'facilities': p.body.print_facilities(),

            'communications': p.body.print_communications(),
            'buildings': p.body.print_provided_add_buildings(),
        }

        description.update({
            'sale_price': p.sale_terms.print_price(),
        })
        description.update({
            'rent_price': p.rent_terms.print_price(),
            'rent_terms': p.rent_terms.print_terms(),
            'rent_facilities': p.rent_terms.print_facilities()
        })
        return description


    @staticmethod
    def compose_house_description(p):
        description = {
            'title': p.body.print_title(),
            'description': p.body.print_description(),

            'market_type': p.body.print_market_type(),
            'condition': p.body.print_condition(),

            'total_area': p.body.print_total_area(),
            'living_area': p.body.print_living_area(),
            'kitchen_area': p.body.print_kitchen_area(),

            'floors_count': p.body.print_floors_count(),
            'rooms_count': p.body.print_rooms_count(),

            'facilities': p.body.print_facilities(),
            'communications': p.body.print_communications(),
            'buildings': p.body.print_provided_add_buildings(),
        }

        description.update({
            'sale_price': p.sale_terms.print_price(),
        })
        description.update({
            'rent_price': p.rent_terms.print_price(),
            'rent_terms': p.rent_terms.print_terms(),
            'rent_facilities': p.rent_terms.print_facilities()
        })
        return description


    @staticmethod
    def compose_room_description(p):
        description = {
            'title': p.body.print_title(),
            'description': p.body.print_description(),

            'market_type': p.body.print_market_type(),
            'condition': p.body.print_condition(),
            'area': p.body.print_area(),

            'floor': p.body.print_floor(),
            'floors_count': p.body.print_floors_count(),

            'facilities': p.body.print_facilities(),
            'communications': p.body.print_communications(),
        }

        description.update({
            'sale_price': p.sale_terms.print_price(),
        })
        description.update({
            'rent_price': p.rent_terms.print_price(),
            'rent_terms': p.rent_terms.print_terms(),
            'rent_facilities': p.rent_terms.print_facilities()
        })
        return description


    @staticmethod
    def compose_trade_description(p):
        description = {
            'title': p.body.print_title(),
            'description': p.body.print_description(),

            'market_type': p.body.print_market_type(),
            'building_type': p.body.print_building_type(),
            'build_year': p.body.print_build_year(),
            'condition': p.body.print_condition(),

            'floor': p.body.print_floor(),
            'floors_count': p.body.print_floors_count(),

            'halls_count': p.body.print_halls_count(),
            'halls_area': p.body.print_halls_area(),
            'total_area': p.body.print_total_area(),

            'vcs_count': p.body.print_vcs_count(),
            'ceiling_height': p.body.print_ceiling_height(),

            'facilities': p.body.print_facilities(),
            'communications': p.body.print_communications(),
            'buildings': p.body.print_provided_add_buildings(),
            'showplaces': p.body.print_showplaces()
        }

        description.update({
            'sale_price': p.sale_terms.print_price(),
        })
        description.update({
            'rent_price': p.rent_terms.print_price(),
            'rent_terms': p.rent_terms.print_terms(),
        })
        return description


    @staticmethod
    def compose_office_description(p):
        description = {
            'title': p.body.print_title(),
            'description': p.body.print_description(),

            'market_type': p.body.print_market_type(),
            'building_type': p.body.print_building_type(),
            'build_year': p.body.print_build_year(),
            'condition': p.body.print_condition(),

            'floor': p.body.print_floor(),
            'floors_count': p.body.print_floors_count(),
            'cabinets_count': p.body.print_cabinets_count(),
            'total_area': p.body.print_total_area(),
            'vcs_count': p.body.print_vcs_count(),
            'ceiling_height': p.body.print_ceiling_height(),

            'facilities': p.body.print_facilities(),
            'communications': p.body.print_communications(),
            'buildings': p.body.print_provided_add_buildings(),
            'showplaces': p.body.print_showplaces()
        }

        description.update({
            'sale_price': p.sale_terms.print_price(),
        })
        description.update({
            'rent_price': p.rent_terms.print_price(),
            'rent_terms': p.rent_terms.print_terms(),
            'rent_facilities': p.rent_terms.print_facilities()
        })
        return description


    @staticmethod
    def compose_warehouse_description(p):
        description = {
            'title': p.body.print_title(),
            'description': p.body.print_description(),

            'market_type': p.body.print_market_type(),
            'halls_area': p.body.print_halls_area(),
            'plot_area': p.body.print_plot_area(),
            'driveways': p.body.print_driveways(),

            'facilities': p.body.print_facilities(),
            'communications': p.body.print_communications(),
            'buildings': p.body.print_provided_add_buildings(),
            'showplaces': p.body.print_showplaces()
        }

        description.update({
            'sale_price': p.sale_terms.print_price(),
        })
        description.update({
            'rent_price': p.rent_terms.print_price(),
            'rent_terms': p.rent_terms.print_terms(),
        })
        return description


    @staticmethod
    def compose_garage_description(p):
        description = {
            'title': p.body.print_title(),
            'description': p.body.print_description(),
            'market_type': p.body.print_market_type(),
            'area': p.body.print_area(),
            'ceiling_height': p.body.print_ceiling_height(),
            'pit': u'есть' if p.body.pit else u'',
            'facilities': p.body.print_facilities(),
        }

        description.update({
            'sale_price': p.sale_terms.print_price(),
        })
        description.update({
            'rent_price': p.rent_terms.print_price(),
            'rent_terms': p.rent_terms.print_terms(),
        })
        return description


    @staticmethod
    def compose_land_description(p):
        description = {
            'title': p.body.print_title(),
            'description': p.body.print_description(),
            'area': p.body.print_area() or u'неизвестно',
            'facilities': p.body.print_facilities(),
            'buildings': p.body.print_provided_add_buildings(),
            'showplaces': p.body.print_showplaces()
        }

        description.update({
            'sale_price': p.sale_terms.print_price(),
        })
        description.update({
            'rent_price': p.rent_terms.print_price(),
            'rent_terms': p.rent_terms.print_terms(),
        })
        return description


class UnpublishedFormatter(object):
    @classmethod
    def format(cls, tid, record):
        head = serializers.serialize(
            'python', [record], fields=('created', 'actual', 'for_rent', 'for_sale', 'state_sid',
                                        'degree_lat', 'degree_lng', 'segment_lat', 'segment_lng',
                                        'pos_lat', 'pos_lng','address'))[0]['fields']

        # Переформатувати дату створення оголошення у прийнятний для десериалізації формат
        created = head['created']
        if created is not None:
            head['created'] = created.isoformat()

        # Переформатувати дату завершального терміну актуальності оголошення
        # у прийнятний для десериалізації формат
        actual = head['actual']
        if actual is not None:
            head['actual'] = actual.isoformat()


        body = serializers.serialize('python', [record.body])[0]['fields']

        # Якщо оголошення призначено для продажу - підгрузити і сериалізувати цю інформацію.
        # Дана інформація не грузиться автоматично щоб уникнути потенційно-зайвих селектів.
        if record.for_sale:
            sale_terms = serializers.serialize('python', [record.sale_terms])[0]['fields']
        else:
            sale_terms = None

        # Якщо оголошення призначено для оренди - підгрузити і сериалізувати цю інформацію.
        # Дана інформація не грузиться автоматично щоб уникнути потенційно-зайвих селектів.
        if record.for_rent:
            rent_terms = serializers.serialize('python', [record.rent_terms])[0]['fields']
        else:
            rent_terms = None

        data = {
            'head': head,
            'body': body,
            'sale_terms': sale_terms,
            'rent_terms': rent_terms,
            'photos': [{
                'thumbnail_url': photo.big_thumb_url,
                'photo_url': photo.photo_url,
                'is_title': photo.check_is_title(),
                'hash_id': photo.hash_id,
            } for photo in record.photos()]
        }
        return cls.format_output_data(data)


    @classmethod
    def format_output_data(cls, data):
        # maps coordinates
        head = data.get('head')
        if head is None:
            raise ValueError('@head can not be None.')

        degree_lat = head.get('degree_lat')
        degree_lng = head.get('degree_lng')
        if (degree_lat is None) or (degree_lng is None):
            coordinates = {
                'lat': None,
                'lng': None,
            }
        else:
            segment_lat = head.get('segment_lat')
            segment_lng = head.get('segment_lng')
            if (segment_lat is None) or (segment_lng is None):
                coordinates = {
                    'lat': None,
                    'lng': None,
                }
            else:
                pos_lat = head.get('pos_lat')
                pos_lng = head.get('pos_lng')
                if (pos_lat is None) or (pos_lng is None):
                    coordinates = {
                        'lat': None,
                        'lng': None,
                    }
                else:
                    coordinates = {
                        'lat': str(degree_lat) + '.' + str(segment_lat) + str(pos_lat),
                        'lng': str(degree_lng) + '.' + str(segment_lng) + str(pos_lng),
                    }

        del data['head']['degree_lat']
        del data['head']['degree_lng']
        del data['head']['segment_lat']
        del data['head']['segment_lng']
        del data['head']['pos_lat']
        del data['head']['pos_lng']
        data['head'].update(coordinates)


        # sale terms
        s_terms = data.get('sale_terms')
        if s_terms:
            s_price = s_terms.get('price')
            if s_price:
                if int(s_price) == s_price:
                    # Якщо після коми лише нулі - повернути ціле значення
                    data['sale_terms']['price'] = "%.0f" % s_price
                else:
                    # Інакше - округлити до 2х знаків після коми
                    data['sale_terms']['price'] = "%.2f" % s_price


        # rent terms
        r_terms = data.get('rent_terms')
        if r_terms:
            r_price = r_terms.get('price')
            if r_price:
                if int(r_price) == r_price:
                    # Якщо після коми лише нулі - повернути ціле значення
                    data['rent_terms']['price'] = "%.0f" % r_price
                else:
                    # Інакше - округлити до 2х знаків після коми
                    data['rent_terms']['price'] = "%.2f" % r_price

        # Костиль..
        # Об’єкти готового бізнесу мають 2 decimal-поля, які ломають json-encoder.
        # Логічно винести функцію формування json-опису об’єкту в модель,
        # але зараз зроблено як зроблено і часу змінювати це немає.
        # Отже, тут ці 2 поля переформатовуються.

        monthly_costs = data['body'].get('monthly_costs')
        if monthly_costs:
            if int(monthly_costs) == monthly_costs:
                # Якщо після коми лише нулі - повернути ціле значення
                data['body']['monthly_costs'] = "%.0f" % monthly_costs
            else:
                # Інакше - округлити до 2х знаків після коми
                data['body']['monthly_costs'] = "%.2f" % float(monthly_costs)


        annual_receipts = data['body'].get('annual_receipts')
        if annual_receipts:
            if int(annual_receipts) == annual_receipts:
                # Якщо після коми лише нулі - повернути ціле значення
                data['body']['annual_receipts'] = "%.0f" % annual_receipts
            else:
                # Інакше - округлити до 2х знаків після коми
                data['body']['annual_receipts'] = "%.2f" % float(annual_receipts)


        return data
