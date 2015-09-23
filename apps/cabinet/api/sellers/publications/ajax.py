# coding=utf-8
import datetime
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, ValidationError, SuspiciousOperation
from django.http.response import HttpResponseBadRequest
from pytz import timezone

from apps.views_base import CabinetView
from collective.decorators.ajax import json_response, json_response_bad_request, json_response_not_found
from collective.methods.request_data_getters import angular_parameters
from core.managing.moderators.models import RejectedPublications
from core.publications import formatters
from core.publications.exceptions import PhotosHandlerExceptions, NotEnoughPhotos
from core.publications.constants import OBJECTS_TYPES, HEAD_MODELS, PHOTOS_MODELS, OBJECT_STATES, \
    DAILY_RENT_RESERVATIONS_MODELS
from core.publications.models_abstract import LivingDailyRentModel
from core.publications.signals import record_updated
from core.publications.update_methods.flats import update_flat
from core.publications.update_methods.houses import update_house
from core.publications.update_methods.offices import update_office
from core.publications.update_methods.rooms import update_room
from core.publications.update_methods.trades import update_trade
from core.publications.update_methods.warehouses import update_warehouse
from core.publications.update_methods.garages import update_garage
from core.publications.update_methods.lands import update_land


class Publications(CabinetView):
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
    def post(cls, request):
        try:
            params = angular_parameters(request, ['tid', 'for_sale', 'for_rent'])

            tid = int(params['tid'])
            is_sale = params['for_sale']
            is_rent = params['for_rent']

            model = HEAD_MODELS[tid]
        except (ValueError, KeyError):
            return cls.PostResponses.invalid_parameters()


        record = model.new(request.user, is_sale, is_rent)
        return cls.PostResponses.ok(record.hash_id)


