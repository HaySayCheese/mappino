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
                    title: tag.title,
                    color_id: tag.colors.indexOf(tag.selectedColor)
                }
            });
        },


        // Запит на видалення тега
        removeTag: function(id) {
            return $http({
                url: '/ajax/api/cabinet/dirtags/' + id + "/",
                method: "DELETE",
                headers: {
                    'X-CSRFToken': $cookies.csrftoken
                }
            });
        },


        // Запит на перейменування тега
        editTag: function(tag) {
            return $http({
                url: '/ajax/api/cabinet/dirtags/' + tag.id + "/",
                method: "PUT",
                headers: {
                    'X-CSRFToken': $cookies.csrftoken
                },
                data: tag
            });
        },


        // Запит на створення оголошення
        createPublication: function(publication) {
            publication.tid = parseInt(publication.tid);

            return $http({
                url: '/ajax/api/cabinet/publications/',
                method: "POST",
                headers: {
                    'X-CSRFToken': $cookies.csrftoken
                },
                data: publication
            });
        }
    }
});