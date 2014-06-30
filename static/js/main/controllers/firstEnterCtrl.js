'use strict';

app.controller('FirstEnterCtrl', function($scope, $location, $timeout, $rootScope) {

    $rootScope.pageTitle = "Добро пожаловать на Mappino";
    $scope.firstEnter = {
        city: $location.search().city || "",
        latLng: ""
    };

    var input = document.getElementById('first-enter-autocomplete');

    var firstEnterModal = angular.element(".first-enter-modal");
    firstEnterModal.modal();


    $scope.initializeAutocomplete = function() {
        var autocomplete,
            autocompleteOptions = {
                types:  ['(cities)'],
                componentRestrictions: {
                    country: 'ua'
                }
            };

        autocomplete = new google.maps.places.Autocomplete(input, autocompleteOptions);


        google.maps.event.addListener(autocomplete, 'place_changed', function() {
            var place = autocomplete.getPlace();

            if (!place.geometry)
                return;

            // If the place has a geometry, then present it on a map.
            if (place.geometry.viewport) {
                $rootScope.$emit('first-enter-change', [place.geometry.location, 17]);
            } else {
                $rootScope.$emit('first-enter-change', [place.geometry.location, 17]);
            }

            firstEnterDone();

            if(!$scope.$$phase)
                $scope.$apply();
        });
    };


    $scope.setCityFromExample = function(city) {
        $scope.firstEnter.city = city;
        $timeout(function() {
            angular.element(input).focus().trigger("change");
        }, 100);


        returnMapPositionFromAddress(city);
    };


    /**
     * Вертає центр карти на місто введене в автокомпліті
     */
    function returnMapPositionFromAddress(address) {

        var geocoder = new google.maps.Geocoder();

        geocoder.geocode({ 'address': address }, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                if (results[0].geometry.viewport)
                    $scope.firstEnter.latLng = results[0].geometry.location;
                else
                    $scope.firstEnter.latLng = results[0].geometry.location;
            }

            $rootScope.$emit('first-enter-change', [$scope.firstEnter.latLng, 17]);
        });
    }

    function firstEnterDone() {
        $location.path("/search");
    }

});