class Publication(CabinetView):
    published_formatter = formatters.PublishedDataSource()
    unpublished_formatter = formatters.UnpublishedFormatter()


    class GetResponses(object):
        @staticmethod
        @json_response
        def ok(publication_data):
            return {
                'code': 0,
                'message': 'OK',
                'data': publication_data,
            }


        @staticmethod
        @json_response_bad_request
        def invalid_parameters():
            return {
                'code': 1,
                'message': 'Request does not contains valid parameters or one of them is incorrect.'
            }


    class PutResponses(object):
        @staticmethod
        @json_response
        def ok(new_value=None):
            if new_value:
                return {
                    'code': 0,
                    'message': 'OK',
                    'data': {
                        'value': new_value,
                    }
                }

            else:
                return {
                    'code': 0,
                    'message': 'OK',
                }


        @staticmethod
        @json_response_bad_request
        def invalid_parameters():
            return {
                'code': 1,
                'message': 'Request does not contains valid parameters or one of them is incorrect.'
            }


    class DeleteResponses(object):
        @staticmethod
        @json_response
        def ok():
            return {
                'code': 0,
                'message': 'OK',
            }


        @staticmethod
        @json_response_bad_request
        def invalid_parameters():
            return {
                'code': 1,
                'message': 'Request does not contains valid parameters or one of them is incorrect.'
            }


    @classmethod
    def get(cls, request, *args):
        try:
            tid, hash_id = args[0], args[1]
            tid = int(tid)
            model = HEAD_MODELS[tid]

        except (IndexError, ValueError, KeyError):
            return cls.GetResponses.invalid_parameters()


        try:
            head = model.by_hash_id(hash_id, select_body=True)
        except ObjectDoesNotExist:
            return cls.GetResponses.invalid_parameters()


        # check owner
        if head.owner.id != request.user.id:
            raise PermissionDenied()


        # seems to be ok
        if head.is_published() or head.is_deleted():
            response = cls.published_formatter.format(tid, head)
        else:
            response = cls.unpublished_formatter.format(tid, head)

        return cls.GetResponses.ok(response)


    @classmethod
    def put(cls, request, *args):
        try:
            tid, hash_id = args[:2]
            tid = int(tid)
            model = HEAD_MODELS[tid]

            parameters = angular_parameters(request, ['fieldName'])
            field = parameters['fieldName']
            value = parameters['fieldValue'] # may be ''

        except (IndexError, ValueError, KeyError):
            return cls.PutResponses.invalid_parameters()


        try:
            head = model.objects.filter(hash_id=hash_id).only('id', 'owner')[0]
        except IndexError:
             return cls.PutResponses.invalid_parameters()


        # check owner
        if head.owner.id != request.user.id:
            raise PermissionDenied()


        returned_value = None

        # todo: move this into models as a method
        if tid == OBJECTS_TYPES.flat():
            returned_value = update_flat(head, field, value, tid)

        elif tid == OBJECTS_TYPES.house():
            returned_value = update_house(head, field, value, tid)

        elif tid == OBJECTS_TYPES.room():
            returned_value = update_room(head, field, value, tid)


        elif tid == OBJECTS_TYPES.land():
            returned_value = update_land(head, field, value, tid)

        elif tid == OBJECTS_TYPES.garage():
            returned_value = update_garage(head, field, value, tid)

        elif tid == OBJECTS_TYPES.office():
            returned_value = update_office(head, field, value, tid)

        elif tid == OBJECTS_TYPES.trade():
            returned_value = update_trade(head, field, value, tid)

        elif tid == OBJECTS_TYPES.warehouse():
            returned_value = update_warehouse(head, field, value, tid)


        # Відправити сигнал про зміну моделі.
        # Кастомний сигнал відправляєтсья, оскільки стандартний post-save
        # не містить необхідної інформації (tid).
        # todo: move this into the model
        record_updated.send(
            sender=None,
            tid=tid,
            hid=head.id,
            hash_id=head.hash_id,
            for_sale=head.for_sale,
            for_rent=head.for_rent,
        )

        return cls.PutResponses.ok(returned_value)


    @classmethod
    def delete(cls, request, *args):
        try:
            tid, hash_id = args[:2]
            tid = int(tid)
            # hash_id doesnt need to be converted to int

            model = HEAD_MODELS[tid]
        except (IndexError, ValueError):
            return cls.DeleteResponses.invalid_parameters()


        try:
            head = model.objects.filter(hash_id=hash_id).only('id', 'owner')[0]
        except IndexError:
            return cls.DeleteResponses.invalid_parameters()


        # check owner
        if head.owner.id != request.user.id:
            raise PermissionDenied()


        if not head.is_deleted():
            # note: no real deletion here.
            # all publications that was deleted are situated in trash
            head.mark_as_deleted()
        else:
            head.delete_permanent()


        return cls.DeleteResponses.ok()


    class PublishUnpublish(CabinetView):
        class PutResponses(object):
            @staticmethod
            @json_response
            def ok(publication_head):
                return {
                    'code': 0,
                    'message': 'OK',
                    'data': {
                        'state_sid': publication_head.state_sid,
                    }
                }


            @staticmethod
            @json_response
            def invalid_parameters():
                return {
                    'code': 1,
                    'message': 'Request contains invalid parameters or does not contains it at all.'
                }


            @staticmethod
            @json_response
            def invalid_publication():
                return {
                    'code': 2,
                    'message': 'Publication does not pass validation.'
                }


            @staticmethod
            @json_response
            def not_enough_photos():
                return {
                    'code': 3,
                    'message': 'Publication does not contains enough photos.'
                }


        @classmethod
        def put(cls, request, *args, **kwargs):
            try:
                tid, hash_id = args[:2]
                tid = int(tid)
                # hash_id doesnt need to be converted to int

                model = HEAD_MODELS[tid]
            except (IndexError, ValueError):
                return cls.PutResponses.invalid_publication()


            try:
                head = model.queryset_by_hash_id(hash_id).only('id', 'owner')[0]
            except IndexError:
                return cls.PutResponses.invalid_publication()


            # check owner
            if head.owner.id != request.user.id:
                raise PermissionDenied()


            operation = kwargs['operation']
            if operation == 'unpublish':
                head.unpublish()
                return cls.PutResponses.ok(head)

            elif operation == 'publish':
                try:
                    head.publish()

                    # publication may be added to publication queue instead of publishing,
                    # so the front should know about it.
                    return cls.PutResponses.ok(head)

                except NotEnoughPhotos:
                    return cls.PutResponses.not_enough_photos()

                except ValidationError:
                    return cls.PutResponses.invalid_publication()


    class UploadPhoto(CabinetView):
        class PostResponses(object):
            @staticmethod
            @json_response
            def ok(photo):
                return {
                    'code': 0,
                    'message': 'OK',
                    'data': {
                        'hash_id': photo.hash_id,
                        'is_title': photo.check_is_title(),
                        'thumbnail_url': photo.big_thumb_url,
                    }
                }


            @staticmethod
            @json_response_bad_request
            def invalid_tid():
                return {
                    'code': 1,
                    'message': 'request does not contains param "tid", or it is invalid.'
                }


            @staticmethod
            @json_response_bad_request
            def invalid_hash_id():
                return {
                    'code': 2,
                    'message': 'request does not contains param "hash_id" or it is invalid.'
                }


            @staticmethod
            @json_response_bad_request
            def image_is_absent():
                return {
                    'code': 3,
                    'message': 'request does not contains image file "file". '
                }


            @staticmethod
            @json_response_bad_request
            def image_is_too_large():
                return {
                    'code': 4,
                    'message': 'request contains image that is greater than max. allowable.'
                }


            @staticmethod
            @json_response_bad_request
            def image_is_too_small():
                return {
                    'code': 5,
                    'message': 'request contains image that is smaller than min. allowable.'
                }


            @staticmethod
            @json_response_bad_request
            def unsupported_image_type():
                return {
                    'code': 6,
                    'message': 'request contains image of unsupported type.'
                }

            # ...
            # other response handlers goes here
            # ...


            @staticmethod
            @json_response_bad_request
            def unknown_error():
                return {
                    'code': 100,
                    'message': 'unknown error occurred.'
                }


        @classmethod
        def post(cls, request, *args):
            try:
                hash_id = args[1]
            except IndexError:
                return cls.PostResponses.invalid_hash_id()

            try:
                tid = int(args[0])
                model = HEAD_MODELS[tid]
                photos_model = PHOTOS_MODELS[tid]
            except (IndexError, ValueError):
                return cls.PostResponses.invalid_tid()


            try:
                image = request.FILES['file']
            except IndexError:
                return cls.PostResponses.image_is_absent()


            try:
                publication = model.objects.filter(hash_id=hash_id).only('id', 'owner')[:1][0]
            except IndexError:
                return cls.PostResponses.invalid_hash_id()


            # check owner
            if publication.owner.id != request.user.id:
                # no http response is needed here.
                # django will generate special error response automatically.
                raise PermissionDenied()


            # process image
            try:
                photo_record = photos_model.add(image, publication)
                return cls.PostResponses.ok(photo_record)

            except PhotosHandlerExceptions.ImageIsTooLarge:
                return cls.PostResponses.image_is_too_large()

            except PhotosHandlerExceptions.ImageIsTooSmall:
                return cls.PostResponses.image_is_too_small()

            except PhotosHandlerExceptions.UnsupportedImageType:
                return cls.PostResponses.unsupported_image_type()

            except PhotosHandlerExceptions.ProcessingFailed:
                return cls.PostResponses.unknown_error()


    class Photos(CabinetView):
        class DeleteResponses(object):
            @staticmethod
            @json_response
            def ok(new_title_photo_hash):
                return {
                    'code': 0,
                    'message': 'OK',
                    'data': {
                        'hash_id': new_title_photo_hash,
                    }
                }


            @staticmethod
            @json_response_bad_request
            def invalid_params():
                return {
                    'code': 1,
                    'message': 'request contains invalid parameters (tid, hid, or pid)',
                }


        @classmethod
        def delete(cls, request, *args):
            try:
                tid, hash_id = args[0].split(':')
                tid = int(tid)
                # hash_id doesnt need to be converted to int
                photo_hash_id = args[1]

            except (IndexError, ValueError):
                return cls.DeleteResponses.invalid_params()


            if tid not in OBJECTS_TYPES.values():
                return cls.DeleteResponses.invalid_params()

            model = HEAD_MODELS[tid]
            try:
                publication = model.objects.filter(hash_id=hash_id).only('id', 'owner')[:1][0]
            except IndexError:
                return cls.DeleteResponses.invalid_params()

            # check owner
            if publication.owner.id != request.user.id:
                raise PermissionDenied()

            # process photo deletion
            try:
                photo = publication.photos_model.objects.get(hash_id=photo_hash_id)
                new_title_photo = photo.remove()
            except ObjectDoesNotExist:
                return cls.DeleteResponses.invalid_params()

            # seems to be OK
            return cls.DeleteResponses.ok(new_title_photo.hash_id if new_title_photo else None)


    class TitlePhoto(CabinetView):
        class PutResponses(object):
            @staticmethod
            @json_response
            def ok():
                return {
                    'code': 0,
                    'message': 'OK',
                }


            @staticmethod
            @json_response_bad_request
            def invalid_tid():
                return {
                    'code': 1,
                    'message': 'Object type id is invalid.'
                }


            @staticmethod
            @json_response_bad_request
            def invalid_hid():
                return {
                    'code': 2,
                    'message': 'Object hash id is invalid.'
                }


            @staticmethod
            @json_response_bad_request
            def invalid_pid():
                return {
                    'code': 3,
                    'message': 'Photo id is invalid.'
                }


        @classmethod
        def put(cls, request, *args):
            """
            Помічає фото з hash_id=photo_hash_id як основне.
            Для даного фото буде згенеровано title_thumb і воно використовуватиметься як початкове у видачі.
            """
            try:
                tid, hash_id = args[0].split(':')
                tid = int(tid)
                # hash_id doesnt need to be converted to int
                photo_hash_id = args[1]

            except (IndexError, ValueError):
                return HttpResponseBadRequest('Invalid parameters.')


            if tid not in OBJECTS_TYPES.values():
                return cls.PutResponses.invalid_tid()


            model = HEAD_MODELS[tid]
            try:
                publication = model.objects.filter(hash_id=hash_id).only('id', 'owner')[:1][0]
            except IndexError:
                return cls.PutResponses.invalid_hid()


            # check owner
            if publication.owner.id != request.user.id:
                raise PermissionDenied()


            # process image
            photos_model = PHOTOS_MODELS[tid]
            try:
                photo = photos_model.objects.get(hash_id=photo_hash_id)
            except ObjectDoesNotExist:
                return cls.PutResponses.invalid_pid()


            photo.mark_as_title()

            # seems to be ok
            return cls.PutResponses.ok()


