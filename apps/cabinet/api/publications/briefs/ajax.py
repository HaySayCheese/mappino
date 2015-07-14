#coding=utf-8
from apps.classes import CabinetView
from collective.decorators.ajax import json_response
from core.publications.constants import OBJECTS_TYPES, HEAD_MODELS, OBJECT_STATES


class BriefsView(CabinetView):
    class GetResponses(object):
        @classmethod
        @json_response
        def ok(cls, briefs):
            return {
                "code": 0,
                'message': "OK",
                "data": briefs,
            }


    @classmethod
    def get(cls, request, section):
        briefs = cls.briefs_of_section(section, request.user.id)
        return cls.GetResponses.ok(briefs)


    @classmethod
    def briefs_of_section(cls, section, user_id):
        pubs = []
        for tid in OBJECTS_TYPES.values():
            query = HEAD_MODELS[tid].by_user_id(user_id).only('id')

            if section == 'all':
                query = query.filter(deleted=None).order_by('created')
            elif section == 'published':
                query = query.filter(state_sid = OBJECT_STATES.published(), deleted=None).order_by('created')
            elif section == 'unpublished':
                query = query.filter(state_sid = OBJECT_STATES.unpublished(), deleted=None).order_by('created')
            elif section == 'trash':
                query = query.filter(state_sid = OBJECT_STATES.deleted()).order_by('deleted')
            else:
                raise ValueError('Invalid section title {0}'.format(section))

            pubs.extend(cls.dump_publications_list(tid, query))

        return pubs


    @classmethod
    def dump_publications_list(cls, tid, queryset):
        """
        Повератає список брифів оголошень, вибраних у queryset.

        Note:
            queryset передається, а не формуєтсья в даній функції для того,
            щоб на вищих рівнях можна було накласти додакові умови на вибірку.
            По суті, дана функція лише дампить результати цієї вибірки в список в певному форматі.
        """
        publications_list = queryset.values_list('id', 'hash_id', 'state_sid', 'created', 'body__title', 'for_rent', 'for_sale')
        if not publications_list:
            return []

        model = HEAD_MODELS[tid]


        result = []
        for publication in publications_list:
            record = {
                'tid': tid,
                'id': publication[1], # hash_id
                'state_sid': publication[2], # state_sid
                'created': publication[3].strftime('%Y-%m-%dT%H:%M:%SZ'),
                'title': publication[4], # body.title
                'for_rent': publication[5], # for_rent
                'for_sale': publication[6], # for_sale

                # ...
                # other fields here
                # ...
            }

            photo = model.objects.filter(id=publication[0]).only('id')[:1][0].title_photo()
            if not photo:
                record['photo_url'] = None
            else:
                record['photo_url'] = photo.small_thumb_url

            result.append(record)

        return result