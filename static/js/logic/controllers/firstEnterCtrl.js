'use strict';

app.controller('FirstEnterCtrl', function($scope, $location) {
    $scope.firstEnterState = "selectCity";

    var propertyTypeSelect = $("#first-enter-search-property-type-select");
    propertyTypeSelect.selectpicker({
        style: 'btn-hg btn-info',
        menuStyle: 'dropdown-inverse'
    });

    // Евент вибору елемента в дропдауні
    propertyTypeSelect.change(function() {
        $scope.filters.propertyType   = propertyTypeSelect.find("option:selected").val();
        $scope.filters.propertyTypeUa = propertyTypeSelect.find("option:selected").text();

        // Міняємо дані про те що юзер відвідав сайт
        localStorage.visited = "true";
        $scope.visited = true;

        // Перенаправляємо його на сторінку пошуку
        $location.path("/search");
        if(!$scope.$$phase)
            $scope.$apply();
    });


    // Ставим фокус на поле пошуку
    var firstEnterCityInput = document.getElementById('first-enter-search-city-input');
    angular.element(firstEnterCityInput).focus();

    var autocompleteOptions = {
        types: ['(cities)'],
        componentRestrictions: {
            country: "ua"
        }
    };

    // Ініціалізуємо автокомпліт
    var autocomplete = new google.maps.places.Autocomplete(firstEnterCityInput, autocompleteOptions);

    // Евент вибору міста в автокомпліті
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