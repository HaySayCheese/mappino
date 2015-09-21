# coding=utf-8


class UserCookie(object):
    """
    Checks if user is logged in and if so - creates/updates special cookie,
    to indicate for the front-end that user is logged in.
    """

    cookie_name = 'user'

    @classmethod
    def process_response(cls, request, response):
        if request.user.is_authenticated():
            response.set_cookie(cls.cookie_name, '')

        else:
            response.delete_cookie(cls.cookie_name)

        return response