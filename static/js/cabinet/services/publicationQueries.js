'use strict';

app.factory('publicationQueries', function($http, $upload) {

    return {

        /**
         * Запит на загрузку оголошень
         *
         * @param {number} tid      Ідентифікатор типу оголошення
         * @param {number} hid      Ідентифікатор оголошення
         */
        loadPublication: function(tid, hid) {
            return $http({
                url: '/ajax/api/cabinet/publications/' + tid + ":" + hid + '/',
                method: "GET"
            });
        },


        /**
         * Запит на створення оголошення
         *
         * @param {object} publication Обєкт оголошення
         */
        createPublication: function(publication) {
            publication.tid = parseInt(publication.tid);

            return $http({
                url: '/ajax/api/cabinet/publications/',
                method: "POST",
                data: publication
            });
        },


        /**
         * Запит на публікацію оголошення
         *
         * @param {number} tid      Ідентифікатор типу оголошення
         * @param {number} hid      Ідентифікатор оголошення
         */
        publish: function(tid, hid) {
            return $http({
                url: '/ajax/api/cabinet/publications/' + tid + ":" + hid + '/publish/',
                method: "UPDATE"
            });
        },


        /**
         * Запит на перенесення оголошення в чорновики
         *
         * @param {number} tid      Ідентифікатор типу оголошення
         * @param {number} hid      Ідентифікатор оголошення
         */
        unpublish: function(tid, hid) {
            return $http({
                url: '/ajax/api/cabinet/publications/' + tid + ":" + hid + '/unpublish/',
                method: "UPDATE"
            });
        },


        /**
         * Запит на перевірку полів при доданні оголошення
         *
         * @param {number} tid      Ідентифікатор типу оголошення
         * @param {number} hid      Ідентифікатор оголошення
         * @param {object} data     Обєкт з назвою інпута та його значенням
         */
        checkInputs: function(tid, hid, data) {
            return $http({
                url: '/ajax/api/cabinet/publications/' + tid + ":" + hid + '/',
                method: "UPDATE",
                data: data
            });
        },


        /**
         * Запит на загрузку фоток на сервер
         *
         * @param {number} tid      Ідентифікатор типу оголошення
         * @param {number} hid      Ідентифікатор оголошення
         * @param {object} photos   Обєкт з фотками
         */
        uploadPhotos: function(tid, hid, photos) {
            return $upload.upload({
                url: '/ajax/api/cabinet/publications/' + tid + ':' + hid + '/upload-photo/',
                method: "POST",
                file: photos
            }).progress(function(evt) {
                console.log('percent: ' + parseInt(100.0 * evt.loaded / evt.total));
            }).success(function(data, status, headers, config) {
                console.log(data);
            });
        }

    }
});