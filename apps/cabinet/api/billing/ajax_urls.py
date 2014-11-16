from django.conf.urls import patterns, url
from apps.cabinet.api.billing.ajax import Billing


urlpatterns = patterns('',
    url(r'^ajax/api/cabinet/billing/realtor/plan/$', Billing.Realtor.Plan.as_view()),
    url(r'^ajax/api/cabinet/billing/realtor/transactions/$', Billing.Realtor.Transactions.as_view()),
    url(r'^ajax/api/cabinet/billing/realtor/orders/$', Billing.Realtor.Orders.as_view()),

    url(r'^callback/api/cabinet/billing/realtor/order/$', Billing.Realtor.OrdersCallback.as_view()),
)