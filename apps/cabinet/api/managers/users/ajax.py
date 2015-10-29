# coding=utf-8

from apps.views_base import ManagersView
from collective.decorators.ajax import json_response, json_response_not_found, json_response_bad_request
from collective.methods.request_data_getters import angular_post_parameters, angular_parameters
from core.managing.moderators.models import RejectedPublications
from core.publications.constants import OBJECTS_TYPES, OBJECT_STATES, HEAD_MODELS

from core.users.models import Users


class AllUsers(ManagersView):

    @classmethod
    def publications_count(cls, user_id):
        pubs_all = []
        pubs_published = []
        for tid in OBJECTS_TYPES.values():
            query = HEAD_MODELS[tid].by_user_id(user_id).only('id')

            query_all = query.all().order_by('state_sid', 'created')

            query_published = query.filter(state_sid=OBJECT_STATES.published(), deleted=None).order_by('state_sid', 'created')

            pubs_all.extend(query_all)
            pubs_published.extend(query_published)
        return {'all': len(pubs_all),
                'published': len(pubs_published)}

    class GetResponses(object):
        @staticmethod
        @json_response

        def ok(users):

            return {
                'code': 0,
                'message': 'OK',
                'data': [{
                'hid': user.hash_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'avatar_url': user.avatar.url(),

                'mobile_phone': user.mobile_phone,
                'add_mobile_phone': user.add_mobile_phone,

                'landline_phone': user.landline_phone,
                'add_landline_phone': user.add_landline_phone,

                'skype': user.skype,

                # note: work email wil lbe shown if main email address should be hidden
                'email': user.email ,
                'pub_count': AllUsers.publications_count(user.id),

                } for user in users]
            }


    @classmethod
    def get(cls, request):

        users = Users.objects.all()

        return cls.GetResponses.ok(users)


class UsersPublications(ManagersView):

    class GetResponses(object):
        @classmethod
        @json_response
        def ok(cls, briefs):
            return {
                "code": 0,
                'message': "OK",
                "data": briefs,
            }



    class PostResponses(object):
        @staticmethod
        @json_response
        def ok(publication_hash_id):
            return {
                'code': 0,
                'message': 'OK',
                'data': {
                    'hid': publication_hash_id,
                }
            }

        @staticmethod
        @json_response_bad_request
        def invalid_parameters():
            return {
                'code': 1,
                'message': 'Request does not contains valid parameters or one of them is incorrect.',
            }

    @classmethod
    def __briefs_of_user(cls,  user_id):
        pubs = []
        for tid in OBJECTS_TYPES.values():
            query = HEAD_MODELS[tid].by_user_id(user_id).only('id')

            query = query.all().order_by('state_sid', 'created')

            pubs.extend(cls.__dump_publications_list(tid, query))

        return pubs

    @classmethod
    def __dump_publications_list(cls, tid, queryset):
        """
        Повератає список брифів оголошень, вибраних у queryset.

        Note:
            queryset передається, а не формуєтсья в даній функції для того,
            щоб на вищих рівнях можна було накласти додакові умови на вибірку.
            По суті, дана функція лише дампить результати цієї вибірки в список в певному форматі.
        """
        publications_list = queryset.values_list(
            'id', 'hash_id', 'state_sid', 'created', 'body__description', 'for_rent', 'for_sale', 'body__address')
        if not publications_list:
            return []

        model = HEAD_MODELS[tid]

        # Briefs may contain messages for the users from the moderators.
        moderators_messages = cls.__load_moderators_messages(tid, publications_list)

        result = []
        for publication in publications_list:
            record = {
                'tid': tid,
                'hid': publication[1],  # hash_id
                'state_sid': publication[2],  # state_sid
                'created': publication[3].strftime('%Y-%m-%dT%H:%M:%S%z'),
                'description': publication[4],  # body.description
                'for_rent': publication[5],  # for_rent
                'for_sale': publication[6],  # for_sale
                'address': publication[7],

                'moderator_message': moderators_messages.get(publication[1])  # hash_id

                # ...
                # other fields here
                # ...
            }

            photo = model.objects.filter(id=publication[0]).only('id')[:1][0].title_photo()
            if not photo:
                record['photo_url'] = None
            else:
                record['photo_url'] = photo.big_thumb_url

            result.append(record)

        return result

    @classmethod
    def __load_moderators_messages(cls, tid, publications_list):
        ids = [
            (tid, p[1]) for p in publications_list
            ]

        moderators_messages = RejectedPublications.objects \
            .by_publications_ids(ids) \
            .values_list('publication_hash_id', 'message')

        return {
            hash_id: message for hash_id, message in moderators_messages
            }


    @classmethod
    def get(cls, request, *args):
        user = Users.objects.filter(hash_id=args[0])[0]
        briefs = cls.__briefs_of_user(user.id)
        return cls.GetResponses.ok(briefs)


    @classmethod
    def post(cls, request, *args):
        user = Users.objects.filter(hash_id=args[0])[0]
        try:
            params = angular_parameters(request, ['tid', 'for_sale', 'for_rent'])

            tid = int(params['tid'])
            is_sale = params['for_sale']
            is_rent = params['for_rent']

            model = HEAD_MODELS[tid]
        except (ValueError, KeyError):
            return cls.PostResponses.invalid_parameters()

        record = model.new(user, is_sale, is_rent)
        return cls.PostResponses.ok(record.hash_id)
