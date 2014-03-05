'use strict';

app.controller('MapCtrl', function($scope, $location, $http, $timeout, $compile, Markers) {

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

        map: {
            city: "",
            zoom: parseInt(9),
            latLng: "50.442218,30.779838"
        },

        red: {
            r_type_sid: 0,
            r_operation_sid: 0,
            r_price_min: "",
            r_price_max: "",
            r_currency_sid: 0,

            // Тільки для оренди
            r_period_sid: 0,
            r_rent_family: false,
            r_rent_foreigners: false
        },

        blue: {
            b_type_sid: 0,
            b_operation_sid: 0,
            b_price_min: "",
            b_price_max: "",
            b_currency_sid: 0,

            // Тільки для оренди
            b_period_sid: 0,
            b_rent_family: false,
            b_rent_foreigners: false
        }
    };
    $scope.filtersParsed = false;


    /**
     * Слідкуємо за зміною фільттрів. Динамічно оновлюємо урл
     **/
    $scope.$watchCollection("filters.red", function(newValue, oldValue) {
        parseFiltersCollectionAndUpdateUrl(newValue);
    });
    $scope.$watchCollection("filters.blue", function(newValue, oldValue) {
        parseFiltersCollectionAndUpdateUrl(newValue);
    });


    /**
     * Код карти
     **/
    function initializeMap() {

        /**
         * Карта
         **/
        var mapOptions = {
            center: new google.maps.LatLng($scope.filters.map.latLng.split(",")[0], $scope.filters.map.latLng.split(",")[1]),
            zoom: parseInt($scope.filters.map.zoom),
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
        markerClusterer = new MarkerClusterer(map, markers);

        /**
         * Евенти карти
         **/
        // Лічильник тому що 'idle' спрацьовує при першій загрузці також
        var mapIdleCount = 0;
        // 'idle' - евент карти який спрацьову при загрузці всіх тайлів і промальовці карти
        google.maps.event.addListener(map, 'idle', function() {
            mapIdleCount++;
            $scope.filters.map.viewport = {
                neLat: map.getBounds().getNorthEast().lat(),
                neLng: map.getBounds().getNorthEast().lng(),
                swLat: map.getBounds().getSouthWest().lat(),
                swLng: map.getBounds().getSouthWest().lng()
            };
            if (mapIdleCount > 1) {
                $scope.filters.map.latLng   = map.getCenter().toUrlValue();
                $scope.filters.map.zoom     = map.getZoom();

                if(!$scope.$$phase)
                    $scope.$apply();

                parseFiltersCollectionAndUpdateUrl($scope.filters.map);
                loadData();
            }
        });

        // Евент коли карта закінчила переміщення
        google.maps.event.addListenerOnce(map, 'idle', function() {
            // якщо урл при загрузці не пустий і має в собі параметр з містом
            // то центруємо карту по координатах в урлу і грузим дані
            if (Object.keys($location.search()).length && Object.keys($location.search()).length > 2) {
                //parseFiltersCollectionAndUpdateUrl($scope.filters.map);
                loadData();
                // якшо пустий то просто ставим карту на Україну
                // і додаєм параметри в урл
            } else {
                parseFiltersCollectionAndUpdateUrl($scope.filters.map);
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

            $scope.filters.map.city = cityInput.value;

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
                if (key.toString().indexOf("_sid") !== -1)
                    searchParameters[key] = parseInt(searchParameters[key]);

                if (key.toString().indexOf("r_") !== -1) {
                    $scope.filters.red[key] = searchParameters[key];
                    continue;
                }

                if (key.toString().indexOf("b_") !== -1) {
                    $scope.filters.blue[key] = searchParameters[key];
                    continue;
                }

                if (key.toString().indexOf("g_") !== -1) {
                    $scope.filters.green[key] = searchParameters[key];
                    continue;
                }

                if (key.toString().indexOf("y_") !== -1) {
                    $scope.filters.yellow[key] = searchParameters[key];
                    continue;
                }

                if (key == "city" || key == "zoom" || key == "latLng")
                    $scope.filters.map[key] = searchParameters[key];
            }
        }
        $scope.filtersParsed = true;


        initializeMap();

        console.log("Filters are parsed");
    };


    /**
     * Парсимо колекцію з фільтрами '$scope.filters'
     * Оновлюємо строку пошука все шо після '?')
     **/
    function parseFiltersCollectionAndUpdateUrl(filters) {
        for (var key in filters) {
            if (filters.hasOwnProperty(key)) {
                if (filters[key] == "" || filters[key] === false || filters[key] == "false" || key == "viewport")
                    $location.search(key, null);
                else
                    $location.search(key, filters[key]);
            }
        }

        // частина урла яка додається до ссилок
        $scope.urlFiltersPart = $location.url()
            .replace("/search", "")
            .replace("/account/registration", "")
            .replace("/account/restore-access", "")
            .replace("/account/login", "");

        if (!$scope.$$phase)
            $scope.$apply();
    }


    /**
     * Функція яка ініціює загрузку даних
     * */
    function loadData() {
        var sneLat = $scope.filters.map.viewport.neLat.toString(),
            sneLng = $scope.filters.map.viewport.neLng.toString(),
            sswLat = $scope.filters.map.viewport.swLat.toString(),
            sswLng = $scope.filters.map.viewport.swLng.toString();

        var neLat = sneLat.replace(sneLat.substring(sneLat.indexOf(".") + 3, sneLat.length), ""),
            neLng = sneLng.replace(sneLng.substring(sneLng.indexOf(".") + 3, sneLng.length), ""),
            swLat = sswLat.replace(sswLat.substring(sswLat.indexOf(".") + 3, sswLat.length), ""),
            swLng = sswLng.replace(sswLng.substring(sswLng.indexOf(".") + 3, sswLng.length), ""),
            viewport = "&ne=" + neLat + ":" + neLng + "&sw=" + swLat + ":" + swLng;

        Markers.load(viewport, 0, function(data) {
            markers = data;
            placeMarkers();
        });
    }


    function placeMarkers() {
        markerClusterer.clearMarkers();

        for (var i = 0; i < markers.length; i++) {
            markers[i].setMap(map);
            markerClusterer.addMarker(markers[i]);
        }
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
     * Ініціалізація бутстраповських плагінів
     **/
    $scope.initDropdown = function() {
        $timeout(function() {
            angular.element(".sidebar-body select").selectpicker({
                style: 'btn-default btn-md'
            });
        }, 500);
    }
});