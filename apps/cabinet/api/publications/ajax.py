# coding=utf-8
import copy
import json

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, ValidationError
from django.http.response import HttpResponse, HttpResponseBadRequest

from collective.http.responses import HttpJsonResponseBadRequest, HttpJsonResponse
from collective.methods.request_data_getters import angular_parameters

from apps.classes import CabinetView
from core.publications import classes
from core.publications.exceptions import PhotosHandlerExceptions
from core.publications.constants import OBJECTS_TYPES, HEAD_MODELS, PHOTOS_MODELS
from core.publications.models_signals import record_updated
from core.publications.update_methods.flats import update_flat
from core.publications.update_methods.houses import update_house
from core.publications.update_methods.offices import update_office
from core.publications.update_methods.rooms import update_room
from core.publications.update_methods.trades import update_trade
from core.publications.update_methods.warehouses import update_warehouse
from core.publications.update_methods.business import update_business
from core.publications.update_methods.garages import update_garage
from core.publications.update_methods.lands import update_land


class Publications(CabinetView):
    class PostResponses(object):
        @staticmethod
        def ok(publication_hash_id):
            return HttpJsonResponse({
                'code': 0,
                'message': 'OK',
                'data': {
                    'id': publication_hash_id,
                }
            })

        @staticmethod
        def invalid_parameters():
            return HttpJsonResponseBadRequest({
                'code': 1,
                'message': 'Request does not contains valid parameters or one of them is incorrect.',
            })


    @classmethod
    def post(cls, request):
        try:
            params = angular_parameters(request, ['tid', 'for_sale', 'for_rent'])

            tid = params['tid']
            is_sale = params['for_sale']
            is_rent = params['for_rent']

            model = HEAD_MODELS[tid]
        except (ValueError, KeyError):
            return cls.PostResponses.invalid_parameters()


        record = model.new(request.user, is_sale, is_rent)
        return cls.PostResponses.ok(record.hash_id)



