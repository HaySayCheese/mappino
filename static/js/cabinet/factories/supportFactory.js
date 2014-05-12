'use strict';

app.factory('Support', function($rootScope, Queries) {

    return {

        /**
         * Загрузка всіх тікетів
         *
         * @param {function} callback
         */
        loadTickets: function(callback) {
            Queries.Support.loadTickets(function(data) {
                _.isFunction(callback) && callback(data);
            })
        },

        /**
         * Загрузка даних тікета
         *
         * @param {function} callback
         */
        loadTicketData: function(data, callback) {
            Queries.Support.loadTicketData(data.ticketId, function(data) {
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