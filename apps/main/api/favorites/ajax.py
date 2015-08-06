# coding=utf-8
from apps.classes import AuthenticatedOnlyView
from collective.decorators.ajax import json_response, json_response_bad_request, json_response_not_found
from collective.http.responses import *
from collective.methods.request_data_getters import angular_parameters
from core.favorites.constants import FAVORITES_MODELS
from core.favorites.exceptions import PublicationDoesNotExists
from core.markers_index.models import SegmentsIndex
from core.publications.models import HEAD_MODELS


class FavoritesListView(AuthenticatedOnlyView):
    class GetResponses(object):
        @staticmethod
        @json_response
        def ok(favorites_list):
            return {
                'code': 0,
                'message': 'OK',
                'data': [record for record in favorites_list]
            }


        @staticmethod
        @json_response
        def anonymous_user():
            return {
                'code': 1,
                'message': 'User must be authenticated.'
            }


    class PostResponses(object):
        @staticmethod
        @json_response
        def ok():
            return {
                'code': 0,
                'message': 'OK'
            }


        @staticmethod
        @json_response_bad_request
        def invalid_params():
            return {
                'code': 1,
                'message': 'Request does not contains valid parameters.'
            }


        @staticmethod
        @json_response_not_found
        def no_such_publication():
            return {
                'code': 2,
                'message': 'There is no publication with exact id.'
            }


    class DeleteResponses(object):
        @staticmethod
        @json_response
        def ok():
            return {
                'code': 0,
                'message': 'OK'
            }


    @classmethod
    def get(cls, request):
        """
        :returns:
            All the favorites of the authenticated user.
        """
        tids_and_publications_ids = {}

        for tid, favorites_model in FAVORITES_MODELS.iteritems():
            publications = favorites_model.queryset_by_user(request.user).only('publication_id')
            if publications:
                tids_and_publications_ids[tid] = [p.publication_id for p in publications]


        briefs = SegmentsIndex.format_favorites(tids_and_publications_ids)
        return cls.GetResponses.ok(briefs)


    @classmethod
    def post(cls, request):
        """
        Adds publication to the user's favorites.
        """
        try:
            publication_id = angular_parameters(request, ['publication_id'])['publication_id']
            tid, hash_id = publication_id.split(':')
            tid = int(tid)
        except ValueError:
            return cls.PostResponses.invalid_params()


        try:
            model = HEAD_MODELS[tid]
            publication = model.objects.filter(hash_id=hash_id).only('id')[:1][0]
        except KeyError:
            return cls.PostResponses.invalid_params()

        except IndexError:
            return cls.PostResponses.no_such_publication()


        try:
            favorites_model = FAVORITES_MODELS[tid]
            favorites_model.add(request.user, publication)

        except KeyError:
            return cls.PostResponses.invalid_params()

        except PublicationDoesNotExists:
            return cls.PostResponses.no_such_publication()


        return cls.PostResponses.ok()


    @classmethod
    def delete(cls, request, *args):
        """
        Removes publication with of type "tid" and hash = "hash_id" from the user's favorites.
        """
        try:
            tid = int(args[0])
            hash_id = args[1]
        except ValueError:
            return cls.PostResponses.invalid_params()


        try:
            model = HEAD_MODELS[tid]
            publication = model.objects.filter(hash_id=hash_id).only('id')[:1][0]
        except KeyError:
            return cls.PostResponses.invalid_params()

        except IndexError:
            return cls.PostResponses.no_such_publication()


        try:
            favorites_model = FAVORITES_MODELS[tid]
            favorites_model.objects.filter(publication_id = publication.id).delete()

        except KeyError:
            return cls.PostResponses.invalid_params()


        return cls.PostResponses.ok()




    @classmethod
    def __get_information_about_publications(cls, record_with_favorites):
        """
        :returns:
            Serializes and returns brief information about favorite publications.

            This method is not optimized, but it is not necessary,
            because the average user will not have more than 10 favorite publications.
        """
        publications_ids = json.loads(record_with_favorites.publications_ids)

        list_with_publications_ids = [publication_ids.split(":",2) for publication_ids in publications_ids]
        list_with_publications_ids = [
            (int(publication_ids[0]), publication_ids[1]) for publication_ids in list_with_publications_ids
        ]

        list_with_publications_info = []
        for tid, hash_id in list_with_publications_ids:
            model = HEAD_MODELS[tid]
            publication = model.objects.filter(hash_id=hash_id).only('body__title')[:1][0]

            # photos = publication.photos().only('big_thumb_url')
            # big_thumb_urls = [photo.big_thumb_url for photo in photos]
            list_with_publications_info.append({
                'id': "{tid}:{hid}".format(tid, hash_id),
                'title': publication.body.title,
                #'photos':big_thumb_urls,

            })

        return list_with_publications_info