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
                $rootScope.$emit('first-enter-change', [place.geometry.location, 17, input.value]);
            } else {
                $rootScope.$emit('first-enter-change', [place.geometry.location, 17, input.value]);
            }

            firstEnterDone();

            if(!$scope.$$phase)
                $scope.$apply();
        });


        angular.element(input).focusin(function () {
            angular.element(document).keypress(function (e) {
                var autocompleteContainer = angular.element(".pac-container"),
                    autocompleteFirstItem = autocompleteContainer.find(".pac-item:first"),
                    geocoder = new google.maps.Geocoder();

                if (e.which == 13)
                    geocoder.geocode({ "address": autocompleteFirstItem.text() }, function(results, status) {
                        if (status == google.maps.GeocoderStatus.OK) {

                            autocompleteFirstItem.addClass("pac-selected");
                            autocompleteContainer.hide();

                            angular.element(input)
                                .val(autocompleteFirstItem.find(".pac-item-query").text()
                                    + ", " +
                                    autocompleteFirstItem.find("span:nth-child(3)").text());

                            if (results[0].geometry.viewport)
                                $rootScope.$emit('first-enter-change', [results[0].geometry.location, 17, input.value]);
                            else {
                                $rootScope.$emit('first-enter-change', [results[0].geometry.location, 17, input.value]);
                            }

                            $scope.firstEnter.city = input.value;
                            firstEnterDone();
                        }
                    });
                else
                    autocompleteContainer.show();
            });
        });
    };


    $scope.setCityFromExample = function(city) {
        $scope.firstEnter.city = city;
        $timeout(function() {
            angular.element(input).focus().trigger("change");
        }, 100);
    };



    function firstEnterDone() {
        input.blur();
        $location.path("/search");
    }

});