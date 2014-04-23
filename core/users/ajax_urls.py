from django.conf.urls import patterns, url
from core.users.ajax.main import \
	RegistrationManager as RegistrationManager, \
	LoginManager as LoginManager



urlpatterns = patterns('',
    # validators
    url(r'^ajax/api/accounts/validate-email/$', RegistrationManager.EmailValidation.as_view()),
    url(r'^ajax/api/accounts/validate-phone-number/$', RegistrationManager.MobilePhoneValidation.as_view()),


	# registration
    url(r'^ajax/api/accounts/registration/$', RegistrationManager.Registration.as_view()),
    url(r'^ajax/api/accounts/registration/cancel/$', RegistrationManager.CancelRegistration.as_view()),
    url(r'^ajax/api/accounts/registration/resend-sms/$', RegistrationManager.ResendCheckSMS.as_view()),


    # login
	url(r'^ajax/api/accounts/login/$', LoginManager.Login.as_view()),
	url(r'^ajax/api/accounts/logout/$', LoginManager.Logout.as_view()),
    url(r'^ajax/api/accounts/on-login-info/$', LoginManager.OnLogin.as_view()),


	# password reset
	url(r'^ajax/api/accounts/password-reset/$', 'apps.accounts.accounts_ajax.password_reset_handler'),
    url(r'^ajax/api/accounts/password-reset/check/$', 'apps.accounts.accounts_ajax.check_token_handler'),
)