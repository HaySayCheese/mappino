'use strict';

app.factory('mapQueries', function($http) {

    return {

        getMarkers: function(viewport, tid) {
            return $http.get('ajax/api/markers/?tid=' + tid + viewport)
        }

    }

});