'use strict';

/*
 * ПЛІЗ НЕ МІНЯЙТЕ НІЧО В ЦЬОМУ ФАЙЛІ
 * СПЛОШНА МАГІЯ, МІСТІКА І ЇМ ПОДІБНЕ
 */

app.controller('MapCtrl', function($scope, $location, $http, $timeout, $compile, $rootScope, Markers) {

    /**
     * Змінні
     **/
    var map,
        markers = [],
        cityInput,// = document.getElementById('sidebar-city-input'),
        autocomplete,
        autocompleteOptions = {
            componentRestrictions: {
                country: "ua"
            }
        },
        geocoder,
        requestTimeout,
        requestTimeoutTime = 1500,
        mapIsLoaded = false;

    /**
     * Фільтри
     **/
    $scope.filters = {

        map: {
            city: "",
            zoom: parseInt(6),
            latLng: "48.455935, 34.41285"
        },

        base: {
            // Загальні
            operation_sid: 0,

            // Дропдауни
            currency_sid:       0,
            heating_type_sid:   0,
            period_sid:         0,
            planing_sid:        0,
            building_type_sid:  0,

            // Поля вводу
            price_from:             "",
            price_to:               "",
            rooms_count_from:       "",
            rooms_count_to:         "",
            floors_count_from:      "",
            floors_count_to:        "",
            persons_count_from:     "",
            persons_count_to:       "",
            total_area_from:        "",
            total_area_to:          "",
            floor_from:             "",
            floor_to:               "",
            halls_area_from:        "",
            halls_area_to:          "",
            cabinets_count_from:    "",
            cabinets_count_to:      "",
            halls_count_from:       "",
            halls_count_to:         "",
            ceiling_height_from:    "",
            ceiling_height_to:      "",
            area_from:              "",
            area_to:                "",

            // Чекбокси
            new_buildings:      true,
            secondary_market:   true,
            family:             false,
            foreigners:         false,
            electricity:        false,
            gas:                false,
            hot_water:          false,
            cold_water:         false,
            sewerage:           false,
            lift:               false,
            security:           false,
            kitchen:            false,
            security_alarm:     false,
            fire_alarm:         false,
            pit:                false,
            water:              false,
            mansard:            false,
            ground:             false
        },

        red: {
            r_type_sid: 0
        },

        blue: {
            b_type_sid: null
        },

        green: {
            g_type_sid: null
        },

        yellow: {
            y_type_sid: null
        }
    };


    /**
     * Слідкуємо за зміною типа нерухомості на панелі і грузимо темплейт
     */
    $scope.$watch("filters.red.r_type_sid", function(newValue) {
        createFiltersForPanels("red", newValue, true);
    });
    $scope.$watch("filters.blue.b_type_sid", function(newValue) {
        createFiltersForPanels("blue", newValue, true);
    });
    $scope.$watch("filters.green.g_type_sid", function(newValue) {
        createFiltersForPanels("green", newValue, true);
    });
    $scope.$watch("filters.yellow.y_type_sid", function(newValue) {
        createFiltersForPanels("yellow", newValue, true);
    });


    /**
     * Слідкуємо за зміною фільттрів. Динамічно оновлюємо урл
     */
    $scope.$watchCollection("filters.red", function(newValue, oldValue) {
        parseFiltersCollectionAndUpdateUrl(newValue);

        loadData(newValue, "red", true)
    });
    $scope.$watchCollection("filters.blue", function(newValue, oldValue) {
        parseFiltersCollectionAndUpdateUrl(newValue);

        loadData(newValue, "blue", true)
    });
    $scope.$watchCollection("filters.green", function(newValue, oldValue) {
        parseFiltersCollectionAndUpdateUrl(newValue);

        loadData(newValue, "green", true)
    });
    $scope.$watchCollection("filters.yellow", function(newValue, oldValue) {
        parseFiltersCollectionAndUpdateUrl(newValue);

        loadData(newValue, "yellow", true)
    });
    $rootScope.$on("first-enter-change", function(event, data) {
        $scope.filters.map.zoom = data[1];
        $scope.filters.map.latLng = data[0];
        $scope.filters.map.city = data[2];

        map.panTo($scope.filters.map.latLng);
        map.setZoom($scope.filters.map.zoom);
    });


    /**
     * Функція встановлення мінімального зума карти для пошуку обєктів
     */
    $scope.setMinimumZoom = function() {
        $scope.filters.map.zoom = 15;

        map.setZoom(15);

        parseFiltersCollectionAndUpdateUrl($scope.filters.map);
    };


    /**
     * Функція створення обєкта з фільтрами
     */
    function createFiltersForPanels(panel, tid, clear) {
        var baseFilters = $scope.filters.base,
            filters     = $scope.filters[panel],
            types       = $rootScope.publicationTypes,
            prefix      = panel.toString().substring(0, 1) + "_";

        $scope.templateLoaded = false;
        $timeout(function() {
            $scope.templateLoaded = true;
        }, 1000);

        if (clear) {
            for (var key in filters) {
                if (filters.hasOwnProperty(key) && key != (prefix + "type_sid"))
                    delete filters[key];
            }
            var searchParameters = $location.search();

            for (var s_key in searchParameters) {
                if (searchParameters.hasOwnProperty(s_key))
                    if (s_key.match(new RegExp('^' + prefix, 'm')))
                        $location.search(s_key, null)
            }
            parseFiltersCollectionAndUpdateUrl(filters);
            parseFiltersCollectionAndUpdateUrl($scope.filters.map);
        }

        if (filters[prefix + "type_sid"] === null)
            return;

        for (var i = 0; i < types[tid].filters.length; i++) {
            if (!filters[[prefix + types[tid].filters[i]]])
                filters[prefix + types[tid].filters[i]] = baseFilters[types[tid].filters[i]];
        }
    }


    /**
     * Код карти
     */
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
         * Інші екземпляри
         **/


        /**
         * Евенти карти
         **/
        google.maps.event.addListener(map, 'idle', function() {
            $scope.filters.map.latLng   = map.getCenter().toUrlValue();
            $scope.filters.map.viewport = map.getBounds();
            $scope.filters.map.zoom     = map.getZoom();

            parseFiltersCollectionAndUpdateUrl($scope.filters.map);

            mapIsLoaded = true;

            if ($scope.filters.map.zoom < 15 && !$rootScope.subdommain) {
                Markers.clearPanelMarkers("red");
                Markers.clearPanelMarkers("blue");
                Markers.clearPanelMarkers("green");
                Markers.clearPanelMarkers("yellow");

                return;
            }

            loadData($scope.filters.red, "red", false);
            loadData($scope.filters.blue, "blue", false);
            loadData($scope.filters.green, "green", false);
            loadData($scope.filters.yellow, "yellow", false);

            if(!$scope.$$phase)
                $scope.$apply();
        });
    }


    /**
     * Парсимо строку пошука (все шо після '?')
     * Оновлюємо колекцію фільтрів '$scope.filters'
     */
    $scope.parseSearchParametersFromUrl = function() {
        var searchParameters = $location.search();

            $rootScope.sidebarTemplateUrl = "ajax/template/main/sidebar/common/";

            $timeout(function() {
                cityInput = document.getElementById('sidebar-city-input');
                autocomplete = new google.maps.places.Autocomplete(cityInput, autocompleteOptions);
                autocomplete.bindTo('bounds', map);

                // Евент вибору елемента в автокомпліті
                google.maps.event.addListener(autocomplete, 'place_changed', function() {
                    var place = autocomplete.getPlace();

                    if (!place.geometry) {
                        return;
                    }

                    if (place.geometry.viewport) {
                        map.panTo(place.geometry.location);
                        map.setZoom(15);
                    } else {
                        map.panTo(place.geometry.location);
                        map.setZoom(15);
                    }

                    $scope.filters.map.city = cityInput.value;

                    if(!$scope.$$phase)
                        $scope.$apply();
                });
            }, 2000);


        for (var key in searchParameters) {
            if (searchParameters.hasOwnProperty(key)) {

                if (key.toString() == "token")
                    continue;

                if (key.toString().indexOf("_sid") != -1)
                    searchParameters[key] = parseInt(searchParameters[key]);


                if (/^r_/.test(key.toString()))
                    $scope.filters.red[key] = searchParameters[key];


                if (/^b_/.test(key.toString()))
                    $scope.filters.blue[key] = searchParameters[key];


                if (/^g_/.test(key.toString()))
                    $scope.filters.green[key] = searchParameters[key];


                if (/^y_/.test(key.toString()))
                    $scope.filters.yellow[key] = searchParameters[key];


                if (key == "city" || key == "zoom" || key == "latLng")
                    $scope.filters.map[key] = searchParameters[key];
            }
        }

        if ($scope.filters.blue.b_type_sid == null || $scope.filters.green.g_type_sid == null || $scope.filters.yellow.y_type_sid == null)
            createFiltersForPanels("red", 0, false);

        $scope.filtersParsed = true;

        $timeout(function() {
            $scope.templateLoaded = true;
        }, 1000);

        initializeMap();
    };


    /**
     * Встановлення оффсета для карти
     *
     * юзається для рієлторів, не видаляти!!
     */
    function offsetCenter(latlng, offsetx, offsety) {

        var scale = Math.pow(2, map.getZoom()),
            worldCoordinateCenter = map.getProjection().fromLatLngToPoint(latlng),
            pixelOffset = new google.maps.Point((offsetx / scale) || 0, (offsety / scale) || 0),

            worldCoordinateNewCenter = new google.maps.Point(
                worldCoordinateCenter.x - pixelOffset.x,
                worldCoordinateCenter.y + pixelOffset.y
            ),
            newCenter = map.getProjection().fromPointToLatLng(worldCoordinateNewCenter);

        if (!_.size(markers.red)) {
            newCenter = new google.maps.LatLng(48.455935, 34.41285);
            map.setCenter(newCenter);
            map.setZoom(6);
            return;
        }

        map.setCenter(newCenter);
        map.setZoom(map.getZoom() - 1);
    }


    /**
     * Парсимо колекцію з фільтрами '$scope.filters'
     * Оновлюємо строку пошука все шо після '?')
     */
    function parseFiltersCollectionAndUpdateUrl(filters) {
        for (var key in filters) {
            if (filters.hasOwnProperty(key)) {

                if (key.indexOf("type_sid") != -1 && filters[key] === null)
                    return;

                if (filters[key] === "0" || filters[key] === 0) {
                    $location.search(key, filters[key]);
                    continue;
                }

                if (filters[key] == "" || filters[key] === false || filters[key] == "false" || key == "viewport") {
                    $location.search(key, null);
                } else {
                    $location.search(key, filters[key]);
                }
            }
        }

        // частина урла яка додається до ссилок
        $scope.urlFiltersPart = $location.url()
            .replace("/search", "")
            .replace("/account/registration", "")
            .replace("/account/restore-access", "")
            .replace("/account/login", "")
            .replace("/first-enter", "")
            .replace("/publication/" + $scope.publicationIdPart, "");

        if (!$scope.$$phase)
            $scope.$apply();
    }


    /**
     * Функція яка ініціює загрузку даних
     */
    function loadData(filters, panel, timeout) {
        if ($rootScope.subdommain.length && $scope.filters.map.zoom < 15)
            return;

        $timeout(function() {
            if (!mapIsLoaded)
                return;

            var sneLat = $scope.filters.map.viewport.getNorthEast().lat().toString(),
                sneLng = $scope.filters.map.viewport.getNorthEast().lng().toString(),
                sswLat = $scope.filters.map.viewport.getSouthWest().lat().toString(),
                sswLng = $scope.filters.map.viewport.getSouthWest().lng().toString();

            var neLat = sneLat.replace(sneLat.substring(sneLat.indexOf(".") + 3, sneLat.length), ""),
                neLng = sneLng.replace(sneLng.substring(sneLng.indexOf(".") + 3, sneLng.length), ""),
                swLat = sswLat.replace(sswLat.substring(sswLat.indexOf(".") + 3, sswLat.length), ""),
                swLng = sswLng.replace(sswLng.substring(sswLng.indexOf(".") + 3, sswLng.length), ""),
                viewport = "&ne=" + neLat + ":" + neLng + "&sw=" + swLat + ":" + swLng;

            if (timeout) {
                clearTimeout(requestTimeout);
                requestTimeout = setTimeout(function() {
                    Markers.load(filters, viewport, panel, function(data) {
                        markers = data;
                        placeMarkers();
                    });
                }, requestTimeoutTime);
            } else {
                Markers.load(filters, viewport, panel, function(data) {
                    markers = data;
                    placeMarkers();
                });
            }
        }, 100);
    }


    /**
     * Функція яка розставляє маркери
     */
    function placeMarkers() {
        for (var panel in markers) {
            if (markers.hasOwnProperty(panel)) {
                for (var marker in markers[panel]) {
                    if (markers[panel].hasOwnProperty(marker)) {
                        markers[panel][marker].setMap(map);

                        (function() {
                            var marker1 = markers[panel][marker];

                            google.maps.event.addListener(marker1, 'click', function() {
                                $location.path("/publication/" + marker1.tid + ":" + marker1.id);

                                if (!$scope.$$phase)
                                    $scope.$apply();
                            });
                        })();

                    }
                }
            }
        }
    }


    /**
     * Вертає центр карти на місто введене в автокомпліті
     */
    function returnMapPositionFromAddress() {
        var address = $scope.filters.map.city;

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
     */
    $scope.initPlugins = function() {
        initDropdown();
        initScrollBar();
    };
    function initDropdown() {
        $timeout(function() {
            angular.element(".sidebar-body select:not(.type-selectpicker)").selectpicker({
                style: 'btn-default btn-md',
                container: angular.element("body")
            });
        }, 0);
    }
    function initScrollBar() {
        $timeout(function() {

            var sidebar = angular.element(".panel-body");

            sidebar.perfectScrollbar("destroy");
            sidebar.perfectScrollbar({
                wheelSpeed: 20,
                useKeyboard: false
            });

            angular.element(window).resize(function() {
                sidebar.perfectScrollbar("update")
            });
            $scope.$watch("filters.red.r_type_sid", function() {
                $timeout(function() {
                    sidebar.scrollTop(0);
                    sidebar.perfectScrollbar("update");
                    sidebar.perfectScrollbar("update");
                }, 500);
            });
            $scope.$watch("filters.blue.b_type_sid", function() {
                $timeout(function() {
                    sidebar.scrollTop(0);
                    sidebar.perfectScrollbar("update");
                    sidebar.perfectScrollbar("update");
                }, 500);
            });
            $scope.$watch("filters.green.g_type_sid", function() {
                $timeout(function() {
                    sidebar.scrollTop(0);
                    sidebar.perfectScrollbar("update");
                    sidebar.perfectScrollbar("update");
                }, 500);
            });
            $scope.$watch("filters.yellow.y_type_sid", function() {
                $timeout(function() {
                    sidebar.scrollTop(0);
                    sidebar.perfectScrollbar("update");
                    sidebar.perfectScrollbar("update");
                }, 500);
            });

        }, 1000);
    }
});