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
         * @param {number}   ticketId
         * @param {function} callback
         */
        loadTicketData: function(ticketId, callback) {
            Queries.Support.loadTicketData(ticketId, function(data) {
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
         * @param {number}   ticketId
         * @param {object}   message
         * @param {function} callback
         */
        sendMessage: function(ticketId, message, callback) {
            Queries.Support.sendMessage(ticketId, message, function(data) {
                _.isFunction(callback) && callback(data);
            });
        }
    }
});