'use strict';

app.controller('MapCtrl', function($scope, $location, $http) {

    /**
     * Змінні
     **/
    var map,
        markers = [],
        cityInput = document.getElementById('sidebar-city-input'),
        markerClusterer,
        geocoder;

    /**
     * Фільтри
     **/
    $scope.filters = {
        city: "",
        zoom: parseInt(9),
        latLng: "50.442218,30.779838"
    };

    /**
     * Код карти
     **/
    function initializeMap() {

        /**
         * Карта
         **/
        var mapOptions = {
            center: new google.maps.LatLng($scope.filters.latLng.split(",")[0], $scope.filters.latLng.split(",")[1]),
            zoom: parseInt($scope.filters.zoom),
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            mapTypeControl: false,
            streetViewControl: false
        };
        map = new google.maps.Map(document.getElementById("map"), mapOptions);

        /**
         * Автокомпліт
         **/
        var autocompleteOptions = {
            types: ['(cities)'],
            componentRestrictions: {
                country: "ua"
            }
        };
        var autocomplete = new google.maps.places.Autocomplete(cityInput, autocompleteOptions);
        autocomplete.bindTo('bounds', map);

        /**
         * Інші екземпляри
         **/
        markerClusterer = new MarkerClusterer(map);

        /**
         * Евенти карти
         **/
        // Лічильник тому що 'idle' спрацьовує при першій загрузці також
        var mapIdleCount = 0;
        // 'idle' - евент карти який спрацьову при загрузці всіх тайлів і промальовці карти
        google.maps.event.addListener(map, 'idle', function() {
            mapIdleCount++;
            $scope.filters.viewport = map.getBounds();
            if (mapIdleCount > 1) {
                $scope.filters.latLng   = map.getCenter().toUrlValue();
                $scope.filters.zoom     = map.getZoom();

                if(!$scope.$$phase)
                    $scope.$apply();

                setMapParametersToUrl();
                loadData();
            }
        });

        // Евент коли карта закінчила переміщення
        google.maps.event.addListenerOnce(map, 'idle', function() {
            // якщо урл при загрузці не пустий і має в собі параметр з містом
            // то центруємо карту по координатах в урлу і грузим дані
            if (Object.keys($location.search()).length && $location.search().city) {
                setMapParametersToUrl();
                //loadData();
                // якшо пустий то просто ставим карту на Україну
                // і додаєм параметри в урл
            } else {
                setMapParametersToUrl();
            }
        });

        // Евент вибору елемента в автокомпліті
        google.maps.event.addListener(autocomplete, 'place_changed', function() {
            var place = autocomplete.getPlace();

            if (!place.geometry) {
                return;
            }

            // If the place has a geometry, then present it on a map.
            if (place.geometry.viewport) {
                map.fitBounds(place.geometry.viewport);
            } else {
                map.panTo(place.geometry.location);
                map.setZoom(17);
            }

            $scope.filters.city = cityInput.value;

            if(!$scope.$$phase)
                $scope.$apply();
        });
    }


    /**
     * Парсимо строку пошука (все шо після '?')
     * Оновлюємо колекцію фільтрів '$scope.filters'
     **/
    $scope.parseSearchParametersFromUrl = function() {
        var searchParameters = $location.search();

        for (var key in searchParameters) {
            if (searchParameters.hasOwnProperty(key)) {
                $scope.filters[key] = searchParameters[key];
            }
        }

        initializeMap();
        initPlugins();

        console.log("Filters are parsed");
    };


    /**
     * Парсимо колекцію з фільтрами '$scope.filters'
     * Оновлюємо строку пошука все шо після '?')
     **/
    function parseFiltersCollectionAndUpdateUrl() {
        var filters = $scope.filters;

        for (var key in filters) {
            if (filters.hasOwnProperty(key)) {
                if (key == "city")
                    $location.search(key, encodeURI(filters[key]));

                if (filters[key] != "" && filters[key] != false)
                    $location.search(key, filters[key]);

                if (filters[key] === false || filters[key] == "" || key == "viewport")
                    $location.search(key, null);
            }
        }

        // частина урла яка додається до ссилок
        $scope.urlFiltersPart = $location.url()
                                    .replace("/search", "")
                                    .replace("/account/registration", "")
                                    .replace("/account/restore-access", "")
                                    .replace("/account/login", "");

        console.log("Filters collection parsed");
    }


    /**
     * Обновляє параметри карти в строці пошука
     **/
    function setMapParametersToUrl() {
        $location.search("latLng", $scope.filters.latLng);
        $location.search("zoom", parseInt($scope.filters.zoom));

        if(!$scope.$$phase)
            $scope.$apply();
    }


    /**
     * Функція яка ініціює загрузку даних
     * */
    function loadData() {
        var neLat = $scope.filters.viewport.ga.b,
            neLng = $scope.filters.viewport.ga.d,
            swLat = $scope.filters.viewport.ta.b,
            swLng = $scope.filters.viewport.ta.d,

            viewport = "&ne=" + neLat + ":" + neLng + "&sw=" + swLat + ":" + swLng;

        $http({
            url: "ajax/api/markers/?tids=1;2;3" + viewport,
            method: "GET",
            headers: {
                'X-CSRFToken': "fat32tsg4363"
            }
        });
    }


    /**
     * Вертає центр карти на місто введене в автокомпліті
     **/
    function returnMapPositionFromAddress() {
        var address = $scope.filters.city;

        geocoder = new google.maps.Geocoder();

        geocoder.geocode({ 'address': address }, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                if (results[0].geometry.viewport)
                    map.fitBounds(results[0].geometry.viewport);
                else {
                    map.panTo(results[0].geometry.location);
                    map.setZoom(17);
                }
            }
        });
    }


    /**
     * Слідкуємо за тим чи користувач закінчив екскурсію ))
     **/
//    var visitCount = 0;
//    $scope.$watch("visited", function(newValue, oldValue) {
//        visitCount++;
//        if (newValue == true && visitCount > 2) {
//            parseFiltersCollectionAndUpdateUrl();
//            returnMapPositionFromAddress();
//        }
//    });


    /**
     * Слідкуємо за зміною фільттрів. Динамічно оновлюємо урл
     **/
    $scope.$watchCollection("filters", function(newValue, oldValue) {
        parseFiltersCollectionAndUpdateUrl();

        console.log(newValue);
    });


    /**
     * Ініціалізація бутстраповських плагінів
     **/
    function initPlugins() {
        var propertyTypeSelect = $("#sidebar-property-type-select");
        propertyTypeSelect.selectpicker({
            style: 'btn btn-lg btn-default',
            menuStyle: 'dropdown-inverse'
        });

        var sidebarRedCurrencyTypeSelect = $("#sidebar-red-currency-type-select");
        sidebarRedCurrencyTypeSelect.selectpicker({
            style: 'btn btn-lg btn-default',
            menuStyle: 'dropdown-inverse'
        });
    }
});