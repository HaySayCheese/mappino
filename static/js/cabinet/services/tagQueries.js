'use strict';

app.factory('tagQueries', function($http, $cookies) {

    return {

        // Запит на творення тега
        loadTags: function() {
            return $http({
                url: '/ajax/api/cabinet/dirtags/',
                method: "GET",
                headers: {
                    'X-CSRFToken': $cookies.csrftoken
                }
            });
        },


        // Запит на творення тега
        createTag: function(tag) {
            return $http({
                url: '/ajax/api/cabinet/dirtags/',
                method: "POST",
                headers: {
                    'X-CSRFToken': $cookies.csrftoken
                },
                data: {
                    title: tag.tagName,
                    color: tag.colors.indexOf(tag.selectedColor)
                }
            });
        },


        // Запит на видалення тега
        removeTag: function(tag) {
            return $http({
                url: 'ajax/api/accounts/login/',
                method: "POST",
                headers: {
                    'X-CSRFToken': $cookies.csrftoken
                },
                data: {
                    tagName: tag.name,
                    tagColor: tag.color
                }
            });
        },


        // Запит на перейменування тега
        editTag: function(tag) {
            return $http({
                url: 'ajax/api/accounts/login/',
                method: "POST",
                headers: {
                    'X-CSRFToken': $cookies.csrftoken
                },
                data: {
                    tagName: tag.name,
                    tagColor: tag.color
                }
            });
        }
    }
});