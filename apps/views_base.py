# coding=utf-8
from django.http.response import HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views.generic import View

from collective.decorators.views import anonymous_required, login_required_or_forbidden


class AnonymousOnlyView(View):
    """
    Base class for all anonymous only views.
    The only purpose of using this view is to reject all authenticated requests.
    """

    @method_decorator(anonymous_required)
    def dispatch(self, *args, **kwargs):
        return super(AnonymousOnlyView, self).dispatch(*args, **kwargs)


class AuthenticatedOnlyView(View):
    """
    Base class for all authenticated only views.
    The only purpose of using this view is to reject all anonymous requests.
    """

    @method_decorator(login_required_or_forbidden)
    def dispatch(self, *args, **kwargs):
        return super(AuthenticatedOnlyView, self).dispatch(*args, **kwargs)


class CabinetView(AuthenticatedOnlyView):
    pass


class ModeratorsView(AuthenticatedOnlyView):
    def dispatch(self, *args, **kwargs):
        request = args[0]
        if not request.user.is_moderator:
            return HttpResponseForbidden('User should have moderators permissions.')

        return super(ModeratorsView, self).dispatch(*args, **kwargs)
