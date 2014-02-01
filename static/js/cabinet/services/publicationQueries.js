'use strict';

app.factory('publicationQueries', function($http, $cookies) {

    return {

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