# coding=utf-8
from apps.main.api.publications_and_markers.utils import *
from core.publications.constants import OBJECTS_TYPES


class PublicationsViewMixin(object):
    """
    Implements several common methods for publications and markers processing.
    """

    # filters parsers are used to process search params from the front.
    filters_parsers = {
        OBJECTS_TYPES.flat(): parse_flats_filters,
        OBJECTS_TYPES.house(): parse_houses_filters,
        OBJECTS_TYPES.room(): parse_rooms_filters,

        OBJECTS_TYPES.land(): parse_lands_filters,
        OBJECTS_TYPES.garage(): parse_garages_filters,

        OBJECTS_TYPES.office(): parse_offices_filters,
        OBJECTS_TYPES.trade(): parse_trades_filters,
        OBJECTS_TYPES.warehouse(): parse_warehouses_filters,
    }


    @staticmethod
    def parse_viewport_coordinates(params):
        """
        Parses viewport coordinates from the "params".

        :param params: object with all the request parameters.
        :type params: dict

        :returns:
            ne_lat, ne_lng, sw_lat, sw_lng in tuple.

        :raises:
            ValueError if request contains invalid data.
        """

        try:
            viewport = params['viewport']
            ne_lat = float(viewport['ne_lat'])
            ne_lng = float(viewport['ne_lng'])
            sw_lat = float(viewport['sw_lat'])
            sw_lng = float(viewport['sw_lng'])

        except (IndexError, ValueError):
            raise ValueError('Invalid viewport coordinates was received.')

        # seems to be ok
        return ne_lat, ne_lng, sw_lat, sw_lng


    @staticmethod
    def parse_tids_panels_and_filters(params):
        """
        :type params: dict
        :param params: JSON object with request parameters.

        :returns:
            list of object types ids received from the request.

        :raises:
            ValueError even if one tid wil not pass validation.
        """

        parsed_tids_and_filters = []
        try:
            for filters in params['filters']:
                tid = int(filters['t_sid'])
                if tid not in OBJECTS_TYPES.values():
                    raise ValueError('Invalid type id received from the client, {}'.format(tid))

                panel = filters['panel']
                parsed_tids_and_filters.append(
                    (tid, panel, filters, ) # note: tuple here
                )

        except (IndexError, ValueError):
            raise ValueError('Invalid filters parameters was received.')

        # seems to be ok
        return parsed_tids_and_filters
