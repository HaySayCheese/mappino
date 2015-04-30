# coding=utf-8
from collective.decorators.views import anonymous_required, login_required_or_forbidden
from core.customers.models import Customers
from django.core.exceptions import ObjectDoesNotExist
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


class CustomerView(View):
    """
    Base class for all views that should process customers.
    Useful to handle customer hash id cookie.
    """

    @staticmethod
    def get_customer_hash_id(request):
        """
        Returns customers hash id or None if no customer hash id cookie is available.
        """
        try:
            return request.get_signed_cookie('customer_hash_id')
        except ValueError:
            return None


    @classmethod
    def get_customer(cls, request):
        """
        Returns customer record or None if no customer hash id cookie is available,
        or no such customer in database.
        """
        hash_id = cls.get_customer_hash_id(request)
        if not hash_id:
            return None

        try:
            return Customers.objects.get(hash_id=hash_id)
        except ObjectDoesNotExist:
            return None


    @classmethod
    def get_customer_queryset(cls, request):
        """
        Returns queryset with customer or empty queryset if no customer hash id cookie is available,
        or no such customer in database.
        """
        hash_id = cls.get_customer_hash_id(request)
        if not hash_id:
            return Customers.objects.none()

        return Customers.objects.filter(hash_id=hash_id).only('id')


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