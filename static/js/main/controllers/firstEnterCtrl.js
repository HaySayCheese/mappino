'use strict';

app.controller('FirstEnterCtrl', function($scope, $location, $timeout, $rootScope) {

    $rootScope.pageTitle = "Добро пожаловать на Mappino";
    $scope.firstEnter = {
        city: $location.search().city || "",
        latLng: ""
    };

    $scope.$watch(function() {
        return sessionStorage.userName;
    }, function(newValue) {
        $scope.userIsLogin = !_.isUndefined(newValue);
    });

    var input = document.getElementById('first-enter-autocomplete');

    var firstEnterModal = angular.element(".first-enter-modal");
    firstEnterModal.modal();


    ga('send', 'pageview', {
        'page': '#!/first-enter',
        'title': $rootScope.pageTitle
    });


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
                $rootScope.$emit('first-enter-change', [place.geometry.location, 15, input.value]);
            } else {
                $rootScope.$emit('first-enter-change', [place.geometry.location, 15, input.value]);
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
    };



    function firstEnterDone() {
        $location.path("/search");
    }

});