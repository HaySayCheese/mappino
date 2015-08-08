# coding=utf-8
from apps.views_base import ModeratorsView
from collective.decorators.ajax import json_response
from core.moderators.models import PublicationsCheckQueue
from core.publications import formatters
from core.publications.constants import HEAD_MODELS


class NextPublicationView(ModeratorsView):
    formatter = formatters.PublishedDataSource() # this is a description generator for the publications.


    class GetResponses(object):
        @staticmethod
        @json_response
        def ok(data):
            return {
                'code': 0,
                'message': 'OK',
                'data': data,
            }


    @classmethod
    def get(cls, request):
        while True:
            record = PublicationsCheckQueue.get_next_record()
            if record is None:
                return cls.GetResponses.ok({}) # there are no publications to check


            try:
                model = HEAD_MODELS[record.publication_tid]
                publication = model.objects\
                    .filter(id=record.publication_head_id)\
                    .only('for_sale', 'for_rent')\
                    .prefetch_related('body')\
                    .prefetch_related('sale_terms')\
                    .prefetch_related('rent_terms')\
                    [:1][0]
            except IndexError:
                record.delete()
                continue


            if not publication.is_published():
                record.delete()
                continue


            data = cls.formatter.format(record.publication_tid, publication)
            return cls.GetResponses.ok(data)


        # todo: перевірити чи в привильному порядку віддаються оголошення