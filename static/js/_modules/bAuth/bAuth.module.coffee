###*
# @module bAuth
# @description todo: add desc
# @version 0.6.1
# @license todo: add license
#
# @requires ngCookies
# @requires module:underscore
###
angular.module '_modules.bAuth', ['ngCookies', 'underscore']
    .factory 'BAuthService', ['$http', '$cookieStore', '_', ($http, $cookieStore, _) ->

        URL =
            'LOGIN':                        '/ajax/api/accounts/login/'
            'LOGOUT':                       '/ajax/api/accounts/logout/'
            'REGISTRATION':                 '/ajax/api/accounts/registration/'
            'REPEAT_REGISTRATION':          '/ajax/api/accounts/registration/cancel/'
            'REPEAT_SEND_CODE':             '/ajax/api/accounts/registration/resend-sms/'
            'VALIDATE_EMAIL':               '/ajax/api/accounts/validate-email/'
            'VALIDATE_PHONE_NUMBER':        '/ajax/api/accounts/validate-phone-number/'
            'VALIDATE_PHONE_CODE':          '/ajax/api/accounts/registration/'
            'GET_USER_NAME':                '/ajax/api/accounts/on-login-info/'
            'RESTORE_ACCESS_SEND_EMAIL':    '/ajax/api/accounts/password-reset/'
            'RESTORE_ACCESS_SEND_PASSWORD': '/ajax/api/accounts/password-reset/restore/'

        ERRORS =
            'LOGIN':
                'CODES':
                    '3':        'Неверная пара логин - пароль'
                'FATAL':        'Fatal login error'
                'BAD_COOKIE':   'User cookie is bad'
            'EMAIL':
                'CODES':
                    '1':        'Некоректная эл. почта'
                    '2':        'Указанная эл. почта уже используется'


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
            self = this

            $http.post URL.LOGIN,
                'username': user.name
                'password': user.password
            .success (response) ->
                if response.code is 0
                    self._saveInStorage response.user
                    _.isFunction(successCallback) && successCallback user
                if response.code isnt 0
                    _.isFunction(errorCallback) && errorCallback
                        'code':     response.code
                        'message':  ERRORS.LOGIN.CODES[response.code]
            .error () ->
                _.isFunction(errorCallback) && errorCallback
                    'message': ERRORS.LOGIN.FATAL



        ###*
        # @public
        # @description Register user
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
        register: (user, successCallback, errorCallback) ->
            $http.post URL.REGISTRATION,
                'name':             user.name
                'surname':          user.surname
                'phone-number':     "+380" + user.phoneNumber #todo: get phone code from lang constants
                'email':            user.email
                'password':         user.password
                'password-repeat':  user.passwordRepeat
            .success () ->
                _.isFunction(successCallback) && successCallback()
            .error () ->
                _.isFunction(errorCallback) && errorCallback()



        ###*
        # @public
        # @description Logout user
        #
        # @param {function()} [callback] - callback
        ###
        logout: (callback) ->
            self = this

            $http.post URL.LOGOUT
            .then () ->
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
            self = this;

            $http.get URL.GET_USER_NAME
            .success (response) ->
                self._saveInStorage(response.user)
                _.isFunction(successCallback) && successCallback(
                    self._formattedResponseUserObject response.user)
            .error () ->
                self._removeFromStorage
                _.isFunction(errorCallback) && errorCallback
                    'message': ERRORS.LOGIN.BAD_COOKIE



        ###*
        # @public
        # @description Validate email address on server
        #
        # @param {string} email                  - Email address
        # @param {function()} [successCallback]  - Success callback
        # @param {function()} [errorCallback]    - Error callback
        ###
        validateEmail: (email, successCallback, errorCallback) ->
            $http.post URL.VALIDATE_EMAIL,
                'email': email
            .success (response) ->
                if response.code is 0
                    _.isFunction(successCallback) && successCallback()
                if response.code isnt 0
                    _.isFunction(errorCallback) && errorCallback
                        'code':     response.code
                        'message':  ERRORS.EMAIL.CODES[response.code]
            .error () ->
                _.isFunction(errorCallback) && errorCallback()



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
                sessionStorage.user = JSON.stringify this._formattedResponseUserObject user
            if localStorage
                localStorage.user = JSON.stringify this._formattedResponseUserObject user



        ###*
        # @private
        # @description Remove user name from local and session stores
        ###
        _removeFromStorage: () ->
            $cookieStore.remove 'sessionid'
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

            'name':     user.name      || '',
            'surname':  user.surname   || '',
            'fullName': user.name + ' ' + user.surname || ''
    ]