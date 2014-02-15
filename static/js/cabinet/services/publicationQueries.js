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
         * Запит на отримання кількості оголошень
         */
        getPublicationsCount: function() {
            return $http({
                url: '/ajax/api/cabinet/publications/counts/',
                method: "GET"
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
                url: '/ajax/api/cabinet/publications/' + tid + ':' + hid + '/photos/',
                method: "POST",
                file: photos
            });
        },


        /**
         * Запит на видалення фотографії
         *
         * @param {number} tid      Ідентифікатор типу оголошення
         * @param {number} hid      Ідентифікатор оголошення
         * @param {number} pid      Ідентифікатор фотографії
         */
        removePhoto: function(tid, hid, pid) {
            return $http({
                url: '/ajax/api/cabinet/publications/' + tid + ':' + hid + '/photos/' + pid + '/',
                method: "DELETE"
            });
        }

    }
});