class Publication(CabinetView):
    class GetResponses(object):
        @staticmethod
        def ok(publication_data):
            return HttpJsonResponse({
                'code': 1,
                'message': 'OK',
                'data': publication_data,
            })


        @staticmethod
        def invalid_parameters():
            return HttpResponseBadRequest({
                'code': 1,
                'message': 'Request does not contains valid parameters or one of them is incorrect.'
            })


    class PutResponses(object):
        @staticmethod
        def ok(new_value):
            if new_value:
                return HttpJsonResponse({
                    'code': 0,
                    'message': 'OK',
                    'data': {
                        'value': new_value,
                    }
                })

            else:
                return HttpJsonResponse({
                    'code': 0,
                    'message': 'OK',
                })

        @staticmethod
        def invalid_parameters():
            return HttpResponseBadRequest({
                'code': 1,
                'message': 'Request does not contains valid parameters or one of them is incorrect.'
            })


    class DeleteResponses(object):
        @staticmethod
        def ok():
            return HttpJsonResponse({
                'code': 0,
                'message': 'OK',
            })

        @staticmethod
        def invalid_parameters():
            return HttpResponseBadRequest({
                'code': 1,
                'message': 'Request does not contains valid parameters or one of them is incorrect.'
            })


    def __init__(self):
        super(Publication, self).__init__()
        self.published_formatter = classes.CabinetPublishedDataSource()
        self.unpublished_formatter = classes.UnpublishedFormatter()


    def get(self, request, *args):
        try:
            tid, hash_id = args[:]
            tid = int(tid)
            model = HEAD_MODELS[tid]

        except (IndexError, ValueError, KeyError):
            return self.GetResponses.invalid_parameters()


        try:
            head = model.by_hash_id(hash_id, select_body=True)
        except ObjectDoesNotExist:
            return self.GetResponses.invalid_parameters()


        # check owner
        if head.owner.id != request.user.id:
            raise PermissionDenied()


        # seems to be ok
        if head.is_published() or head.is_deleted():
            response = self.published_formatter.format(tid, head)
        else:
            response = self.unpublished_formatter.format(tid, head)

        return self.GetResponses.ok(response)


    def put(self, request, *args):
        try:
            tid, hash_id = args[:]
            tid = int(tid)
            model = HEAD_MODELS[tid]

            parameters = angular_parameters(request, ['f'])
            field = parameters['f']
            value = parameters['v'] # may be ''

        except (IndexError, ValueError, KeyError):
            return self.PutResponses.invalid_parameters()


        try:
            head = model.objects.filter(hash_id=hash_id).only('id', 'owner')[0]
        except IndexError:
             return self.PutResponses.invalid_parameters()


        # check owner
        if head.owner.id != request.user.id:
            raise PermissionDenied()


        returned_value = None

        # todo: move this into models as a method
        # Жилая недвижимость
        if tid == OBJECTS_TYPES.flat():
            returned_value = update_flat(head, field, value, tid)

        elif tid == OBJECTS_TYPES.house():
            returned_value = update_house(head, field, value, tid)

        elif tid == OBJECTS_TYPES.room():
            returned_value = update_room(head, field, value, tid)

        # Коммерческая недвижимость
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

        elif tid == OBJECTS_TYPES.business():
            returned_value = update_business(head, field, value, tid)


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

        return self.PutResponses.ok(returned_value)


    def delete(self, request, *args):
        try:
            tid, hash_id = args[:]
            tid = int(tid)
            # hash_id doesnt need to be converted to int

            model = HEAD_MODELS[tid]
        except (IndexError, ValueError):
            return self.DeleteResponses.invalid_parameters()


        try:
            head = model.objects.filter(hash_id=hash_id).only('id', 'owner')[0]
        except IndexError:
            return self.DeleteResponses.invalid_parameters()


        # check owner
        if head.owner.id != request.user.id:
            raise PermissionDenied()


        if not 'permanent' in request.path:
            # note: no real deletion here.
            # all publications that was deleted are situated in trash
            head.mark_as_deleted()
        else:
            head.delete_permanent()

        return self.DeleteResponses.ok()



    class Publish(CabinetView):
        put_codes = {
            'OK': {
                'code': 0,
            },
            'invalid_hid': {
                'code': 1,
            },
            'incomplete_or_invalid_pub': {
                'code': 2,
            },

            'pay_as_you_go_insufficient_funds': {
                'code': 30,
            },
            'fixed_insufficient_funds': {
                'code': 50,
            },
        }


        def put(self, request, *args):
            try:
                tid, hash_id = args[0].split(':')
                tid = int(tid)
                # hash_id doesnt need to be converted to int
            except (IndexError, ValueError):
                return HttpResponseBadRequest('Invalid parameters.')


            model = HEAD_MODELS[tid]
            try:
                head = model.objects.filter(hash_id=hash_id).only('id', 'owner')[0]
            except IndexError:
                return HttpResponseBadRequest(json.dumps(
                    self.put_codes['invalid_hid']), content_type='application/json')


            # check owner
            if head.owner.id != request.user.id:
                raise PermissionDenied()


            # todo: enable billing check back
            # try:
            #     # billing constraints check
            #     request.user.account.check_may_publish_publications()
            #
            # except billing_exceptions.PAYGInsufficientFunds:
            #     return HttpJsonResponse(self.put_codes['pay_as_you_go_insufficient_funds'])
            #
            # except billing_exceptions.FixedInsufficientFunds:
            #     return HttpJsonResponse(self.put_codes['fixed_insufficient_funds'])


            try:
                head.publish()
            except ValidationError:
                return HttpResponseBadRequest(json.dumps(
                    self.put_codes['incomplete_or_invalid_pub']), content_type='application/json')

            # seems to be ok
            return HttpResponse(json.dumps(
                self.put_codes['OK']), content_type='application/json')


    class Unpublish(CabinetView):
        put_codes = {
            'OK': {
                'code': 0,
            },
            'invalid_hid': {
                'code': 1,
            },
        }


        def put(self, request, *args):
            try:
                tid, hash_id = args[0].split(':')
                tid = int(tid)
                # hash_id doesnt need to be converted to int
            except (IndexError, ValueError):
                return HttpResponseBadRequest('Invalid parameters.')


            model = HEAD_MODELS[tid]
            try:
                head = model.objects.filter(hash_id=hash_id).only('id', 'owner')[0]
            except IndexError:
                return HttpResponseBadRequest(json.dumps(
                    self.put_codes['invalid_hid']), content_type='application/json')


            # check owner
            if head.owner.id != request.user.id:
                raise PermissionDenied()

            # seems to be ok
            head.unpublish()
            return HttpResponse(json.dumps(
                self.put_codes['OK']), content_type='application/json')


    class UploadPhoto(CabinetView):
        class PostResponses(object):
            @staticmethod
            def ok(photo):
                return HttpJsonResponse({
                    'code': 0,
                    'message': 'OK',
                    'data': {
                        'hash_id': photo.hash_id,
                        'is_title': photo.check_is_title(),
                        'thumbnail': photo.big_thumb_url,
                    }
                })


            @staticmethod
            def invalid_tid():
                return HttpJsonResponseBadRequest({
                    'code': 1,
                    'message': 'request does not contains param "tid", or it is invalid.'
                })


            @staticmethod
            def invalid_hash_id():
                return HttpJsonResponseBadRequest({
                    'code': 2,
                    'message': 'request does not contains param "hash_id" or it is invalid.'
                })


            @staticmethod
            def image_is_absent():
                return HttpJsonResponseBadRequest({
                    'code': 3,
                    'message': 'request does not contains image file "file". '
                })


            @staticmethod
            def image_is_too_large():
                return HttpJsonResponseBadRequest({
                    'code': 4,
                    'message': 'request contains image that is greater than max. allowable.'
                })


            @staticmethod
            def image_is_too_small():
                return HttpJsonResponseBadRequest({
                    'code': 5,
                    'message': 'request contains image that is smaller than min. allowable.'
                })


            @staticmethod
            def unsupported_image_type():
                return HttpJsonResponseBadRequest({
                    'code': 6,
                    'message': 'request contains image of unsupported type.'
                })

            # ...
            # other response handlers goes here
            # ...


            @staticmethod
            def unknown_error():
                return HttpJsonResponseBadRequest({
                    'code': 100,
                    'message': 'unknown error occurred.'
                })


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
        delete_codes = {
            'OK': {
                'code': 0,
            },
            'invalid_tid': {
                'code': 1,
            },
            'invalid_hid': {
                'code': 2,
            },
            'invalid_pid': {
                'code': 3,
            },
        }


        def delete(self, request, *args):
            try:
                tid, hash_id = args[0].split(':')
                tid = int(tid)
                # hash_id doesnt need to be converted to int
                photo_hash_id = args[1]

            except (IndexError, ValueError):
                return HttpResponseBadRequest('Invalid parameters.')


            if tid not in OBJECTS_TYPES.values():
                return HttpResponseBadRequest(
                    json.dumps(self.delete_codes['invalid_tid']), content_type='application/json')

            model = HEAD_MODELS[tid]
            try:
                publication = model.objects.filter(hash_id=hash_id).only('id', 'owner')[:1][0]
            except IndexError:
                return HttpResponseBadRequest(
                    json.dumps(self.delete_codes['invalid_hid']), content_type='application/json')


            # check owner
            if publication.owner.id != request.user.id:
                raise PermissionDenied()


            # process photo deletion
            try:
                photo = publication.photos_model.objects.get(hash_id=photo_hash_id)
                new_title_photo = photo.remove()
            except ObjectDoesNotExist:
                return HttpResponseBadRequest(
                    json.dumps(self.delete_codes['invalid_pid']), content_type='application/json')

            # seems to be OK
            response = copy.deepcopy(self.delete_codes['OK'])
            if new_title_photo is None:
                response['photo_hash_id'] = None
                response['brief_url'] = None
            else:
                response['photo_hash_id'] = new_title_photo.hash_id
                response['brief_url'] = new_title_photo.url() + new_title_photo.small_thumbnail_name()

            return HttpResponse(json.dumps(response), content_type='application/json')


    class PhotoTitle(CabinetView):
        post_codes = {
            'OK': {
                'code': 0,
            },
            'invalid_tid': {
                'code': 1,
            },
            'invalid_hid': {
                'code': 2,
            },
            'invalid_pid': {
                'code': 3,
            },
        }


        def post(self, request, *args):
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
                return HttpResponseBadRequest(
                    json.dumps(self.post_codes['invalid_tid']), content_type='application/json')

            model = HEAD_MODELS[tid]
            try:
                publication = model.objects.filter(hash_id=hash_id).only('id', 'owner')[:1][0]
            except IndexError:
                return HttpResponseBadRequest(
                    json.dumps(self.post_codes['invalid_hid']), content_type='application/json')


            # check owner
            if publication.owner.id != request.user.id:
                raise PermissionDenied()


            # process image
            photos_model = PHOTOS_MODELS[tid]
            try:
                photo = photos_model.objects.get(hash_id=photo_hash_id)
            except ObjectDoesNotExist:
                return HttpResponseBadRequest(
                    json.dumps(self.post_codes['invalid_pid']), content_type='application/json')

            photo.mark_as_title()

            # seems to be ok
            response = copy.deepcopy(self.post_codes['OK'])
            response['brief_url'] = publication.title_small_thumbnail_url()
            return HttpResponse(json.dumps(response), content_type='application/json')