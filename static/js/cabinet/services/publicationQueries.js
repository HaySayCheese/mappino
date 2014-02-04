'use strict';

app.factory('publicationQueries', function($http) {

    return {

        /**
         * Запит на загрузку оголошень
         *
         * @param {string} category Категорія ('all', 'published', 'unpublished', ...)
         * @param {number} tid      Ідентифікатор типу оголошення
         * @param {number} hid      Ідентифікатор оголошення
         */
        loadPublication: function(category, tid, hid) {
            return $http({
                url: '/ajax/api/cabinet/publications/' + category + '/' + tid + ":" + hid + '/',
                method: "GET"
            });
        },


        /**
         * Запит на створення оголошення
         *
         * @param {Object} publication Обєкт оголошення
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
         * Запит на перевірку полів при доданні оголошення
         *
         * @param {string} category Категорія ('all', 'published', 'unpublished', ...)
         * @param {number} tid      Ідентифікатор типу оголошення
         * @param {number} hid      Ідентифікатор оголошення
         * @param {object} data     Обєкт з назвою інпута та його значенням
         */
        checkInputs: function(category, tid, hid, data) {
            return $http({
                url: '/ajax/api/cabinet/publications/' + category + '/' + tid + ":" + hid + '/',
                method: "POST",
                data: data
            });
        }

    }
});