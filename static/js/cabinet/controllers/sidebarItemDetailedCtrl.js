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
    $rootScope.$on("tagsUpdated", function() {
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

            $scope.publicationLoaded = true;

            // якщо оголошення неопубліковане
            if (!data.head.actual) {
                $scope.publicationTemplateUrl = "/ajax/template/cabinet/publications/unpublished/" + tid + "/";
            } else {
                $scope.publicationTemplateUrl = "/ajax/template/cabinet/publications/published/";
            }
        });
    }


    /**
     * Ініціюється при інклуді хтмл файла
     */
    $scope.initLoadFormScripts = function() {
        $timeout(function() {
            // Послідовність має значення
            initInputsChange();
            initDropdowns();
            initSectionDropdown();

            $rootScope.loadings.detailed = false;
            $scope.showPublication = true;

            $timeout(function() {
                !$scope.publication.head.actual && initMap();
                $scope.publication.head.actual && initCharts();
                initScrollBar();
            }, 300);
        }, 500);
    };





    /**
     * При втраті фокуса з інпута
     * викликати запит на відправку на сервер
     */
    function initInputsChange() {
        // Інпути і текстові поля
        angular.element(".sidebar-item-detailed-body input[type='text'], textarea").bind("focusout", function(e) {
            var name  = e.currentTarget.name,
                value = e.currentTarget.value.replace(/\s+/g, " ");

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

            Publication.checkInputs(tid, hid, { f: name, v: value }, null);
        });

        // Дропдауни
        angular.element(".sidebar-item-detailed-body select").bind('change',function(e) {
            var name  = e.currentTarget.name,
                value = e.currentTarget.value;

            Publication.checkInputs(tid, hid, { f: name, v: value }, null);
        });
    }


    /**
     * Клік по чекбоксу тега
     */
    $scope.tagCheckboxChange = function(e) {
        var id    = e.currentTarget.id,
            name  = e.currentTarget.name,
            value = e.currentTarget.checked;

        Publication.checkInputs(tid, hid, { f: name, v: id + "," + value }, null);
    };


    /**
     * Ініціалізація графіків
     */
    function initCharts() {
        var lineChart = {};
        lineChart.type = "LineChart";

        lineChart.data = {
            "cols": [
                {
                    "id": "month",
                    "label": "Месяц",
                    "type": "date"
                }, {
                    "id": "views",
                    "label": "Просмотров",
                    "type": "number"
                }
            ],
            "rows": [
                {
                    "c": [
                        {
                            "v": new Date(2014, 5, 18)
                        }, {
                            "v": 0
                        }
                    ]
                }, {
                    "c": [
                        {
                            "v": new Date(2014, 5, 19)
                        }, {
                            "v": 10
                        }
                    ]
                }, {
                    "c": [
                        {
                            "v": new Date(2014, 5, 20)
                        }, {
                            "v": 2
                        }
                    ]
                }, {
                    "c": [
                        {
                            "v": new Date(2014, 5, 21)
                        }, {
                            "v": 3
                        }
                    ]
                }, {
                    "c": [
                        {
                            "v": new Date(2014, 5, 22)
                        }, {
                            "v": 6
                        }
                    ]
                }, {
                    "c": [
                        {
                            "v": new Date(2014, 5, 23)
                        }, {
                            "v": 1
                        }
                    ]
                }
            ]
        };

        lineChart.options = {
            chartArea: {
                width: "94%",
                top: 20
            },
            height: 300,

            isStacked: "true",
            legend: 'none',
            displayExactValues: true,

            series: {
                0: { color: '#318ce1' }
            },

            smoothLine: true,
            lineWidth: 4,
            pointSize: 8,

            hAxis: {
                format : "dd.MM"
            }
        };

        $scope.lineChart = lineChart;
    }


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
                position: center,
                icon: 'http://127.0.0.1/mappino_static/img/markers/red-normal.png'
            });

        autocomplete.bindTo('bounds', map);

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

            console.log(latLng)

            Publication.checkInputs(tid, hid, { f: "address", v: input.value }, null);
            Publication.checkInputs(tid, hid, { f: "lat_lng", v: latLng.lat() + ";" + latLng.lng() }, null);
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
        Publication.removePhoto(tid, hid, photo.id);
    };


    /**
     * Публікація оголошення
     */
    $scope.publishPublication = function() {
        $scope.showValidationMessages = true;

        if (!$scope.form.publication.$valid) {
            var checkboxElement = angular.element("input[type='checkbox'].ng-invalid")[0],
                inputElement    = angular.element("textarea.ng-invalid, input.ng-invalid")[0];

            if (checkboxElement)
                checkboxElement.parentNode.scrollIntoView(true);
            else {
                inputElement.scrollIntoView(true);
                inputElement.focus();
            }

            return;
        }

        var btn = angular.element(".publish-btn").button("loading");

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