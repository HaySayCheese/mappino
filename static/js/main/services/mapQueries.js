'use strict';

app.factory('mapQueries', function($http) {

    return {

        getMarkers: function(viewport, tid) {
            return $http.get('ajax/api/markers/?tid=' + tid + viewport)
        },

        getMarkersOfFilters: function(filters, viewport, tid) {
            return $http.get('ajax/api/markers/?tid=' + tid + viewport + filters)
        }

    }

});