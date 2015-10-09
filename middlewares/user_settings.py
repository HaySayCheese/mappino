# coding=utf-8


class UserCookie(object):
    """
    Checks if user is logged in and if so - creates/updates special cookie,
    to indicate for the front-end that user is logged in.
    """

    cookie_name = 'user'

    @classmethod
    def process_response(cls, request, response):
        if 200 < response.status_code < 299:
            if hasattr(request, 'user') and request.user.is_authenticated():
                response.set_cookie(cls.cookie_name, '')
            else:
                response.delete_cookie(cls.cookie_name)

        # responses about errors and redirects should not be modified

        return response
