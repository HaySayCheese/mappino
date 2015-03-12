'use strict';

/*
 * ПЛІЗ НЕ МІНЯЙТЕ НІЧО В ЦЬОМУ ФАЙЛІ
 * СПЛОШНА МАГІЯ, МІСТІКА І ЇМ ПОДІБНЕ
 */

app.controller('MapCtrl', function($scope, $location, $http, $timeout, $compile, $rootScope, Markers) {

    /**
     * Змінні
     **/

    var BASE_MAP_ZOOM = 15;

    var map,
        _tempViewportFromHomePage,
        markers = [],
        cityInput,
        autocomplete,
        autocompleteOptions = {
            componentRestrictions: {
                country: "ua"
            }
        },
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
            latLng: "48.455935, 34.41285" // translate: для інших країн має бути інший початковий регіон
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
            mansard:            true,
            ground:             true
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
     * Стан загрузки темплейта для панелі
     **/
    $scope.status = {
        redTemplateIsLoaded:    false,
        blueTemplateIsLoaded:   false,
        greenTemplateIsLoaded:  false,
        yellowTemplateIsLoaded: false
    };


    /**
     * Слідкуємо за зміною типа нерухомості на панелі і створюємо
     * для неї фільтри в залежності від вибраного типа нерухомості
     **/
    //$scope.$watch("filters.red.r_type_sid", function(newValue, oldValue) {
    //    $scope.status.redTemplateIsLoaded = false;
    //    if (!oldValue && newValue) {
    //        createFiltersForPanels("red", false);
    //    } else {
    //        createFiltersForPanels("red", true);
    //    }
    //});
    //$scope.$watch("filters.blue.b_type_sid", function(newValue, oldValue) {
    //    $scope.status.blueTemplateIsLoaded = false;
    //    if (!oldValue && newValue) {
    //        createFiltersForPanels("blue", false);
    //    } else {
    //        createFiltersForPanels("blue", true);
    //    }
    //});
    //$scope.$watch("filters.green.g_type_sid", function(newValue, oldValue) {
    //    $scope.status.greenTemplateIsLoaded = false;
    //    if (!oldValue && newValue) {
    //        createFiltersForPanels("green", false);
    //    } else {
    //        createFiltersForPanels("green", true);
    //    }
    //});
    //$scope.$watch("filters.yellow.y_type_sid", function(newValue, oldValue) {
    //    $scope.status.yellowTemplateIsLoaded = false;
    //    if (!oldValue && newValue) {
    //        createFiltersForPanels("yellow", false);
    //    } else {
    //        createFiltersForPanels("yellow", true);
    //    }
    //});


    /**
     * Слідкуємо за зміною фільтрів, оновлюємо урл та грузимо
     * дані в залежності від фільтрів
     **/
    $scope.$watchCollection("filters.red", function(newValue, oldValue) {
        // Якщо для цієї панелі ще не було обрано тип нерухомості
        // то створюємо фільтри для неї за типом
        if (!oldValue.r_type_sid && newValue.r_type_sid) {
            createFiltersForPanels("red", false);
        } else {
            createFiltersForPanels("red", true);
        }
        // Парсимо фільтри, оновлюємо урл і грузимо дані
        parseFiltersCollectionAndUpdateUrl(newValue);
        loadData(true);
    });
    $scope.$watchCollection("filters.blue", function(newValue, oldValue) {
        if (!oldValue.r_type_sid && newValue.r_type_sid) {
            createFiltersForPanels("blue", false);
        } else {
            createFiltersForPanels("blue", true);
        }
        parseFiltersCollectionAndUpdateUrl(newValue);
        loadData(true);
    });
    $scope.$watchCollection("filters.green", function(newValue, oldValue) {
        if (!oldValue.r_type_sid && newValue.r_type_sid) {
            createFiltersForPanels("green", false);
        } else {
            createFiltersForPanels("green", true);
        }
        parseFiltersCollectionAndUpdateUrl(newValue);
        loadData(true);
    });
    $scope.$watchCollection("filters.yellow", function(newValue, oldValue) {
        if (!oldValue.r_type_sid && newValue.r_type_sid) {
            createFiltersForPanels("yellow", false);
        } else {
            createFiltersForPanels("yellow", true);
        }
        parseFiltersCollectionAndUpdateUrl(newValue);
        loadData(true);
    });


    /**
     * Функція встановлення мінімального зума карти для пошуку обєктів
     **/
    $scope.setMinimumZoom = function() {
        $scope.filters.map.zoom = BASE_MAP_ZOOM;
        map.setZoom(BASE_MAP_ZOOM);
        parseFiltersCollectionAndUpdateUrl($scope.filters.map);
    };


    /**
     * Функція створення обєкта з фільтрами.
     * По дефолту обєкт з фільтрами для панелі немає фільтрів окрім
     * '<prefix>_type_sid'. В залежности від вибраного типу нерухомості
     * створюємо для цього обєкта фільтри або видаляємо їх якщо тип не вибраний
     **/
    function createFiltersForPanels(panel_color, clear_previous_filters) {
        var baseFilters = $scope.filters.base,
            filters = $scope.filters[panel_color],
            prefix = panel_color.toString().substring(0, 1) + "_",
            types = $rootScope.publicationTypes,
            tid = filters[prefix + 'type_sid'];

        if (clear_previous_filters) {

            // Видаляємо поля (фільтри) з панелі за колььором
            for (var key in filters) {
                // Залишаємо поле '<prefix>_type_sid'
                // для відображення дропдауна
                if (key === prefix + "type_sid"){
                    continue;
                }

                if (filters.hasOwnProperty(key)) {
                    delete filters[key];
                }
            }

            // Видаляємо фільтри з урла
            var searchParameters = $location.search();
            for (var s_key in searchParameters) {
                if (searchParameters.hasOwnProperty(s_key)) {
                    if (s_key.match(new RegExp('^' + prefix, 'm'))) {
                        $location.search(s_key, null);
                    }
                }
            }
            // Оновлюємо урл.
            // Додаємо в нього фільтри створені для панелі за кольором
            //parseFiltersCollectionAndUpdateUrl(filters);
            //parseFiltersCollectionAndUpdateUrl($scope.filters.map);
        }



        if (tid !== null) {
            // Створюємо набір фільтрів для панелі за набором в
            // '$rootScope.publicationTypes'
            for (var i=0; i<types[tid].filters.length; i++) {
                var filterName = prefix + types[tid].filters[i];

                if (!filters[filterName])
                    filters[filterName] = baseFilters[types[tid].filters[i]];
            }
        }
    }


    /**
     * google map initialize function
     **/
    function initializeMap() {

        // якщо з головної приходить вюпорт в локалстор
        var bounds = {};
        if (_tempViewportFromHomePage) {
            var c = _tempViewportFromHomePage.replace( /[\s()]/g, '' ).split( ','),
                sw = new google.maps.LatLng(+c[0], +c[1]),
                ne = new google.maps.LatLng(+c[2], +c[3]);

            bounds = new google.maps.LatLngBounds(sw, ne);
        }


        /**
         * Карта
         **/
        var mapOptions = {
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            disableDefaultUI: true
        };

        map = new google.maps.Map(document.getElementById("map"), mapOptions);

        if (_tempViewportFromHomePage) {
            map.fitBounds(bounds);
        } else {
            map.panTo(new google.maps.LatLng($scope.filters.map.latLng.split(",")[0], $scope.filters.map.latLng.split(",")[1]));
            map.setZoom(parseInt($scope.filters.map.zoom));
        }



        /**
         * b-zoom-control
         **/
        var zoomControlDiv  = document.createElement('div'),
            zoomControl     = new BMapZoomControl(zoomControlDiv, map, 'LEFT_BOTTOM');


        /**
         * Евенти карти
         **/
        google.maps.event.addListener(map, 'idle', function() {
            $scope.filters.map.latLng   = map.getCenter().toUrlValue();
            $scope.filters.map.viewport = map.getBounds();
            $scope.filters.map.zoom     = map.getZoom();

            parseFiltersCollectionAndUpdateUrl($scope.filters.map);

            mapIsLoaded = true;

            loadData(false);

            if(!$scope.$$phase)
                $scope.$apply();
        });
    }


    /**
     * Створюємо обєкти з фільтрами для панелей якщо в урл є '<prefix>_type_sid'
     * Парсимо строку з фільтрами та розкладаємо їх по створених обєктах.
     **/
    $scope.parseSearchParametersFromUrl = function() {
        var searchParameters = $location.search();

        searchParameters['r_type_sid'] ? createFiltersForPanels("red", false) :
            searchParameters['b_type_sid'] ? createFiltersForPanels("blue", false) :
                searchParameters['g_type_sid'] ? createFiltersForPanels("green", false) :
                    searchParameters['y_type_sid'] ? createFiltersForPanels("yellow", false) : createFiltersForPanels("red", false);


        $rootScope.sidebarTemplateUrl = "/ajax/template/main/sidebar/common/";


        $timeout(function() {
            cityInput = document.getElementById('sidebar-city-input');
            autocomplete = new google.maps.places.Autocomplete(cityInput, autocompleteOptions);
            autocomplete.bindTo('bounds', map);

            // Евент вибору елемента в автокомпліті
            google.maps.event.addListener(autocomplete, 'place_changed', function() {
                var place = autocomplete.getPlace();

                if (!place.geometry)
                    return;

                if (place.geometry.viewport && place.types[0] !== "locality") {
                    map.fitBounds(place.geometry.viewport);
                } else {
                    map.panTo(place.geometry.location);
                    map.setZoom(BASE_MAP_ZOOM);
                }

                $timeout(function() {
                    cityInput.value = cityInput.value.substring(0, cityInput.value.lastIndexOf(","));
                    $scope.filters.map.city = cityInput.value;

                    if(!$scope.$$phase)
                        $scope.$apply();
                }, 0);
            });
        }, 2000);


        // якщо в урлі нема параметра з координатами то берем з локалстора
        // те що передали з головної
        if (!searchParameters['latLng'] && localStorage._tempViewportFromHomePage) {
            _tempViewportFromHomePage = localStorage._tempViewportFromHomePage;
            delete localStorage._tempViewportFromHomePage;
        }


        for (var key in searchParameters) {
            if (searchParameters.hasOwnProperty(key)) {

                if (key.toString() === "token")
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


                if (key === "city" || key === "zoom" || key === "latLng")
                    $scope.filters.map[key] = searchParameters[key];
            }
        }

        $scope.filtersParsed = true;

        initializeMap();
    };


    /**
     * Встановлення оффсета для карти
     *
     * юзається для рієлторів, не видаляти!!
     **/
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
     * Парсимо обєкти з фільтрами та додаємо їх в урл
     **/
    function parseFiltersCollectionAndUpdateUrl(filters) {
        for (var key in filters) {
            if (filters.hasOwnProperty(key)) {

                if (key.indexOf("type_sid") !== -1 && filters[key] === null) {
                    return false;
                }

                if (filters[key] === "0" || filters[key] === 0) {
                    $location.search(key, filters[key]);
                    continue;
                }

                if (filters[key] === "" || filters[key] === false || filters[key] === "false" || key === "viewport") {
                    $location.search(key, null);
                } else {
                    $location.search(key, filters[key]);
                }
            }
        }

        createUrlFiltersPart();

        if (!$scope.$$phase)
            $scope.$apply();
    }


    /**
     * Зберігаємо частину урл з фільтрами для підміни в разі
     * закриття діалогів
     **/
    function createUrlFiltersPart() {
        $scope.urlFiltersPart = $location.url()
            .replace("/account/registration", "")
            .replace("/account/restore-access", "")
            .replace("/account/login", "")
            .replace("/publication/" + $scope.publicationIdPart, "");
    }


    /**
     * Функція яка ініціює загрузку даних
     */
    function loadData(timeout) {

        $timeout(function() {
            if (!mapIsLoaded) {
                return;
            }

            var sneLat = $scope.filters.map.viewport.getNorthEast().lat().toString(),
                sneLng = $scope.filters.map.viewport.getNorthEast().lng().toString(),
                sswLat = $scope.filters.map.viewport.getSouthWest().lat().toString(),
                sswLng = $scope.filters.map.viewport.getSouthWest().lng().toString();

            var neLat = sneLat.replace(sneLat.substring(sneLat.indexOf(".") + 3, sneLat.length), ""),
                neLng = sneLng.replace(sneLng.substring(sneLng.indexOf(".") + 3, sneLng.length), ""),
                swLat = sswLat.replace(sswLat.substring(sswLat.indexOf(".") + 3, sswLat.length), ""),
                swLng = sswLng.replace(sswLng.substring(sswLng.indexOf(".") + 3, sswLng.length), ""),
                viewport = {
                    'ne_lat': neLat,
                    'ne_lng': neLng,
                    'sw_lat': swLat,
                    'sw_lng': swLng
                };

            if (timeout) {
                clearTimeout(requestTimeout);
                requestTimeout = setTimeout(function() {
                    Markers.load($scope.filters.red, $scope.filters.blue,
                                    $scope.filters.green, $scope.filters.yellow,
                                    viewport, $scope.filters.map.zoom, function(data) {

                        markers = data;
                        placeMarkers(data);
                    });
                }, requestTimeoutTime);
            } else {
                Markers.load($scope.filters.red, $scope.filters.blue,
                                $scope.filters.green, $scope.filters.yellow,
                                viewport, $scope.filters.map.zoom, function(data) {

                    markers = data;
                    placeMarkers(data);
                });
            }
        }, 100);
    }


    /**
     * Функція яка розставляє маркери
     */
    function placeMarkers(data) {
        for (var panel in data) {
            if (data.hasOwnProperty(panel)) {
                for (var marker in markers[panel]) {
                    if (markers[panel].hasOwnProperty(marker)) {
                        markers[panel][marker].setMap(map);

                        (function() {
                            var marker1 = markers[panel][marker];

                            if (marker1.type != "pie-marker")
                                google.maps.event.addListener(marker1, 'click', function() {
                                    $location.path("/publication/" + marker1.tid + ":" + marker1.id);

                                    if (!$scope.$$phase)
                                        $scope.$apply();
                                });
                            else
                                google.maps.event.addListener(marker1, 'click', function(e) {
                                    map.setZoom(map.getZoom() + 1);
                                    map.setCenter(marker1.getPosition());
                                });
                        })();
                    }
                }
            }
        }
    }



    /**
     * Ініціалізація бутстраповських плагінів
     */
    $scope.initPlugins = function() {
        initDropdown();
        initScrollBarInPanels();
    };
    function initDropdown() {
        $timeout(function() {
            angular.element(".sidebar-body select:not(.type-selectpicker)").selectpicker({
                style: 'btn-default btn-md',
                container: angular.element("body")
            });
        }, 0);
    }
    function initScrollBarInPanels() {
        $timeout(function() {
            var sidebar = angular.element(".panel-body");

            sidebar.perfectScrollbar("destroy");
            sidebar.perfectScrollbar({
                wheelSpeed: 20,
                useKeyboard: false
            });

            angular.element(window).resize(function() {
                sidebar.perfectScrollbar("update");
            });

            $scope.$watchCollection('status', function() {
                sidebar.perfectScrollbar("update");
            });

        }, 1000);
    }
});