'use strict';

app.factory('Settings', function($rootScope, Queries) {

    return {
        /**
        * Загрузка даних юзера
        *
        * @param {function} callback
        */
        load: function(callback) {
            Queries.Settings.load(function(data) {
                _.isFunction(callback) && callback(data);
            })
        },

        /**
         * Валідація полів на сервері
         *
         * @param {object}   data Обєкт з полем і значенням
         * @param {function} callback
         */
        checkInputs: function(data, callback) {
            var inputValue  = data.v;

            Queries.Settings.check(data, function(data) {
                _.isFunction(callback) && callback(data.value ? data.value : inputValue, data.code);
            });
        },

        /**
         * Загрузка фотки юзера
         *
         * @param {object}   photo
         * @param {function} callback
         */
        uploadUserPhoto: function(photo, callback) {
            Queries.Settings.uploadUserPhoto(photo, function(data) {
                _.isFunction(callback) && callback(data);
            });
        }
    }
});