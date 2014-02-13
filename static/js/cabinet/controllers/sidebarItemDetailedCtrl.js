'use strict';

app.controller('SidebarItemDetailedCtrl', function($scope, $rootScope, $timeout, $compile, $routeParams, Publication, Briefs, Tags) {

    initScrollBar();

    $scope.publicationSections = [];
    $scope.publication = [];
    $scope.tags = Tags.getAll();
    $scope.form = {};

    var tid, hid;


    /**
     * При зміні урла грузить дані оголошення
     */
    $scope.$on("$routeChangeSuccess", function() {
        tid = $rootScope.publicationId.split(":")[0];
        hid = $rootScope.publicationId.split(":")[1];

        loadPublicationData();
    });


    /**
     * Ловим евент зміни тегів
     */
    $scope.$on("tagsUpdated", function() {
        $scope.tags = Tags.getAll();
    });


    /**
     * Змінюємо пункти дропдауна ярликів в залежності від чекбоксів
     * оренди і продажу
     */
    $scope.$watch("publication.head.for_sale", function() {
        initSectionDropdown();
    });
    $scope.$watch("publication.head.for_rent", function() {
        initSectionDropdown();
    });


    /**
     * Функція загрузки даних по неопублікованому оголошенню
     */
    function loadPublicationData() {
        if (!$rootScope.publicationId)
            return;

        $scope.publication = [];
        $rootScope.loadings.detailed = true;


        Publication.load(tid, hid, function(data) {
            $scope.publication = data;

            console.log(data);

            checkSaleOrRentObject();

            $scope.publicationLoaded = true;

            // якщо оголошення неопубліковане
            if (!data.head.actual) {
                $scope.publicationTemplateUrl = "/ajax/template/cabinet/publications/" + tid + "/";

                $timeout(function() {
                    // Послідовність має значення
                    initInputsChange();
                    initDropdowns();
                    initSectionDropdown();

                    $rootScope.loadings.detailed = false;
                    $scope.showPublication = true;

                    $timeout(function() {
                        initMap();
                        initScrollBar();
                    }, 50);
                }, 200);
            } else {
                $scope.publicationTemplateUrl = "/ajax/template/cabinet/published/" + tid + "/";
            }
        });
    }


    /**
     * Встановлення параметрів для пустих обєктів
     */
    function checkSaleOrRentObject() {
        if (!$scope.publication.sale_terms) {
            $scope.publication.sale_terms = {
                add_terms:      "",
                currency_sid:   0,
                is_contract:    false,
                price:          null,
                sale_type_sid:  0,
                transaction_sid: 0
            }
        }

        if (!$scope.publication.rent_terms) {
            $scope.publication.rent_terms = {
                add_terms:      "",
                conditioner:    false,
                currency_sid:   0,
                family:         false,
                foreigners:     false,
                furniture:      false,
                home_theater:   false,
                is_contract:    false,
                period_sid:     1,
                persons_count:  null,
                pets:           false,
                price:          null,
                refrigerator:   false,
                rent_type_sid:  0,
                smoking:        false,
                tv:             false,
                washing_machine: false
            }
        }
    }


    /**
     * При втраті фокуса з інпута
     * викликати запит на відправку на сервер
     */
    function initInputsChange() {
        // Інпути і текстові поля
        angular.element(".sidebar-item-detailed-body input[type='text'], textarea").bind("focusout", function(e) {
            var name  = e.currentTarget.name,
                value = e.currentTarget.value.replace(/\s/g, "");

            if (!$scope.form.publication[name].$dirty)
                return;

            Publication.checkInputs(tid, hid, { f: name, v: value }, function(newValue, code) {
                if (newValue)
                    e.currentTarget.value = newValue;

                $scope.form.publication[name].$setValidity("incorrect", code === 0);
            });

        });

        // Чекбокси кроме чекбоксів тегів
        angular.element(".sidebar-item-detailed-body input[type='checkbox'][name!='tag']").bind("change", function(e) {
            var name  = e.currentTarget.name,
                value = e.currentTarget.checked;

            Publication.checkInputs(tid, hid, { f: name, v: value });
        });

        // Дропдауни
        angular.element(".sidebar-item-detailed-body select").bind('change',function(e) {
            var name  = e.currentTarget.name,
                value = e.currentTarget.value;

            Publication.checkInputs(tid, hid, { f: name, v: value });
        });
    }


    /**
     * Клік по чекбоксу тега
     */
    $scope.tagCheckboxChange = function(e) {
        var id    = e.currentTarget.id,
            name  = e.currentTarget.name,
            value = e.currentTarget.checked;

        Publication.checkInputs(tid, hid, { f: name, v: id + "," + value });
    };


    /**
     * Ініціалізація карти
     */
    function initMap() {

        var cityInput = document.getElementById("publication-map-input"),
            center = new google.maps.LatLng($scope.publication.head.lat || 50.448159, $scope.publication.head.lng || 30.524654),
            // Опції карти
            mapOptions = {
                center: center,
                zoom: $scope.publication.head.lat ? 17 : 8,
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                mapTypeControl: false,
                streetViewControl: false
            },
            // Карта
            map = new google.maps.Map(document.getElementById("publication-map"), mapOptions),
            // Автокомпліт
            autocompleteOptions = {
                componentRestrictions: {
                    country: "ua"
                }
            },
            autocomplete = new google.maps.places.Autocomplete(cityInput, autocompleteOptions),
            // Маркер
            marker = new google.maps.Marker({
                map: map,
                draggable: true,
                position: center
            });

        autocomplete.bindTo('bounds', map);

        // Спроба взяти координати з геолокації користувача
        if(navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                var pos = new google.maps.LatLng(position.coords.latitude,
                    position.coords.longitude);

                map.setCenter(pos);
                marker.setPosition(pos);
                setAddressFromLatLng(pos, cityInput);
            });
        }

        // Евенти
        google.maps.event.addListener(map, 'click', function(e) {
            marker.setPosition(e.latLng);
            setAddressFromLatLng(e.latLng, cityInput);
        });
        google.maps.event.addListener(marker, 'dragend', function(e) {
            setAddressFromLatLng(e.latLng, cityInput);
        });
        google.maps.event.addListener(autocomplete, 'place_changed', function() {
            var place = autocomplete.getPlace();

            if (!place.geometry)
                return;

            if (place.geometry.viewport) {
                map.fitBounds(place.geometry.viewport);
            } else {
                map.panTo(place.geometry.location);
                marker.setPosition(place.geometry.location);
                map.setZoom(17);
                setAddressFromLatLng(place.geometry.location, cityInput);
            }
        });
    }


    /**
     * Ставить в інпут адрес з координат
     */
    function setAddressFromLatLng(latLng, input) {
        var geocoder = new google.maps.Geocoder();

        geocoder.geocode({ 'latLng': latLng }, function(results, status) {
            if(status == google.maps.GeocoderStatus.OK)
                input.value = results[0].formatted_address;

            angular.element(input).trigger("input");

            Publication.checkInputs(tid, hid, { f: "address", v: input.value });
            Publication.checkInputs(tid, hid, { f: "lat_lng", v: latLng.d + ";" + latLng.e });
        });
    }


    /**
     * Ініціалізація області загрузки зображень
     */
    $scope.multipleSelect = function() {
        $timeout(function() {
            angular.element("input[type='file']").trigger("click");
        }, 0);

    };


    /**
     * Логіка загрузки зображень
     */
    $scope.onFileSelect = function(files) {

        !$scope.publication.photos && ($scope.publication.photos = []);

        for (var i = 0; i < files.length; i++) {
            Publication.uploadPhotos(tid, hid, files[i], function(data) {
                $scope.publication.photos.push(data.image);
            });
        }
    };


    /**
     * Видалення зображень
     */
    $scope.removePhoto = function(photo) {
        Publication.removePhoto(tid, hid, photo.id, function(data) {
            console.log(data)
        })
    };


    /**
     * Публікація оголошення
     */
    $scope.publishPublication = function() {
        $scope.showValidationMessages = true;

        if ($scope.form.publication.$invalid) {
            var checkboxElement = angular.element("input[type='checkbox'].ng-invalid")[0],
                inputElement    = angular.element("textarea.ng-invalid, input.ng-invalid")[0];


            if (checkboxElement)
                checkboxElement.parentNode.scrollIntoView(true);
            else
                inputElement.scrollIntoView(true);

            return;
        }

        var btn = angular.element(".sidebar-item-detailed-body .btn-success").button("loading");

        Publication.publish(tid, hid, function(data) {
            btn.button("reset");
        })
    };


    /**
     * Скрол до розділа
     */
    $scope.scrollToHeader = function(id) {
        document.getElementById(id).scrollIntoView(true);
    };


    /**
     * Ініціалізація дропдаунів
     */
    function initDropdowns() {
        angular.element("select").selectpicker({
            style: 'btn-default btn-md'
        });
    }


    function initSectionDropdown() {
        $scope.publicationSections = [];

        angular.element("h3").each(function(i, e) {
            var header = angular.element(e)[0];

            $scope.publicationSections.push({
                href: header.id,
                title: header.textContent
            });
        });

        for (var i = 0; i < $scope.publicationSections.length; i++) {
            if ($scope.publicationSections[i].href === 'for-sale-section' && !$scope.publication.head.for_sale) {
                $scope.publicationSections.splice(i, 1);
            }

            if ($scope.publicationSections[i].href === 'for-rent-section' && !$scope.publication.head.for_rent) {
                $scope.publicationSections.splice(i, 1);
            }
        }
    }


    /**
     * Функція скролбара
     */
    function initScrollBar() {
        var sidebar = angular.element(".sidebar-item-detailed-body .detailed-container");

        sidebar.perfectScrollbar("destroy");

        sidebar.perfectScrollbar({
            wheelSpeed: 40,
            useKeyboard: false,
            suppressScrollX: true
        });

        angular.element(window).resize(function() {
            sidebar.perfectScrollbar("update");
        });
    }
});