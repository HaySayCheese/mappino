'use strict'

###*
# @class
# @description todo: add desc
# @version 0.8.2
# @license todo: add license
###
class BAuthService
    constructor: (@http, @cookieStore) ->
        @URL =
            'LOGIN':                        '/ajax/api/accounts/login/'
            'LOGOUT':                       '/ajax/api/accounts/logout/'
            'REGISTRATION':                 '/ajax/api/accounts/registration/'
            'CANCEL_REGISTRATION':          '/ajax/api/accounts/registration/cancel/'
            'RESEND_SMS_CODE':              '/ajax/api/accounts/registration/resend-sms/'
            'VALIDATE_SMS_CODE':            '/ajax/api/accounts/registration/'
            'VALIDATE_EMAIL':               '/ajax/api/accounts/validate-email/'
            'VALIDATE_PHONE':               '/ajax/api/accounts/validate-phone-number/'
            'GET_USER_NAME':                '/ajax/api/accounts/on-login-info/'
            'RESTORE_ACCESS_SEND_EMAIL':    '/ajax/api/accounts/password-reset/'
            'RESTORE_ACCESS_SEND_PASSWORD': '/ajax/api/accounts/password-reset/restore/'
        @ERRORS =
            'LOGIN':
                'CODES':
                    '3':        'Неверная пара логин - пароль'
                'FATAL':        'Fatal login error'
                'BAD_COOKIE':   'User cookie is bad'
            'RESTORE_ACCESS':
                'CODES':
                    '1':        'Запрос уже в очереди. Сообщение на почту отправлено повторно.'
                    '2':        'Пользователя с такими данными нету'
            'EMAIL':
                'CODES':
                    '1':        'Некоректная эл. почта'
                    '2':        'Указанная эл. почта уже используется'
            'PHONE':
                'CODES':
                    '1':        'Некоректный номер'
                    '2':        'Указанный номер уже используется'
                    '3':        'Некоректный код'
            'SMS_CODE':
                'CODES':
                    '1':        'Некоректный код'



    ###*
    # @public
    # @description Login user
    #
    # @param {object} user                     - User object
    # @param {string} user.name                - User name
    # @param {string} user.password            - User password
    # @param {function()} [successCallback]    - Success callback
    # @param {function()} [errorCallback]      - Error callback
    ###
    login: (user, successCallback, errorCallback) ->
        self = @
        request = @http.post @URL.LOGIN,
            'username': user.name
            'password': user.password

        request.success (response) ->
            if response.code is 0
                self._saveInStorage response.user
                _.isFunction(successCallback) && successCallback(
                    self._formattedResponseUserObject response.user)
            if response.code isnt 0
                _.isFunction(errorCallback) && errorCallback
                    'code':     response.code
                    'message':  self.ERRORS.LOGIN.CODES[response.code]

        request.error ->
            _.isFunction(errorCallback) && errorCallback
                'message': self.ERRORS.LOGIN.FATAL



    ###*
    # @public
    # @description Registration user
    #
    # @param {object} user                     - User object
    # @param {string} user.name                - User name
    # @param {string} user.surname             - User surname
    # @param {number} user.phoneNumber         - User phone number
    # @param {string} user.email               - User email address
    # @param {string} user.password            - User password
    # @param {string} user.passwordRepeat      - User password repeat
    # @param {function()} [successCallback]    - Success callback
    # @param {function()} [errorCallback]      - Error callback
    ###
    registration: (user, successCallback, errorCallback) ->
        request = @http.post @URL.REGISTRATION,
            'name':             user.name
            'surname':          user.surname
            'phone-number':     "+380" + user.phoneNumber #todo: get phone code from lang constants
            'email':            user.email
            'password':         user.password
            'password-repeat':  user.passwordRepeat

        request.success -> _.isFunction(successCallback) && successCallback()
        request.error -> _.isFunction(errorCallback) && errorCallback()



    ###*
    # @public
    # @description Cancel registration
    #
    # @param {function()} [successCallback]    - Success callback
    # @param {function()} [errorCallback]      - Error callback
    ###
    cancelRegistration: (successCallback, errorCallback) ->
        request = @http.post @URL.CANCEL_REGISTRATION, {}

        request.success -> _.isFunction(successCallback) && successCallback()
        request.error -> _.isFunction(errorCallback) && errorCallback()



    ###*
    # @public
    # @description Logout user
    #
    # @param {function()} [callback] - callback
    ###
    logout: (callback) ->
        self = @
        request = @http.post @URL.LOGOUT, {}

        request.success ->
            self._removeFromStorage()
            _.isFunction(callback) && callback()



    ###*
    # @public
    # @description Try login user using session cookies
    #
    # @param {function()} [successCallback]  - Success callback
    # @param {function()} [errorCallback]    - Error callback
    ###
    tryLogin: (successCallback, errorCallback) ->
        self = @;
        request = @http.get @URL.GET_USER_NAME

        request.success (response) ->
            self._saveInStorage(response.user)
            _.isFunction(successCallback) && successCallback(
                self._formattedResponseUserObject response.user)

        request.error ->
            self._removeFromStorage()
            _.isFunction(errorCallback) && errorCallback
                'message': self.ERRORS.LOGIN.BAD_COOKIE



    ###*
    # @public
    # @description Validate email address on server
    #
    # @param {string} email                  - Email address
    # @param {function()} [successCallback]  - Success callback
    # @param {function()} [errorCallback]    - Error callback
    ###
    validateEmail: (email, successCallback, errorCallback) ->
        self = @
        request = @http.post @URL.VALIDATE_EMAIL,
            'email': email

        request.success (response) ->
            if response.code is 0
                _.isFunction(successCallback) && successCallback()
            if response.code isnt 0
                _.isFunction(errorCallback) && errorCallback
                    'code':     response.code
                    'message':  self.ERRORS.EMAIL.CODES[response.code]

        request.error ->
            _.isFunction(errorCallback) && errorCallback()



    ###*
    # @public
    # @description Validate phone number on server
    #
    # @param {(string|number)} phone         - Phone number
    # @param {function()} [successCallback]  - Success callback
    # @param {function()} [errorCallback]    - Error callback
    ###
    validatePhone: (phone, successCallback, errorCallback) ->
        self = @
        request = @http.post @URL.VALIDATE_PHONE,
            'number': phone

        request.success (response) ->
            if response.code is 0
                _.isFunction(successCallback) && successCallback()
            if response.code isnt 0
                _.isFunction(errorCallback) && errorCallback
                    'code':     response.code
                    'message':  self.ERRORS.PHONE.CODES[response.code]

        request.error -> _.isFunction(errorCallback) && errorCallback()



    ###*
    # @public
    # @description Validate SMS code
    #
    # @param {(string|number)} code          - SMS code
    # @param {function()} [successCallback]  - Success callback
    # @param {function()} [errorCallback]    - Error callback
    ###
    validateSMSCode: (code, successCallback, errorCallback) ->
        self = @
        request = @http.post @URL.VALIDATE_SMS_CODE,
            'code': code

        request.success (response) ->
            if response.code is 0
                self._saveInStorage(response.user)
                _.isFunction(successCallback) && successCallback()
            if response.code isnt 0
                _.isFunction(errorCallback) && errorCallback
                    'code':         response.code
                    'attempts':     response.attempts
                    'max_attempts': response.max_attempts
                    'message':      self.ERRORS.SMS_CODE.CODES[response.code]

        request.error -> _.isFunction(errorCallback) && errorCallback()



    ###*
    # @public
    # @description Resend SMS code
    #
    # @param {function()} [successCallback]  - Success callback
    # @param {function()} [errorCallback]    - Error callback
    ###
    resendSMSCode: (successCallback, errorCallback) ->
        request = @http.post @URL.RESEND_SMS_CODE, {}

        request.success -> _.isFunction(successCallback) && successCallback()
        request.error -> _.isFunction(errorCallback) && errorCallback()



    ###*
    # @public
    # @description Restore access - send email
    #
    # @param {string} username               - User email or phone number
    # @param {function()} [successCallback]  - Success callback
    # @param {function()} [errorCallback]    - Error callback
    ###
    restoreAccessSendEmail: (username, successCallback, errorCallback) ->
        request = @http.post @URL.RESTORE_ACCESS_SEND_EMAIL,
            'username': username

        request.success (response) ->
            if response.code is 0
                _.isFunction(successCallback) && successCallback()
            if response.code isnt 0
                _.isFunction(errorCallback) && errorCallback
                    'code':     response.code
                    'message':  self.ERRORS.RESTORE_ACCESS.CODES[response.code]

        request.error -> _.isFunction(errorCallback) && errorCallback()



    ###*
    # @public
    # @description Restore access - send password
    #
    # @param {object} user                  - User object
    # @param {string} user.password         - User password
    # @param {string} user.passwordRepeat   - User password repeat
    # @param {string} token                 - Token
    # @param {function()} [successCallback] - Success callback
    # @param {function()} [errorCallback]   - Error callback
    ###
    restoreAccessSendPassword: (user, token, successCallback, errorCallback) ->
        request = @http.post @URL.RESTORE_ACCESS_SEND_PASSWORD,
            'token':            user.token,
            'password':         user.password,
            'password-repeat':  user.passwordRepeat

        request.success (response) ->
            if response.code is 0
                _.isFunction(successCallback) && successCallback()
            if response.code isnt 0
                _.isFunction(errorCallback) && errorCallback
                    'code':     response.code
                    'message':  ''

        request.error -> _.isFunction(errorCallback) && errorCallback()



    ###*
    # @public
    # @description Returns user object param value by param name from storage
    #
    # @param {string} param - Name of user param in storage (name, surname or fullName)
    #
    # @returns {string} - Returns user param value by param name
    ###
    getUserParam: (param) ->
        # todo: додати провірку по назві параметра
        if localStorage && localStorage.user
            (JSON.parse(localStorage.user))[param]
        else if sessionStorage && sessionStorage.user
            (JSON.parse(sessionStorage.user))[param]
        else null



    ###
    All private methods goes here
    ###

    ###*
    # @private
    # @description Setting user name to a local and session storage
    #
    # @param {object} user            - User object
    # @param {string} user.name       - User name
    # @param {string} user.surname    - User surname
    ###
    _saveInStorage: (user) ->
        if sessionStorage
            sessionStorage.user = JSON.stringify @_formattedResponseUserObject user
        if localStorage
            localStorage.user = JSON.stringify @_formattedResponseUserObject user



    ###*
    # @private
    # @description Remove user name from local and session stores
    ###
    _removeFromStorage: ->
        @cookieStore.remove 'sessionid'
        if localStorage and localStorage.user
            delete localStorage.user
        if sessionStorage and sessionStorage.user
            delete sessionStorage.user



    ###*
    # @private
    # @description Returns the formatted user object (name, surname and full name)
    #
    # @param {object} user            - User object
    # @param {string} user.name       - User name
    # @param {string} user.surname    - User surname
    #
    # @returns {object} Formatted user object (name, surname and fullName)
    ###
    _formattedResponseUserObject: (user) ->
        if _.isEmpty user
            false

        'name':     user.name      || ''
        'surname':  user.surname   || ''
        'fullName': user.name + ' ' + user.surname || ''




bAuthModule = angular.module '_modules.bAuth', ['ngCookies', 'underscore']
bAuthModule.factory 'BAuthService', ['$http', '$cookieStore',
    (http, cookieStore) -> new BAuthService(http, cookieStore)
]