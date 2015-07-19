'use strict';

app.factory('Settings', function($rootScope, $window, $cookies, Queries) {

    var user = [];

    return {

        /**
        * Загрузка даних користувача
        *
        * @param {function} callback
        */
        load: function(callback) {
            Queries.Settings.load(function(data) {
                account = data;

                _.isFunction(callback) && callback(account);
            })
        },


        /**
         * Валідація полів на сервері
         *
         * @param {object}   input Обєкт з полем і значенням
         * @param {function} callback
         */
        checkInputs: function(input, callback) {
            var inputValue  = input.v;

            Queries.Settings.check(input, function(data) {
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
                if (data.data.code === 100) {
                    channel.info("Во время загрузки возникла ошибка. Повторите попытку с другим изображением");
                    _.isFunction(callback) && callback(account);
                    return;
                }

                account.account.avatar_url = data.data.url + "?" + new Date().getTime();

                _.isFunction(callback) && callback(account);
            });
        },


        /**
         * Логаут
         *
         * @param {function} callback
         */
        logoutUser: function(callback) {
            Queries.Settings.logoutUser(function(data) {
                delete sessionStorage.userName;
                delete $cookies.sessionid;

                $window.location.reload();

                _.isFunction(callback) && callback(data);
            });
        }
    }
});