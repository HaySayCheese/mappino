# coding=utf-8
from apps.common.api.accounts.ajax import RegistrationManager, LoginManager, AccessRestoreManager
from django.conf.urls import patterns, url



urlpatterns = patterns('',
    # validators
        # ajax
        url(r'^ajax/api/accounts/validate-email/$', RegistrationManager.EmailValidation.as_view()),
        url(r'^ajax/api/accounts/validate-phone-number/$', RegistrationManager.MobilePhoneValidation.as_view()),


    # registration
        # ajax
        url(r'^ajax/api/accounts/registration/$', RegistrationManager.Registration.as_view()),
        url(r'^ajax/api/accounts/registration/cancel/$', RegistrationManager.CancelRegistration.as_view()),
        url(r'^ajax/api/accounts/registration/resend-sms/$', RegistrationManager.ResendCheckSMS.as_view()),


    # login
        # ajax
        url(r'^ajax/api/accounts/login/$', LoginManager.Login.as_view()),
        url(r'^ajax/api/accounts/logout/$', LoginManager.Logout.as_view()),
        url(r'^ajax/api/accounts/on-login-info/$', LoginManager.OnLogin.as_view()),


    # password reset
        # get
        url(r'^accounts/access-restore/redirect/$', AccessRestoreManager.RedirectFromEmail.as_view()),

        # ajax
        url(r'^ajax/api/accounts/password-reset/$', AccessRestoreManager.BeginRestore.as_view()),
        url(r'^ajax/api/accounts/password-reset/restore/$', AccessRestoreManager.Check.as_view()),
)