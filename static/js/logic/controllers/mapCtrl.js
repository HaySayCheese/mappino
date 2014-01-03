'use strict';

app.controller('MapCtrl', function($scope, $location) {

    /**
     * Змінні
     **/
    var map,
        markers = [],
        //cityInput = document.getElementById('filter-city'),
        markerClusterer,
        geocoder;

    /**
     * Фільтри
     **/
    $scope.filters = {
        city: "",
        latLng: "50.008197,33.498954",
        zoom:   7,

        propertyType:   localStorage.propertyType   || "houses",
        propertyTypeUa: localStorage.propertyTypeUa || "Дома",

        operationType: "all",

        priceMin: "",
        priceMax: "",

        areaMin: "",
        areaMax: "",

        floorMin: "",
        floorMax: "",

        internet:   false,
        phone:      false,

        onlyBuildings: false
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
            zoom: parseFloat($scope.filters.zoom),
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
//        var autocomplete = new google.maps.places.Autocomplete(cityInput, autocompleteOptions);
//        autocomplete.bindTo('bounds', map);

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
            if (mapIdleCount > 1) {
                $scope.filters.latLng   = map.getCenter().toUrlValue();
                $scope.filters.zoom     = map.getZoom();

                if(!$scope.$$phase)
                    $scope.$apply();

                setMapParametersToUrl();
            }
        });

        google.maps.event.addListenerOnce(map, 'idle', function() {
            // якщо урл при загрузці не пустий і має в собі параметр з містом
            // то центруємо карту по координатах в урлу і грузим дані
            if (Object.keys($location.search()).length && $location.search().city) {
                setMapParametersToUrl();
                loadData();
                // якшо пустий то просто ставим карту на Україну
                // і додаєм параметри в урл
            } else {
                setMapParametersToUrl();
            }
        });

        // Вибір елемента в автокомпліті
//        google.maps.event.addListener(autocomplete, 'place_changed', function() {
//            var place = autocomplete.getPlace();
//            if (!place.geometry) {
//                return;
//            }
//
//            // If the place has a geometry, then present it on a map.
//            if (place.geometry.viewport) {
//                map.fitBounds(place.geometry.viewport);
//            } else {
//                map.panTo(place.geometry.location);
//                map.setZoom(17);  // Why 17? Because it looks good.
//            }
//
//            $scope.filters.city = cityInput.value;
//            if(!$scope.$$phase)
//                $scope.$apply();
//        });
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
//        dropdownInit();
//        radioButtonInit();

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

                if (filters[key] != "" && filters[key] != false /* не додаєм в урл деякі параметри */ && key != "propertyTypeUa" && key)
                    $location.search(key, filters[key]);

                if (filters[key] === false || filters[key] == "")
                    $location.search(key, null)
            }
        }

        console.log("Filters collection parsed");
    }


    /**
     * Обновляє параметри карти в строці пошука
     **/
    function setMapParametersToUrl() {
        $location.search("latLng", $scope.filters.latLng);
        $location.search("zoom", parseFloat($scope.filters.zoom));

        if(!$scope.$$phase)
            $scope.$apply();
    }


    /**
     * Функція яка ініціює загрузку даних
     * */
    function loadData() {
        propertyQuery.getPropertysByFilters($scope.filters).success(function() {
            setTimeout(function() {
                console.log("Loaded");
            }, 2000);
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
                    map.fitBounds(results[0].geometry.viewport)
                else {
                    map.panTo(results[0].geometry.location);
                    map.setZoom(17);
                }
            }
        });
    }


    /**
     * Клік по кнопці пошука
     **/
    $scope.reloadPropertyByFilters = function() {
        returnMapPositionFromAddress();
        parseFiltersCollectionAndUpdateUrl();
        loadData();
    };
});