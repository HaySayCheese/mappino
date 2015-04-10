/**
 * @module Auth
 * @description
 *  // todo: add module description
 * @version 0.5.0
 * @license // todo: add license
 **/
angular.module('mappino.services.auth', ['ngCookies']).
    factory('BAuthService', ['$http', '$cookieStore', function($http, $cookieStore) {
        "use strict";

        var URL = {
            'LOGIN':                        '/ajax/api/accounts/login/',
            'LOGOUT':                       '/ajax/api/accounts/logout/',
            'REGISTRATION':                 '/ajax/api/accounts/registration/',
            'REPEAT_REGISTRATION':          '/ajax/api/accounts/registration/cancel/',
            'REPEAT_SEND_CODE':             '/ajax/api/accounts/registration/resend-sms/',
            'VALIDATE_EMAIL':               '/ajax/api/accounts/validate-email/',
            'VALIDATE_PHONE_NUMBER':        '/ajax/api/accounts/validate-phone-number/',
            'VALIDATE_PHONE_CODE':          '/ajax/api/accounts/registration/',
            'GET_USER_NAME':                '/ajax/api/accounts/on-login-info/',
            'RESTORE_ACCESS_SEND_EMAIL':    '/ajax/api/accounts/password-reset/',
            'RESTORE_ACCESS_SEND_PASSWORD': '/ajax/api/accounts/password-reset/restore/'
        };

        var ERRORS = {
            'LOGIN': {
                'CODES': {
                    '3':        'Неверная пара логин - пароль'
                },
                'FATAL':        'Fatal login error',
                'UNDEFINED':    'Undefined login error code',
                'BAD_COOKIE':   'User cookie is bad'
            }
        };


        return {

            /**
             * @public
             * @description
             *  Login user
             *
             *  Call successCallback when user is logged and
             *  return formatted user object (name, surname and fullName)
             *  by calling '_formattedUserObject(<response_user>)'
             *
             *  Call errorCallback when response code !== 0 and
             *  return message from:
             *  - 'ERRORS.LOGIN.CODES[<response_error_code>]' or
             *  - 'ERRORS.LOGIN[<'FATAL'||'UNDEFINED'||'BAD_COOKIE'>]'
             *
             * @param {object} user                     - User object
             * @param {string} user.name                - User name
             * @param {string} user.password            - User password
             * @param {function()} [successCallback]    - Success callback
             * @param {function()} [errorCallback]      - Error callback
             **/
            login: function(user, successCallback, errorCallback) {
                var that = this;

                $http.post(URL.LOGIN, {
                        username: user.name,
                        password: user.password
                    }).
                    success(function(response) {
                        if (response.code === 0) {
                            that._saveInStorage(response.user);
                            _.isFunction(successCallback) && successCallback(that._formattedUserObject(response.user));
                        }

                        if (response.code !== 0) {
                            _.isFunction(errorCallback) && errorCallback({
                                'code':     response.code,
                                'message':  ERRORS.LOGIN.CODES[response.code] || ERRORS.LOGIN.UNDEFINED
                            });
                        }
                    }).
                    error(function() {
                        _.isFunction(errorCallback) && errorCallback({
                            'message': ERRORS.LOGIN.FATAL
                        });
                    });
            },



            /**
             * @public
             * @description
             *  Register user
             *
             * @param {object} user                     - User object
             * @param {string} user.name                - User name
             * @param {string} user.surname             - User surname
             * @param {number} user.phoneNumber         - User phone number
             * @param {string} user.email               - User email address
             * @param {string} user.password            - User password
             * @param {string} user.passwordRepeat      - User password repeat
             * @param {function()} [successCallback]    - Success callback
             * @param {function()} [errorCallback]      - Error callback
             **/
            register: function(user, successCallback, errorCallback) {
                $http.post(URL.REGISTRATION, {
                        'name':             user.name,
                        'surname':          user.surname,
                        'phone-number':     "+380" + user.phoneNumber,
                        'email':            user.email,
                        'password':         user.password,
                        'password-repeat':  user.passwordRepeat
                    }).
                    success(function() {
                        _.isFunction(successCallback) && successCallback();
                    }).
                    error(function() {
                        _.isFunction(errorCallback) && errorCallback();
                    });
            },



            /**
             * @public
             * @description
             *  Logout user
             *
             * @param {function()} [successCallback]    - Success callback
             * @param {function()} [errorCallback]      - Error callback
             **/
            logout: function(successCallback, errorCallback) {
                var that = this;

                $http.post(URL.LOGOUT).
                    success(function() {
                        that._removeFromStorage();
                        _.isFunction(successCallback) && successCallback();
                    }).
                    error(function() {
                        that._removeFromStorage();
                        _.isFunction(errorCallback) && errorCallback();
                    });
            },



            /**
             * @public
             * @description
             *  Try login user using session cookies
             *
             * @param {function()} [successCallback]  - Success callback
             * @param {function()} [errorCallback]    - Error callback
             **/
            tryLogin: function(successCallback, errorCallback) {
                var that = this;

                $http.get(URL.GET_USER_NAME).
                    success(function(response) {
                        that._saveInStorage(response.user);
                        _.isFunction(successCallback) && successCallback(that._formattedUserObject(response.user));
                    }).
                    error(function() {
                        that._removeFromStorage();
                        _.isFunction(errorCallback) && errorCallback({
                            'message': ERRORS.LOGIN.BAD_COOKIE
                        });
                    });
            },



            /**
             * @public
             * @description
             *  Returns user name from storage
             *
             *  @returns {string} - User name
             **/
            getUserName: function() {
                return localStorage.userName || sessionStorage.userName || null;
            },



            /***********************************
             * All private methods starts here *
             ***********************************/

            /**
             * @private
             * @description
             *  Setting user name to a local and session storage
             *
             * @param {object} user            - User object
             * @param {string} user.name       - User name
             * @param {string} user.surname    - User surname
             **/
            _saveInStorage: function(user) {
                if (sessionStorage) {
                    sessionStorage.userName = user.name + " " + user.surname;
                }
                if (localStorage) {
                    localStorage.userName = user.name + " " + user.surname;
                }
            },



            /**
             * @private
             * @description
             *  Remove user name from local and session stores
             **/
            _removeFromStorage: function() {
                if (sessionStorage.userName) {
                    delete sessionStorage.userName;
                }
                if (localStorage.userName) {
                    delete localStorage.userName;
                }
                $cookieStore.remove('sessionid');
            },



            /**
             * @private
             * @description
             *  Returns the formatted user object (name, surname and full name)
             *
             * @param {object} user            - User object
             * @param {string} user.name       - User name
             * @param {string} user.surname    - User surname
             *
             * @returns {object} Formatted user object (name, surname and fullName)
             **/
            _formattedUserObject: function(user) {
                if (_.isEmpty(user)) {
                    return false;
                }

                return {
                    'name':     user.name      || '',
                    'surname':  user.surname   || '',
                    'fullName': user.name + ' ' + user.surname || ''
                };
            }
        };
    }]
);