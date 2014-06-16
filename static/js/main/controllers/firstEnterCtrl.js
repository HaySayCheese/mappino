'use strict';

app.controller('FirstEnterCtrl', function($scope, $location, $rootScope) {

    $scope.firstEnter = {
        city: ""
    };

    var firstEnterModal = angular.element(".first-enter-modal");
    firstEnterModal.modal();


    $scope.initializeAutocomplete = function() {
        var input = document.getElementById('first-enter-autocomplete'),
            autocomplete,
            autocompleteOptions = {
                types:  ['(cities)'],
                componentRestrictions: {
                    country: 'ua'
                }
            };

        autocomplete = new google.maps.places.Autocomplete(input, autocompleteOptions);
    }

});