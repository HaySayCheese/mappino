#coding=utf-8
import copy
import json

from django.http import HttpResponseBadRequest, HttpResponse
from django.views.generic import View

from collective.exceptions import InvalidHttpParameter
from core.publications.constants import OBJECTS_TYPES, HEAD_MODELS



class RealtorsContacts(View):
    """
    Implements operations for getting contacts of realtors on main pages of the site.
    """
    get_codes = {
        'OK': {
            'code': 0,
            'contacts': None, # WARN: realtors contacts here
        },
        'invalid_parameters': {
            'code': 1
        },
        'invalid_tid': {
            'code': 2
        },
        'invalid_hash_id': {
            'code': 3
        },
    }


    def get(self, request, *args):
        """
        Повертає JSON-відповідь з переліком контактів рієлтора та його уподобаннями з приводу зв’язку із ним.
        У випадку виникнення помилки поверне JSON-відповідь з кодом помилки.

        :param request: <ignored>
        :param args:
            [0]: заголовок оголошення у вигляді <tid:hash_id>, де tid — тип оголошення, а hash_id — хеш оголошення.
        :return:
            JSON http response
        """

        try:
            tid, hash_hid = args[0].split(':')
            if (tid is None) or (hash_hid is None):
                raise InvalidHttpParameter()

        except (
            IndexError, # args doesn't contains required params
            InvalidHttpParameter, # tid or hash_id is None
        ):
            return HttpResponseBadRequest(
                json.dumps(self.get_codes['invalid_parameters']), content_type='application/json')


        try:
            tid = int(tid)
            if tid not in OBJECTS_TYPES.values():
                raise InvalidHttpParameter()

        except (
            InvalidHttpParameter, # tid is incorrect object type
            ValueError, # tid is not an int
        ):
            return HttpResponseBadRequest(
                json.dumps(self.get_codes['invalid_tid']), content_type='application/json')


        model = HEAD_MODELS[tid]
        try:
            publication = model.objects.filter(hash_id=hash_hid).only('id', 'owner')[:1][0]
        except (
            IndexError, # model doesn't contains record with such hash_id
        ):
            return HttpResponse( # request semantically is correct
                json.dumps(self.get_codes['invalid_hash_id']), content_type='application/json')


        realtor = publication.owner
        preferences = realtor.preferences()


        # process_contacts_request() зніме платню з рієлтора згідно з умовами тарифного плану.
        # Даний метод викликається під час будь-якого запиту контактів і для будь-якого рієлтора,
        # незалежно від того, на якому тарифному плані він знаходиться.
        # Перевірка тарифного плану та ін. перевірки такого роду будуть виконані вже в межах даного методу.
        # Це зроблено для того, щоб інкапсулювати логіку біллінга в одному модулі і не розмазувати її по всім в’юхам.
        # process_contacts_request() ніби виступає обробником події запиту контактів,
        # а будуть зняті гроші з рієлтора чи ні - питання цього методу.
        realtor.account().process_contacts_request(request)


        response = copy.deepcopy(self.get_codes['OK']) # WARN: deep copy here
        response.update({
            'contacts':  realtor.contacts_dict(),
            'preferences': {
                'allow_call_requests': preferences.allow_call_requests,
                'allow_messaging': preferences.allow_messaging,
            }
        })
        return HttpResponse(json.dumps(response), content_type='application/json')