'use strict';

app.factory('Support', function($rootScope, Queries) {

    return {
        /**
         * Загрузка даних тікета
         *
         * @param {function} callback
         */
        load: function(callback) {
            Queries.Support.loadTicketData($rootScope.ticketId, function(data) {
                _.isFunction(callback) && callback(data);
            })
        },

        /**
         * Створення тікета
         *
         * @param {object}   data Обєкт з даними тікета
         * @param {function} callback
         */
        createTicket: function(data, callback) {
            Queries.Support.createTicket(data, function(data) {
                _.isFunction(callback) && callback(data);
            });
        },

        /**
         * Відправка повідомлення
         *
         * @param {object}   data Обєкт з даними тікета
         * @param {function} callback
         */
        sendMessage: function(data, callback) {
            Queries.Support.sendMessage(data, function(data) {
                _.isFunction(callback) && callback(data);
            });
        }
    }
});