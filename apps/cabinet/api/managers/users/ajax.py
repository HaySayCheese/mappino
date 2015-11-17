# coding=utf-8
from apps.common.api.accounts.ajax import LoginManager

from apps.views_base import ManagersView
from collective.decorators.ajax import json_response, json_response_bad_request
from collective.methods.request_data_getters import angular_post_parameters, angular_parameters, angular_put_parameters
from core.managing.moderators.models import RejectedPublications
from core.publications.constants import OBJECTS_TYPES, OBJECT_STATES, HEAD_MODELS

from core.users.models import Users
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import phonenumbers

# gets all users data
class AllUsers(ManagersView):

    @classmethod
    def publications_count(cls, user_id):
        """ get count of all publications of user and how many of them is published """
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

                'email': user.email ,
                'work_email': user.work_email,
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
        """ gets briefs of user by id  """
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


    # create publication for user by his hash id
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


class UserView(ManagersView):
    class PostResponses(object):
        @staticmethod
        @json_response
        def ok(user_id):
            return {
                'code': 0,
                'message': 'OK',
                'data': {
                    'user_hid': user_id
                }
            }

        @staticmethod
        @json_response
        def invalid_phone_number():
            return {
                'code': 1,
                'message': 'Parameter "mobile_phone" is invalid or absent.'
            }

        @staticmethod
        @json_response
        def user_already_exist():
            return {
                'code': 2,
                'message': 'User already exist.'
            }

    class GetResponses(object):
        @staticmethod
        @json_response
        def ok(user):
            phone_number = phonenumbers.parse(user.mobile_phone)
            code = phone_number.country_code
            number = phone_number.national_number
            add_number = None
            add_code = code
            if user.add_mobile_phone is not None:
                add_phone_number = phonenumbers.parse(user.add_mobile_phone)
                add_code = add_phone_number.country_code
                add_number = add_phone_number.national_number

            return {
                'code': 0,
                'message': 'OK',
                'data': {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'mobile_code': u'+{0}'.format(code),
                    'mobile_phone': u'{0}'.format(number),
                    'avatar_url': user.avatar.url(),
                    'email': user.email,
                    'work_email': user.work_email,

                    'add_mobile_phone': add_number,
                    'add_mobile_code': u'+{0}'.format(add_code),
                    'landline_phone': user.landline_phone,
                    'add_landline_phone': user.add_landline_phone,

                    'skype': user.skype,

                }
            }


    class PutResponses(object):
        @staticmethod
        @json_response
        def ok(value=None):
            return {
                'code': 0,
                'message': 'OK',
                'data': {
                    'value': value
                }
            }

        @staticmethod
        @json_response
        def value_required():
            return {
                'code': 1,
                'message': 'Value is required.'
            }

        @staticmethod
        @json_response
        def invalid_value():
            return {
                'code': 2,
                'message': 'Value is invalid.'
            }

        @staticmethod
        @json_response
        def duplicated_value():
            return {
                'code': 3,
                'message': 'Value is duplicated.'
            }

        @staticmethod
        @json_response
        def invalid_parameters():
            return {
                'code': 100,
                'message': 'Request does not contains parameters or one of them is invalid.'
            }

    def __init__(self):
        super(UserView, self).__init__()
        self.update_methods = {
            'first_name': self.__update_first_name,
            'last_name': self.__update_last_name,
            'email': self.__update_email,
            'work_email': self.__update_work_email,
            'mobile_phone': self.__update_mobile_phone_number,
            'add_mobile_phone': self.__update_add_mobile_phone_number,
            'landline_phone': self.__update_landline_phone_number,
            'add_landline_phone': self.__update_add_landline_phone_number,
            'skype': self.__update_skype,
        }


    @classmethod
    def get(self, request, *args):
        user = Users.objects.filter(hash_id=args[0])[0]
        return self.GetResponses.ok(user)



    @classmethod
    def post(cls, request):
        try:
            params = angular_post_parameters(request, ['mobile_code', 'mobile_phone'])

            number, code = str(params['mobile_phone']), str(params['mobile_code'])
            if code[0] != '+':
                code = '+' + code

            phone_number = u'{0}{1}'.format(code, number)

            phone_number = Users.objects.parse_phone_number(phone_number)

        except (ValueError, KeyError):
            return cls.PostResponses.invalid_phone_number()

        user = Users.by_one_of_the_mobile_phones(phone_number)
        if user is None:
            # create new empty user
            user = Users.objects.create_user(phone_number)
            # return hash id of new user
            return cls.PostResponses.ok(user.hash_id)
        else:
            return cls.PostResponses.user_already_exist()

    # update user fields by hash id
    def put(self, request, *args):
        user = Users.objects.filter(hash_id=args[0])[0]
        try:
            params = angular_put_parameters(request)
            field, value = params.iteritems().next()
        except (ValueError, KeyError):
            return self.PutResponses.invalid_parameters()

        try:
            update_method = self.update_methods.get(field)
            return update_method(user, value)

        except KeyError:
            return self.PutResponses.invalid_parameters()

    def __update_first_name(self, user, name):
        if not name:
            return self.PutResponses.value_required()

        if not user.first_name == name:
            user.first_name = name.capitalize()
            user.save()

        return self.PutResponses.ok(user.first_name)

    def __update_last_name(self, user, name):
        if not name:
            return self.PutResponses.value_required()

        if not user.last_name == name:
            user.last_name = name.capitalize()
            user.save()

        return self.PutResponses.ok(user.last_name)

    def __update_email(self, user, email):
        if not email:
            return self.PutResponses.value_required()

        if user.email == email:
            # no validation and DB write
            return self.PutResponses.ok()

        try:
            validate_email(email)
        except ValidationError:
            return self.PutResponses.invalid_value()

        # check for duplicates
        if not Users.email_is_free(email):
            return self.PutResponses.duplicated_value()

        # todo: add email normalization here
        user.email = email
        user.save()
        return self.PutResponses.ok()

    def __update_work_email(self, user, email):
        if not email:
            # work email may be empty
            if user.work_email:
                user.work_email = ''
                user.save()

            return self.PutResponses.ok()

        if user.work_email == email:
            # no validation and DB write
            return self.PutResponses.ok()

        try:
            validate_email(email)
        except ValidationError:
            return self.PutResponses.invalid_value()

        # check for duplicates
        if not Users.email_is_free(email):
            return self.PutResponses.duplicated_value()

        # todo: add email normalization here
        user.work_email = email
        user.save()
        return self.PutResponses.ok()


    def __update_add_mobile_phone_number(self, user, phone):
        if not phone:
            # add mobile phone may be empty
            if user.add_mobile_phone:
                user.add_mobile_phone = ''
                user.save()

            return self.PutResponses.ok()

        try:
            phone = Users.objects.parse_phone_number(phone)
        except ValueError:
            return self.PutResponses.invalid_value()

        if user.add_mobile_phone == phone:
            # already the same
            return self.PutResponses.ok()

        # check for duplicates
        if user.mobile_phone == phone or not user.mobile_phone_number_is_free(phone):
            return self.PutResponses.duplicated_value()

        if not user.add_landline_phone == phone:
            user.add_mobile_phone = phone
            user.save()

        return self.PutResponses.ok()

    def __update_landline_phone_number(self, user, phone):
        if not phone:
            # landline phone may be empty
            if user.landline_phone:
                user.landline_phone = ''
                user.save()

            return self.PutResponses.ok()

        # note: several users may have common landline phone,
        # so wee need to check for duplication only with other landline_phone
        if user.add_landline_phone == phone:
            return self.PutResponses.duplicated_value()

        if not user.landline_phone == phone:
            user.landline_phone = phone
            user.save()

        return self.PutResponses.ok()


    def __update_mobile_phone_number(self, user, phone):
        return self.PutResponses.ok()

        # note: mobile phone can not be changed by manager.


    def __update_add_landline_phone_number(self, user, phone):
        if not phone:
            # add landline phone may be empty
            if user.add_landline_phone:
                user.add_landline_phone = ''
                user.save()

            return self.PutResponses.ok()

        # note: several users may have common landline phone,
        # so wee need to check for duplication only with other landline_phone
        if user.landline_phone == phone:
            return self.PutResponses.duplicated_value()

        if not user.add_landline_phone == phone:
            user.add_landline_phone = phone
            user.save()

        return self.PutResponses.ok()

    def __update_skype(self, user, login):
        if not user.skype == login:
            user.skype = login
            user.save()

        return self.PutResponses.ok()
