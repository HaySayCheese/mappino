'use strict';

app.factory('briefQueries', function($http) {

    return {

        /**
         * @param {string, number} category Категорія ('all', 'published', 'unpublished', ...)
         */
        loadBriefs: function(category) {
            return $http({
                url: '/ajax/api/cabinet/publications/briefs/' + category + '/',
                method: "GET"
            });
        },


        /**
         * @param {string} value Строка пошука
         */
        searchInBriefs: function(value) {
            return $http({
                url: '/ajax/api/cabinet/search?' + value + '/',
                method: "GET"
            });
        }

    }
});