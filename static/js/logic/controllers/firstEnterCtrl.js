'use strict';

app.controller('FirstEnterCtrl', function($scope, $location) {
    $scope.firstEnterState = "selectCity";
    $("#property-type-select").selectpicker({
        style: 'btn-hg btn-info',
        menuStyle: 'dropdown-inverse'
    });

    var firstEnterCityInput = document.getElementById('first-enter-city-input');
    angular.element(firstEnterCityInput).focus();

    var autocompleteOptions = {
        types: ['(cities)'],
        componentRestrictions: {
            country: "ua"
        }
    };

    var autocomplete = new google.maps.places.Autocomplete(firstEnterCityInput, autocompleteOptions);

    google.maps.event.addListener(autocomplete, 'place_changed', function() {
        var place = autocomplete.getPlace();
        if (!place.geometry) {
            return;
        }

        $scope.filters.city = firstEnterCityInput.value;
        if(!$scope.$$phase)
            $scope.$apply();

        setTimeout(function() {
            $scope.firstEnterState = "selectType";
            if(!$scope.$$phase)
                $scope.$apply();
        }, 500);
    });
});