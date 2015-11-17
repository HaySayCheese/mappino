# coding=utf-8
import datetime

from apps.views_base import ManagersView
from collective.decorators.ajax import json_response
from core.publications.constants import OBJECTS_TYPES, OBJECT_STATES, HEAD_MODELS
from utils import week_days


class PublicationsCount(ManagersView):

    @classmethod
    def publications_count_for_interval(cls, datefrom, dateto):
        """ get count of all publications for time interval [datefrom, dateto] and how many of them is published """
        pubs_all = []
        pubs_published = []
        for tid in OBJECTS_TYPES.values():
            query = HEAD_MODELS[tid].objects.filter(created__gte=datefrom, created__lte=dateto).only('id')

            query_all = query.all().order_by('state_sid', 'created')

            query_published = query.filter(state_sid=OBJECT_STATES.published(), deleted=None)

            pubs_all.extend(query_all)
            pubs_published.extend(query_published)
        return {'all': len(pubs_all),
                'published': len(pubs_published)}

    class GetResponses(object):

        @staticmethod
        @json_response
        def ok():

            weeks = week_days()

            return {
                'code': 0,
                'message': 'OK',
                'data': {
                    'for_current_week': PublicationsCount.publications_count_for_interval(weeks.get(2)[0], weeks.get(2)[6]),
                    'for_last_week': PublicationsCount.publications_count_for_interval(weeks.get(1)[0], weeks.get(1)[6]),
                    'for_before_last_week': PublicationsCount.publications_count_for_interval(weeks.get(0)[0], weeks.get(0)[6]),
                    'for_month': PublicationsCount.publications_count_for_interval(datetime.datetime.now() - datetime.timedelta(days=30), datetime.datetime.now()),
                }
            }


    @classmethod
    def get(cls, request):

        return cls.GetResponses.ok()

