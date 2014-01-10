'use strict';

app.controller('FirstEnterCtrl', function($scope, $rootScope, $location, $timeout) {
    $scope.firstEnterPart = "city";

    $timeout(function() {

        var cityInput = document.getElementById('fe-city-input'),
            propertyTypeSelect,
            autocompleteOptions = {
                types: ['(cities)'],
                componentRestrictions: {
                    country: "ua"
                }
            },
            autocomplete = new google.maps.places.Autocomplete(cityInput, autocompleteOptions);

        // Ставим фокус на поле пошуку
        angular.element(cityInput).focus();


        // Ініціалізація дропдауна
        $scope.$watch("firstEnterPart", function(newValue, oldValue) {
            if (newValue == "type") {
                propertyTypeSelect = $("#fe-property-type-select");
                propertyTypeSelect.selectpicker({
                    style: 'btn-primary btn-lg'
                });

                propertyTypeSelect.change(function() {
                    // Перенаправляємо його на сторінку пошуку
                    $location.path("/search");

                    $scope.filters.propertyType   = propertyTypeSelect.find("option:selected").val();
                    $scope.filters.propertyTypeUa = propertyTypeSelect.find("option:selected").text();

                    // Міняємо дані про те що юзер відвідав сайт
                    $rootScope.visited = true;

                    if(!$scope.$$phase)
                        $scope.$apply();
                });
            }
        });


        // Евент вибору міста в автокомпліті
        google.maps.event.addListener(autocomplete, 'place_changed', function() {
            var place = autocomplete.getPlace();
            if (!place.geometry) {
                return;
            }

            $scope.filters.city = cityInput.value;

            $timeout(function() {

                $scope.firstEnterPart = "type";

                if(!$scope.$$phase)
                    $scope.$apply();

            }, 1000)

        });

    }, 100);

//
//    // Евент вибору елемента в дропдауні

//
//

});