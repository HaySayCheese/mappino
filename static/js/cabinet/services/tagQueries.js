'use strict';

app.factory('tagQueries', function($http) {

    return {

        /**
         * Запит на загрузку тегів
         */
        loadTags: function() {
            return $http({
                url: '/ajax/api/cabinet/dirtags/',
                method: "GET"
            });
        },


        /**
         * Запит на створення тега
         *
         * @param {object} tag Обєкт тега
         */
        createTag: function(tag) {
            return $http({
                url: '/ajax/api/cabinet/dirtags/',
                method: "POST",
                data: {
                    title: tag.title,
                    color_id: tag.colors.indexOf(tag.selectedColor)
                }
            });
        },


        /**
         * Запит на видалення тега
         *
         * @param {number} id Ідентифікатор тега
         */
        removeTag: function(id) {
            return $http({
                url: '/ajax/api/cabinet/dirtags/' + id + "/",
                method: "DELETE"
            });
        },


        /**
         * Запит на перейменування тега
         *
         * @param {object} tag Обєкт тега
         */
        editTag: function(tag) {
            return $http({
                url: '/ajax/api/cabinet/dirtags/' + tag.id + "/",
                method: "PUT",
                data: {
                    color_id: tag.color_id,
                    title: tag.title
                }
            });
        }
    }
});