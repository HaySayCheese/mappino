# coding=utf-8
from apps.classes import AuthenticatedOnlyView
from collective.decorators.ajax import json_response
from collective.http.responses import *
from collective.methods.request_data_getters import angular_parameters
from core.favorites.models import Favorites
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
        @json_response
        def invalid_params():
            return {
                'code': 1,
                'message': 'Request does not contains valid parameters.'
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
        record_with_favorites = Favorites.by_user(request.user.id)
        if not record_with_favorites:
            # user does not have favorites,
            # lets return empty response
            return cls.GetResponses.ok([])


        favorites_info = cls.__get_information_about_publications(record_with_favorites)
        return cls.GetResponses.ok(favorites_info)


    @classmethod
    def post(cls, request):
        """
        Adds publication to the user's favorites.
        """
        try:
            publication_id = angular_parameters(request, ['publication_id'])['publication_id']
            tid, hash_id = publication_id['id'].split(':')
            tid = int(tid)
        except ValueError:
            return cls.PostResponses.invalid_params()


        Favorites.add(request.user, tid, hash_id)
        return cls.PostResponses.ok()


    @classmethod
    def delete(cls, request, tid, hash_id):
        """
        Removes publication with of type "tid" and hash = "hash_id" from the user's favorites.
        """
        Favorites.remove(request.user.id, tid, hash_id)
        return cls.DeleteResponses.ok()


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