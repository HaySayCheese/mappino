'use strict';

app.factory('Settings', function($rootScope, Queries) {

    return {


        /**
        * Загрузка даних користувача
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
         * Загрузка фотографії користувача
         *
         * @param {object}   photo  Обєкт з фотографією
         * @param {function} callback
         */
        uploadUserPhoto: function(photo, callback) {
            Queries.Settings.uploadUserPhoto(photo, function(data) {
                _.isFunction(callback) && callback(data);
            });
        }
    }
});