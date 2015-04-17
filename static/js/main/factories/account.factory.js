app.factory('Account', ['Queries', function(Queries) {
    'use strict';

    return {
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