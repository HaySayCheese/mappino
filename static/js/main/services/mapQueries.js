'use strict';

app.factory('mapQueries', function($http) {

    return {

        getMarkers: function(viewport) {
            return $http.get('ajax/api/markers/?tid=0' + viewport)
        }

    }

});