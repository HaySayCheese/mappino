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
            'LOGOUT':                       '/ajax/api/accounts/logout/'
            'CANCEL_REGISTRATION':          '/ajax/api/accounts/registration/cancel/'
            'RESEND_SMS_CODE':              '/ajax/api/accounts/registration/resend-sms/'
            'VALIDATE_SMS_CODE':            '/ajax/api/accounts/registration/'
            'RESTORE_ACCESS_SEND_EMAIL':    '/ajax/api/accounts/password-reset/'
            'RESTORE_ACCESS_SEND_PASSWORD': '/ajax/api/accounts/password-reset/restore/'
        @ERRORS =

            'RESTORE_ACCESS':
                'CODES':
                    '1':        'Запрос уже в очереди. Сообщение на почту отправлено повторно.'
                    '2':        'Пользователя с такими данными нету'
            'SMS_CODE':
                'CODES':
                    '1':        'Некоректный код'



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