class DailyRent(object):
    class Reservations(CabinetView):
        class PostResponses(object):
            @staticmethod
            @json_response
            def ok():
                return {
                    'code': 0,
                    'message': 'OK',
                }


            @staticmethod
            @json_response_bad_request
            def invalid_tid():
                return {
                    'code': 1,
                    'message': 'request contains invalid tid.'
                }


            @staticmethod
            @json_response_not_found
            def hash_id_not_found():
                return {
                    'code': 2,
                    'message': 'publication with exact hash id does not exists.'
                }


            @staticmethod
            @json_response_bad_request
            def invalid_date_enter():
                return {
                    'code': 3,
                    'message': 'invalid enter date'
                }


            @staticmethod
            @json_response_bad_request
            def invalid_date_leave():
                return {
                    'code': 4,
                    'message': 'invalid leave date'
                }


            @staticmethod
            @json_response
            def already_booked():
                return {
                    'code': 5,
                    'message': 'Period is already booked',
                }


        class GetResponses(object):
            @staticmethod
            @json_response
            def ok(reservations):
                return {
                    'code': 0,
                    'message': 'OK',
                    'data': [
                        {
                            'date_enter': reservation.date_enter.strftime('%Y-%m-%d'),
                            'date_leave': reservation.date_leave.strftime('%Y-%m-%d'),
                            'client_name': reservation.client_name or '',
                        } for reservation in reservations
                    ]
                }


            @staticmethod
            @json_response_bad_request
            def invalid_tid():
                return {
                    'code': 1,
                    'message': 'request contains invalid tid.'
                }


            @staticmethod
            @json_response_not_found
            def hash_id_not_found():
                return {
                    'code': 2,
                    'message': 'publication with exact hash id does not exists.'
                }


        class DeleteResponses(object):
            @staticmethod
            @json_response
            def ok():
                return {
                    'code': 0,
                    'message': 'OK',
                }


            @staticmethod
            @json_response_bad_request
            def invalid_tid():
                return {
                    'code': 1,
                    'message': 'request contains invalid tid.'
                }


            @staticmethod
            @json_response_not_found
            def hash_id_not_found():
                return {
                    'code': 2,
                    'message': 'publication with exact hash id does not exists.'
                }


            @staticmethod
            @json_response_bad_request
            def invalid_date_enter():
                return {
                    'code': 3,
                    'message': 'invalid enter date'
                }


            @staticmethod
            @json_response_bad_request
            def invalid_date_leave():
                return {
                    'code': 4,
                    'message': 'invalid leave date'
                }


        @classmethod
        def post(cls, request, *args):
            publication_tid, publication_hash_id = args[:2]
            publication_tid = int(publication_tid)


            try:
                params = angular_parameters(request, ['date_enter', 'date_leave'])
            except ValueError:
                return cls.PostResponses.invalid_date_enter()


            # Service potentially will work in several countries.
            # Each of this country may have different time zone code.
            # But reservations must be done in ime zone of country, publication is from.
            #
            # Currently it is not necessary.
            # Ukraine time zone should be used.
            # todo: add timezone handling here

            try:
                # format is 2015-09-18T09:00:00.000Z
                date_enter = params['date_enter'][:10]
                date_enter = datetime.datetime.strptime(date_enter, '%Y-%m-%d')
                date_enter = date_enter.replace(tzinfo=timezone('Europe/Kiev'))
                date_enter = date_enter.date()
            except ValueError:
                return cls.PostResponses.invalid_date_enter()

            try:
                date_leave = params['date_leave'][:10]
                date_leave = datetime.datetime.strptime(date_leave, '%Y-%m-%d')
                date_leave = date_leave.replace(tzinfo=timezone('Europe/Kiev'))
                date_leave = date_leave.date()
            except ValueError:
                return cls.PostResponses.invalid_date_leave()

            if date_enter > date_leave:
                return cls.PostResponses.invalid_date_enter()


            publications_model = HEAD_MODELS.get(publication_tid)
            if not publications_model:
                return cls.PostResponses.invalid_tid()


            try:
                publication = publications_model.objects\
                    .filter(hash_id=publication_hash_id)\
                    .only('id', 'owner', 'rent_terms__period_sid')\
                    [:1][0]

                if publication.owner != request.user:
                    raise SuspiciousOperation()
                
                if not publication.rent_terms.is_daily:
                    raise SuspiciousOperation(
                        'Trying to add daily reservation to publication that is not published as daily rent.')

            except IndexError:
                return cls.PostResponses.hash_id_not_found()


            daily_rent_reservations_model = DAILY_RENT_RESERVATIONS_MODELS.get(publication_tid)
            if not daily_rent_reservations_model:
                return cls.PostResponses.invalid_tid()


            try:
                daily_rent_reservations_model.objects.make_reservation(
                    publication, date_enter, date_leave, params.get('client_name'))

            except LivingDailyRentModel.AlreadyBooked:
                return cls.PostResponses.already_booked()


            return cls.PostResponses.ok()


        @classmethod
        def get(cls, request, *args):
            publication_tid, publication_hash_id = args[:2]
            publication_tid = int(publication_tid)


            publications_model = HEAD_MODELS.get(publication_tid)
            if not publications_model:
                return cls.GetResponses.invalid_tid()

            try:
                publication = publications_model.objects\
                    .filter(hash_id=publication_hash_id)\
                    .only('id')\
                    [:1][0]

            except IndexError:
                return cls.GetResponses.hash_id_not_found()


            daily_rent_reservations_model = DAILY_RENT_RESERVATIONS_MODELS.get(publication_tid)
            if not daily_rent_reservations_model:
                return cls.PostResponses.invalid_tid()


            reservations = daily_rent_reservations_model.objects.filter(publication=publication)
            return cls.GetResponses.ok(reservations)


        @classmethod
        def delete(cls, request, *args):
            publication_tid, publication_hash_id = args[:2]
            publication_tid = int(publication_tid)


            try:
                params = angular_parameters(request, ['date_enter', 'date_leave'])
            except ValueError:
                return cls.DeleteResponses.invalid_date_enter()


            # Service potentially will work in several countries.
            # Each of this country may have different time zone code.
            # But reservations must be done in ime zone of country, publication is from.
            #
            # Currently it is not necessary.
            # Ukraine time zone should be used.
            # todo: add timezone handling here

            try:
                # format is 2015-09-18T09:00:00.000Z
                date_enter = params['date_enter'][:10]
                date_enter = datetime.datetime.strptime(date_enter, '%Y-%m-%d')
                date_enter = date_enter.replace(tzinfo=timezone('Europe/Kiev'))
                date_enter = date_enter.date()
            except ValueError:
                return cls.DeleteResponses.invalid_date_enter()

            try:
                date_leave = params['date_leave'][:10]
                date_leave = datetime.datetime.strptime(date_leave, '%Y-%m-%d')
                date_leave = date_leave.replace(tzinfo=timezone('Europe/Kiev'))
                date_leave = date_leave.date()
            except ValueError:
                return cls.DeleteResponses.invalid_date_leave()

            if date_enter > date_leave:
                return cls.PostResponses.invalid_date_enter()


            publications_model = HEAD_MODELS.get(publication_tid)
            if not publications_model:
                return cls.DeleteResponses.invalid_tid()


            try:
                publication = publications_model.objects\
                    .filter(hash_id=publication_hash_id)\
                    .only('id', 'owner', 'rent_terms__period_sid')\
                    [:1][0]

                if publication.owner != request.user:
                    raise SuspiciousOperation()

                if not publication.rent_terms.is_daily:
                    raise SuspiciousOperation(
                        'Trying to add daily reservation to publication that is not published as daily rent.')

            except IndexError:
                return cls.DeleteResponses.hash_id_not_found()


            daily_rent_reservations_model = DAILY_RENT_RESERVATIONS_MODELS.get(publication_tid)
            if not daily_rent_reservations_model:
                return cls.DeleteResponses.invalid_tid()


            daily_rent_reservations_model.objects.cancel_reservation(publication, date_enter, date_leave)
            return cls.DeleteResponses.ok()


