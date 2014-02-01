'use strict';

app.factory('briefQueries', function($http, $cookies) {

    return {

        // Загрузка всіх брифів
        loadBriefs: function(category) {
            return $http({
                url: '/ajax/api/cabinet/publications/briefs/' + category,
                method: "GET",
                headers: {
                    'X-CSRFToken': $cookies.csrftoken
                }
            });
        }

    }
});