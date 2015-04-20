from collective.decorators.views import anonymous_required, login_required_or_forbidden
from django.utils.decorators import method_decorator
from django.views.generic import View



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