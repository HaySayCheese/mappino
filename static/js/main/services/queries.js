/**
 * Файл з описом усіх http запитів
 * Змінні путів знаходяться в файлі "/services/http_const.js"
 **/



app.factory('Queries', ['$http','HTTP_URL', function($http, HTTP_URL) {
    'use strict';

    return {
        Map: {
            getMarkers: function(filters) {
                return $http.get(HTTP_URL.MAP.GET_MARKERS.fmt(filters));
            }
        }
    };
}]);