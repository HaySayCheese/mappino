app.controller('ContentController', ['$scope', '$location', '$http', '$timeout', '$rootScope', 'MarkersFactory', 'FiltersFactory', 'LoadedValues',
    function($scope, $location, $http, $timeout, $rootScope, MarkersFactory, FiltersFactory, LoadedValues) {
        "use strict";


        /* Змінні */
        var BASE_MAP_ZOOM = 15;

        var map,
            markers = [],
            cityInput,
            autocomplete,
            autocompleteOptions = {
                componentRestrictions: {
                    country: "ua"
                }
            },
            requestTimeout,
            requestTimeoutTime = 1500;


        /**
         * Слідкуємо за зміною фільтрів, оновлюємо урл та грузимо
         * дані в залежності від фільтрів
         **/
        $scope.$watchCollection("filters.red", function(newValue, oldValue) {
            // Якщо для цієї панелі ще не було обрано тип нерухомості
            // то створюємо фільтри для неї за типом
            if (oldValue.r_t_sid !== newValue.r_t_sid) {
                LoadedValues.sidebar.templates.red = false;
                FiltersFactory.createFiltersForPanel("red", true);
            }
            // Парсимо фільтри, оновлюємо урл і грузимо дані
            FiltersFactory.updateUrlFromFilters(newValue);
            loadData(true);
        });

        $scope.$watchCollection("filters.blue", function(newValue, oldValue) {
            if (oldValue.b_t_sid !== newValue.b_t_sid) {
                LoadedValues.sidebar.templates.blue = false;
                FiltersFactory.createFiltersForPanel("blue", true);
            }
            FiltersFactory.updateUrlFromFilters(newValue);
            loadData(true);
        });

        $scope.$watchCollection("filters.green", function(newValue, oldValue) {
            if (oldValue.g_t_sid !== newValue.g_t_sid) {
                LoadedValues.sidebar.templates.green = false;
                FiltersFactory.createFiltersForPanel("green", true);
            }
            FiltersFactory.updateUrlFromFilters(newValue);
            loadData(true);
        });

        $scope.$watchCollection("filters.yellow", function(newValue, oldValue) {
            if (oldValue.y_t_sid !== newValue.y_t_sid) {
                LoadedValues.sidebar.templates.yellow = false;
                FiltersFactory.createFiltersForPanel("yellow", true);
            }
            FiltersFactory.updateUrlFromFilters(newValue);
            loadData(true);
        });

        $scope.$watchCollection('status', function() {
            $rootScope.$broadcast('updatePerfectScrollbar');
        });




        $scope.runApplication = function() {
            FiltersFactory.updateFiltersFromUrl();
            $scope.filters = FiltersFactory.getFilters();

            LoadedValues.filters.parsed = true;
            initializeMap();
        };



        function initializeMap() {

            // якщо з головної приходить вюпорт в локалстор
            var bounds = {},
                tempViewportFromHomePage,
                searchParameters = $location.search();

            if (!searchParameters['l'] && localStorage._tempViewportFromHomePage) {
                tempViewportFromHomePage = localStorage._tempViewportFromHomePage;

                var c = tempViewportFromHomePage.replace( /[\s()]/g, '' ).split( ','),
                    sw = new google.maps.LatLng(+c[0], +c[1]),
                    ne = new google.maps.LatLng(+c[2], +c[3]);

                bounds = new google.maps.LatLngBounds(sw, ne);

                delete localStorage._tempViewportFromHomePage;
            }


            /* Карта */
            var mapOptions = {
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                disableDefaultUI: true
            };

            map = new google.maps.Map(document.getElementById("map"), mapOptions);

            if (tempViewportFromHomePage) {
                map.fitBounds(bounds);
            } else {
                map.panTo(new google.maps.LatLng($scope.filters.map.l.split(",")[0], $scope.filters.map.l.split(",")[1]));
                map.setZoom(parseInt($scope.filters.map.z));
            }



            /* b-zoom-control */
            var zoomControlDiv  = document.createElement('div'),
                zoomControl     = new BMapZoomControl(zoomControlDiv, map, 'LEFT_BOTTOM');


            /* Евенти карти */
            google.maps.event.addListener(map, 'idle', function() {
                $scope.filters.map.z = map.getZoom();
                $scope.filters.map.l = map.getCenter().toUrlValue();
                $scope.filters.map.v = map.getBounds();

                FiltersFactory.updateUrlFromFilters($scope.filters.map);

                LoadedValues.map.loaded = true;

                loadData(false);

                if(!$scope.$$phase)
                    $scope.$apply();
            });
        }


        $scope.initializeAutocomplete = function() {
            $timeout(function() {
                cityInput       = document.getElementById('sidebar-city-input');
                autocomplete    = new google.maps.places.Autocomplete(cityInput, autocompleteOptions);

                autocomplete.bindTo('bounds', map);

                // Евент вибору елемента в автокомпліті
                google.maps.event.addListener(autocomplete, 'place_changed', function() {
                    var place = autocomplete.getPlace();
                    if (!place.geometry) {
                        return;
                    }

                    if (place.geometry.viewport && place.types[0] !== "locality") {
                        map.fitBounds(place.geometry.viewport);
                    } else {
                        map.panTo(place.geometry.location);
                        map.setZoom(BASE_MAP_ZOOM);
                    }

                    // Відрізаємо країну від адреса
                    $timeout(function() {
                        for (var i = 0; i < place.address_components.length; i++) {
                            for (var j = 0; j < place.address_components[i].types.length; j++) {
                                if (place.address_components[i].types[j] === "country" && place.address_components.length > 1) {
                                    var newAddress = cityInput.value.substring(0, cityInput.value.lastIndexOf(","));
                                    cityInput.value = newAddress;
                                    $scope.filters.map.c = newAddress;
                                    break;
                                } else {
                                    $scope.filters.map.c = place.formatted_address;
                                    break;
                                }
                            }
                        }
                    }, 0);

                    if(!$scope.$$phase)
                        $scope.$apply();

                    FiltersFactory.updateUrlFromFilters($scope.filters.map);
                });
            });
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
         * Функція яка ініціює загрузку даних
         */
        function loadData(timeout) {
            $timeout(function() {
                if (!LoadedValues.map.loaded) {
                    return;
                }

                var formattedViewport = FiltersFactory.getFormattedViewport(),
                    zoom = $scope.filters.map.z;

                if (timeout) {
                    clearTimeout(requestTimeout);
                    requestTimeout = setTimeout(function() {
                        MarkersFactory.load($scope.filters.red, $scope.filters.blue, $scope.filters.green,
                            $scope.filters.yellow,  formattedViewport, zoom, function(data) {

                            markers = data;
                            placeMarkers(data);
                        });
                    }, requestTimeoutTime);
                } else {
                    MarkersFactory.load($scope.filters.red, $scope.filters.blue, $scope.filters.green,
                        $scope.filters.yellow, formattedViewport, zoom, function(data) {

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

                                if (marker1.type !== "pie-marker")
                                    google.maps.event.addListener(marker1, 'click', function() {
                                        $location.path("/publication/" + marker1.tid + ":" + marker1.id);

                                        if (!$scope.$$phase)
                                            $scope.$apply();
                                    });
                                else {
                                    google.maps.event.addListener(marker1, 'click', function(e) {
                                        map.setZoom(map.getZoom() + 1);
                                        map.setCenter(marker1.getPosition());
                                    });
                                }
                            })();
                        }
                    }
                }
            }
        }

    }
]);