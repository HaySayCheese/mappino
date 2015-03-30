app.controller('HomeController', ['$scope', '$timeout', '$http', '$cookies', 'base64', 'UserService',
    function($scope, $timeout, $http, $cookies, base64, UserService) {
        "use strict";

        UserService.checkIfLoginIn(function() {
            $scope.user = {
                name: UserService.getUserName()
            };
        });

        $scope.map = {
            zoom: 6,
            latLng: '48.455935,34.41285'
        };
        $scope.filters = {
            city:           '',
            type_sid:       0,
            period_sid:     null,
            operation_sid:  0
        };
        $scope.errors = {
            badRegion: false
        };

        var cityInput   = document.getElementById('home-location-autocomplete'),
            cityAutocomplete = new google.maps.places.Autocomplete(cityInput, {
                componentRestrictions: {
                    country: "ua"
                }
            }),
            geocoder = new google.maps.Geocoder();



        /**
         * autocomplete 'place_changed' event handler
         **/
        google.maps.event.addListener(cityAutocomplete, 'place_changed', function() {
            geocode(cityAutocomplete.getPlace());
        });



        /**
         * Дивимся за колекцією фільтрів
         *
         * Якщо вибрано оренду:
         *  - ставимо параметер з сроком оренди в посуточний
         * Якщо вибрано оренду і тип оголошення один з комерційних:
         *  - забираємо срок оренди
         **/
        $scope.$watchCollection('filters', function(_filters) {
            if (_filters.operation_sid === 2) {
                $scope.filters.period_sid = 1;
                if (_filters.type_sid > 2) {
                    $scope.filters.operation_sid = 1;
                }
            } else {
                $scope.filters.period_sid = null;
            }
        });



        /**
         * Підганяємо першу картінку на сторінці по висоті вікна
         **/
        $(window).on('resize', function() {
            if ($(window).height() > 500) {
                $('.img-holder.top').css('height', $(window).height() + 'px');
            }
        }).resize();


        /**
         * Анімація падаючих маркерів на планшет
         **/
        $(document).scroll(function() {
            var scrollTop = $(this).scrollTop();

            /** Markers */
            var sections = $("section"),
                markers = $(".tablet-marker");

            if (scrollTop > sections[1].offsetTop - 50) {
                $.each(markers, function(i, el) {
                    setTimeout(function() {
                        $(el).addClass("fadeInDown");
                    }, 300 + (i * 300));
                });
            }
        });



        /**
         * Логаут користувача
         **/
        $scope.logout = function(e) {
            UserService.logoutUser(function() {
                $scope.user = {
                    name: UserService.getUserName()
                };
            });
            event.preventDefault();
        };



        /**
         * Встановлення регіона в поле пошуку з підсказок
         **/
        $scope.setRegion = function(region) {
            geocode(region);
        };



        /**
         * Формування фільтрів в урл та переадресація на сторінку пошука
         **/
        // todo: need fix
        $scope.search = function() {
            geocode($scope.filters.city);

            if ((!$scope.map.latLng && !localStorage._tempViewportFromHomePage) || !$scope.filters.city) {
                $scope.errors.badRegion = true;
                return false;
            } else {
                var path = "map/#!/" + ($scope.map.latLng ? $scope.map.latLng + "/" + $scope.map.zoom : '48.455935,34.41285/6') + "/search/?";
                var searchString = "c=" + $scope.filters.city +
                    "&r_t_sid="  + $scope.filters.type_sid +
                    "&r_op_sid=" + ($scope.filters.operation_sid === 2 ? 1 : $scope.filters.operation_sid);

                if ($scope.filters.period_sid) {
                    searchString += "&r_pr_sid=" + $scope.filters.period_sid;
                }

                window.location = window.location.href + path + base64.urlencode(searchString);
            }
        };



        $scope.scrollTo = function(to) {
            $("html, body").animate({
                scrollTop: to === 'top' ? 0 : $(window).height()
            }, '500');
            event.preventDefault();
        };



        /**
         * Геокодування адреси в координати
         *
         * Використовується для перевірки наявності введеного
         * користувачем міста
         **/
        function geocode(place) {
            if (place.formatted_address) {
                place = place.formatted_address;
            }

            geocoder.geocode({ 'address': place }, function(results, status) {
                if (status === google.maps.GeocoderStatus.OK) {
                    if (results[0].geometry.viewport && results[0].types[0] !== "locality") {
                        localStorage._tempViewportFromHomePage = results[0].geometry.viewport.toString();
                    } else {
                        $scope.map.latLng = results[0].geometry.location.lat() + "," + results[0].geometry.location.lng();
                        delete localStorage._tempViewportFromHomePage;
                    }
                    $scope.filters.city = results[0].formatted_address;
                    $scope.errors.badRegion = false;

                    if (!$scope.$$phase) {
                        $scope.$apply();
                    }
                } else {
                    $scope.errors.badRegion = true;
                }
            });
        }
    }
]);