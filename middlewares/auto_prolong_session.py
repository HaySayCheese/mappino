#coding=utf-8


class AutoProlongSession(object):
    """
    Automatically prolongs sessions for authenticated user if the request was processed fine.
    """

    session_expire = 60*60*24*12 # 12 days

    def process_response(self, request, response):
        if response.status_code == 200 and request.user.is_authenticated():
            request.session.set_expiry(self.session_expire)
        return response