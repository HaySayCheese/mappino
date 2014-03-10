'use strict';

app.factory('mapQueries', function($http) {

    return {
        getMarkers: function(tid, filters, viewport) {
            return $http.get('ajax/api/markers/?tid=' + tid + viewport + filters)
        }

    }

});