class Briefs(CabinetView):
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
        briefs = cls.__briefs_of_section(section, request.user.id)
        return cls.GetResponses.ok(briefs)


    @classmethod
    def __briefs_of_section(cls, section, user_id):
        pubs = []
        for tid in OBJECTS_TYPES.values():
            query = HEAD_MODELS[tid].by_user_id(user_id).only('id')

            if section == 'all':
                query = query.all().order_by('state_sid', 'created')
            elif section == 'published':
                query = query.filter(state_sid = OBJECT_STATES.published(), deleted=None).order_by('state_sid', 'created')
            elif section == 'unpublished':
                query = query.filter(state_sid = OBJECT_STATES.unpublished(), deleted=None).order_by('state_sid', 'created')
            elif section == 'trash':
                query = query.filter(state_sid = OBJECT_STATES.deleted()).order_by('state_sid', 'deleted')
            else:
                raise ValueError('Invalid section title {0}'.format(section))

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
            'id', 'hash_id', 'state_sid', 'created', 'body__title', 'body__description', 'for_rent', 'for_sale')
        if not publications_list:
            return []

        model = HEAD_MODELS[tid]


        # Briefs may contain messages for the users from the moderators.
        moderators_messages = cls.__load_moderators_messages(tid, publications_list)


        result = []
        for publication in publications_list:
            record = {
                'tid':          tid,
                'hid':          publication[1], # hash_id
                'state_sid':    publication[2], # state_sid
                'created':      publication[3].strftime('%Y-%m-%dT%H:%M:%SZ'),
                'title':        publication[4], # body.title
                'description':  publication[5], # body.description
                'for_rent':     publication[6], # for_rent
                'for_sale':     publication[7], # for_sale

                'moderator_message': moderators_messages.get(publication[1]) # hash_id

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

        moderators_messages = RejectedPublications.objects\
            .by_publications_ids(ids)\
            .values_list('publication_hash_id', 'message')

        return {
            hash_id: message for hash_id, message in moderators_messages
        }