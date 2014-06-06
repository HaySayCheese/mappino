'use strict';

app.factory('Account', function(authorizationQueries, $location) {

    return {

        /**
         * Логін користувача
         *
         * @param {object}      user  Обєкт з іменем та паролем користувача
         * @param {function}    callback
         */
        login: function(user, callback) {
            authorizationQueries.loginUser(user).success(function(data) {
                _.isFunction(callback) && callback(data);
            });
        },


        /**
         * Реєстрація користувача
         *
         * @param {object}      user  Обєкт з іменем та паролем користувача
         * @param {function}    callback
         */
        register: function(user, callback) {
            authorizationQueries.registerUser(user).success(function(data) {
                _.isFunction(callback) && callback(data);
            });
        },


        /**
         * Повторна реєстрація користувача
         *
         * @param {function}    callback
         */
        repeatRegister: function(callback) {
            authorizationQueries.repeatRegistration().success(function(data) {
                _.isFunction(callback) && callback(data);
            });
        },


        /**
         * Відправка коду на перевірку
         *
         * @param {function}    callback
         */
        checkPhoneCode: function(callback) {
            authorizationQueries.validatePhoneCode().success(function(data) {
                _.isFunction(callback) && callback(data);
            });
        },


        /**
         * Повторна відправка коду на перевірку
         *
         * @param {function}    callback
         */
        repeatSendCode: function(callback) {
            authorizationQueries.repeatSendCode().success(function(data) {
                _.isFunction(callback) && callback(data);
            });
        },


        /**
         * Перевірка пошти
         *
         * @param {object}      email  Обєкт з поштою користувача
         * @param {function}    callback
         */
        checkEmail: function(email, callback) {
            authorizationQueries.validateEmail(email).success(function(data) {
                _.isFunction(callback) && callback(data);
            })
        },


        /**
         * Перевірка номера телефона
         *
         * @param {object}      phone  Обєкт з номером користувача
         * @param {function}    callback
         */
        checkPhone: function(phone, callback) {
            authorizationQueries.validatePhone(phone).success(function(data) {
                _.isFunction(callback) && callback(data);
            })
        },


        /**
         * Перевірка токена
         *
         * @param {function}    callback
         */
        checkToken: function(callback) {
            authorizationQueries.checkToken($location.search().token).success(function(data) {
                _.isFunction(callback) && callback(data);
            })
        },


        /**
         * Відновлення доступу: відправка пошти
         *
         * @param {object}      email  Обєкт з поштою користувача
         * @param {function}    callback
         */
        restoreAccessSendEmail: function(email, callback) {
            authorizationQueries.restoreAccessSendEmail(email).success(function(data) {
                _.isFunction(callback) && callback(data);
            })
        },


        /**
         * Відновлення доступу: відправка паролів
         *
         * @param {object}      passwords  Обєкт з паролями користувача
         * @param {function}    callback
         */
        restoreAccessSendPasswords: function(passwords, callback) {
            authorizationQueries.restoreAccessSendPasswords(passwords).success(function(data) {
                _.isFunction(callback) && callback(data);
            })
        },


        /**
         * Отримання імені користувача
         *
         * @param {function}    callback
         */
        getUserName: function(callback) {
            authorizationQueries.getUserName().success(function(data) {
                _.isFunction(callback) && callback(data);
            }).error(function() {
                //
            })
        },


        /**
         * Отримання імені користувача
         *
         * @param {function}    callback
         */
        logoutUser: function(callback) {
            authorizationQueries.logoutUser().success(function(data) {
                _.isFunction(callback) && callback(data);
            })
        }

    }
});