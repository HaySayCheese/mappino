app.factory('Account', ['Queries', function(Queries) {
    'use strict';

    return {

        /**
         * Повторна реєстрація користувача
         *
         * @param {function}    callback
         */
        repeatRegister: function(callback) {
            Queries.Account.repeatRegistration().success(function(data) {
                console.log(data)
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
         * Відновлення доступу: відправка пошти
         *
         * @param {object}      email  Обєкт з поштою користувача
         * @param {function}    callback
         */
        restoreAccessSendEmail: function(email, callback) {
            Queries.Account.restoreAccessSendEmail(email).success(function(data) {
                _.isFunction(callback) && callback(data);
            });
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
            });
        }

    };
}]);