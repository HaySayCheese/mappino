'use strict';

app.factory('Account', function(Queries, $location) {

    return {

        /**
         * Логін користувача
         *
         * @param {object}      user  Обєкт з іменем та паролем користувача
         * @param {function}    callback
         */
        login: function(user, callback) {
            Queries.Account.loginUser(user).success(function(data) {
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
            Queries.Account.registerUser(user).success(function(data) {
                _.isFunction(callback) && callback(data);
            });
        },


        /**
         * Повторна реєстрація користувача
         *
         * @param {function}    callback
         */
        repeatRegister: function(callback) {
            Queries.Account.repeatRegistration().success(function(data) {
                _.isFunction(callback) && callback(data);
            });
        },


        /**
         * Відправка коду на перевірку
         *
         * @param {object}      code  Обєкт з кодом
         * @param {function}    callback
         */
        checkPhoneCode: function(code, callback) {
            Queries.Account.validatePhoneCode(code).success(function(data) {
                _.isFunction(callback) && callback(data);
            });
        },


        /**
         * Повторна відправка коду на перевірку
         *
         * @param {function}    callback
         */
        repeatSendCode: function(callback) {
            Queries.Account.repeatSendCode().success(function(data) {
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
            Queries.Account.validateEmail(email).success(function(data) {
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
            Queries.Account.validatePhone(phone).success(function(data) {
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
            Queries.Account.restoreAccessSendEmail(email).success(function(data) {
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
            Queries.Account.restoreAccessSendPasswords(passwords).success(function(data) {
                _.isFunction(callback) && callback(data);
            })
        },


        /**
         * Отримання імені користувача
         *
         * @param {function}    callback
         */
        getUserName: function(callback) {
            Queries.Account.getUserName().then(function(data) {
                _.isFunction(callback) && callback(data);
            });
        },


        /**
         * Отримання імені користувача
         *
         * @param {function}    callback
         */
        logoutUser: function(callback) {
            Queries.Account.logoutUser().success(function(data) {
                _.isFunction(callback) && callback(data);
            })
        }

    }
});