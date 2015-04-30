'use strict';

app.controller('SidebarItemDetailedCtrl', function($scope, $rootScope, $timeout, $location, $compile, $routeParams, Publication, Briefs, Tags, Settings) {

    $scope.publicationSections = [];
    $scope.publication = [];
    $scope.publicationChartData = [];
    $scope.tags = Tags.getAll();
    $scope.form = {};

    var tid, hid, isPublished = false, map;

    /**
     * При зміні урла грузить дані оголошення
     */
    $scope.$on("$routeChangeSuccess", function() {
        tid = $rootScope.publicationId.split(":")[0];
        hid = $rootScope.publicationId.split(":")[1];

        angular.element('body > #photosModal').remove();

        loadPublicationData();
    });


    /**
     * Ловим евент зміни тегів
     */
    $rootScope.$on("tagsUpdated", function() {
        $scope.tags = Tags.getAll();

        initSectionDropdown();
    });



    $scope.moveToBody = function() {
        angular.element('#photosModal').appendTo("body");
    };

    /**
     * Змінюємо пункти дропдауна ярликів в залежності від чекбоксів
     * оренди і продажу
     */
    $scope.$watch("publication.head.for_sale", function() {
        $timeout(function() {
            initSectionDropdown();
        }, 100);
    });
    $scope.$watch("publication.head.for_rent", function() {
        $timeout(function() {
            initSectionDropdown();
        }, 100);
    });


    /**
     * Функція загрузки даних по оголошенню
     */
    function loadPublicationData() {
        if (!$rootScope.publicationId)
            return;

        $scope.publication = [];
        $rootScope.loadings.detailed = true;

        Publication.load(tid, hid, function(data) {
            $scope.publication = data;

            if (data.head.state_sid !== 1) {
                isPublished = true;
                loadChartData();
                $scope.publicationLoaded = true;
                $scope.publicationTemplateUrl = "/ajax/template/cabinet/publications/published/";
            } else {
                isPublished = false;
                $scope.publicationLoaded = true;
                $scope.publicationTemplateUrl = "/ajax/template/cabinet/publications/unpublished/" + tid + "/";
            }
        });
    }

    /**
     * Функція загрузки даних для графіків
     */
    function loadChartData() {
        $scope.chartLoaded = false;
        $rootScope.loadings.chartData = true;

        Publication.loadChartData(tid, hid, function(data) {
            $scope.publicationChartData = data;
            $scope.chartLoaded = true;
            $rootScope.loadings.chartData = false;
            initChart();
        });
    }


    /**
     * Ініціюється при інклуді хтмл файла
     */
    $scope.initLoadFormScripts = function() {
        // якщо неопубліковане
        !isPublished && $timeout(function() {
            // Послідовність має значення
            initInputsChange();
            initDropdowns();
            initSectionDropdown();

            $rootScope.loadings.detailed = false;
            $scope.showPublication = true;

            $timeout(function() {
                initScrollBar();
            }, 300);
        }, 300);


        // якщо опубліковане
        isPublished && $timeout(function() {
            initSectionDropdown();

            $rootScope.loadings.detailed = false;
            $scope.showPublication = true;

            //initChart();

            $timeout(function() {
                initScrollBar();
            }, 300);
        }, 0);
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
                if (newValue && !angular.element(e.currentTarget).is(":focus")) {
                    e.currentTarget.value = newValue;

                    $scope.form.publication[name].$setValidity("incorrect", code === 0);
                }
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
    function initChart() {
        var areaChart = {};
        areaChart.type = "AreaChart";

        areaChart.data = {
            "cols": [
                {
                    "id": "month",
                    "label": "Месяц",
                    "type": "date"
                }, {
                    "id": "views",
                    "label": "Просмотров",
                    "type": "number"
                }, {
                    "id": "contacts_requests",
                    "label": "Запросили контакты",
                    "type": "number"
                }
            ],
            "rows": $scope.publicationChartData
        };

        areaChart.options = {
            chartArea: {
                width: "94%",
                top: 20
            },
            height: 300,

            legend: {
                position: 'bottom'
            },
            focusTarget: 'category',
            displayExactValues: true,

            series: {
                0: { color: '#3db1d7' },
                1: { color: '#54c6a7' }
            },

            lineWidth: 4,
            pointSize: 8,

            hAxis: {
                format : "dd.MM",
                gridlines: {
                    color: "#eee"
                },
                baselineColor: '#eee',
                textColor: '#999'
            },
            vAxis: {
                format: '0',
                gridlines: {
                    color: "#eee",
                    count: -1
                },
                baselineColor: '#eee',
                textColor: '#999'
            }

        };

        areaChart.formatters = {
            number : [{
                columnNum: 2,
                pattern: "# чел'.'"
            }]
        };

        $scope.areaChart = areaChart;
    }


    /**
     * Ініціалізація карти
     */
    $scope.initMap = function() {

        var cityInput = document.getElementById("publication-map-input"),
            center = new google.maps.LatLng($scope.publication.head.lat || 50.448159, $scope.publication.head.lng || 30.524654),
            // Опції карти
            mapOptions = {
                center: center,
                zoom: $scope.publication.head.lat ? 17 : 8,
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                mapTypeControl: false,
                streetViewControl: false,
                scrollwheel: true,
                disableDoubleClickZoom: false
            },
            // Автокомпліт
            autocompleteOptions = {
                componentRestrictions: {
                    country: "ua"
                }
            },
            autocomplete = new google.maps.places.Autocomplete(cityInput, autocompleteOptions);

        map = new google.maps.Map(document.getElementById("publication-map"), mapOptions);

        var marker = new google.maps.Marker({
            map: map,
            draggable: true,
            position: center,
            icon: '/static/img/markers/red-normal.png'
        });

        autocomplete.bindTo('bounds', map);

        // Евенти
        google.maps.event.addListener(map, 'click', function(e) {
            setTimeout(function() {
                marker.setPosition(e.latLng);
                setAddressFromLatLng(e.latLng, cityInput);
            }, 500)
        });
        google.maps.event.addListener(map, 'dblclick', function(event) {
            map.setZoom(map.getZoom() + 1);
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


        google.maps.event.addListenerOnce(map, 'idle', function(e) {
            $timeout(function() {
                var latLng = new google.maps.LatLng($scope.publication.head.lat || 50.448159, $scope.publication.head.lng || 30.524654);
                map.setCenter(latLng);
                Publication.checkInputs(tid, hid, { f: "lat_lng", v: latLng.lat() + ";" + latLng.lng() }, null);
            }, 1000);
        });


        $timeout(function() {
            google.maps.event.trigger(map, "resize");
        }, 500);
    };


    /**
     * Ставить в інпут адрес з координат
     */
    function setAddressFromLatLng(latLng, input) {
        var geocoder = new google.maps.Geocoder();

        geocoder.geocode({ 'latLng': latLng }, function(results, status) {
            if(status == google.maps.GeocoderStatus.OK)
                input.value = results[0].formatted_address;

            angular.element(input).trigger("input");

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

        $rootScope.loadings.uploadPhotos = true;

        for (var i = 0; i < files.length; i++) {
            Publication.uploadPhotos(tid, hid, files[i], function(data) {
                $rootScope.loadings.uploadPhotos = false;

                initScrollBar();

                Briefs.updateBriefOfPublication(tid, hid, "photo_url", data.title_url);
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
     * Видалення зображень
     */
    $scope.setMainPhoto = function(photo) {
        Publication.setMainPhoto(tid, hid, photo.id);
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
     * Зняття оголошення з опублікованих
     */
    $scope.unpublishPublication = function() {
        var btn = angular.element(".publish-btn").button("loading");

        Publication.unpublish(tid, hid, function(data) {
            btn.button("reset");
        });
    };


    /**
     * Перенесення оголошення в корзину
     */
    $scope.toTrashPublication = function() {
        var btn = angular.element(".remove-btn").button("loading");

        Publication.toTrash(tid, hid, function(data) {
            btn.button("reset");
            Briefs.remove(tid, hid);
        });
    };


    /**
     * Видалення оголошення
     */
    $scope.removePublication = function() {
        var btn = angular.element(".remove-btn").button("loading");

        Publication.remove(tid, hid, function(data) {
            btn.button("reset");
            Briefs.remove(tid, hid);
        });
    };


    /**
     * Переміщення оголошення в неопубліковані з корзини
     */
    $scope.toUnpublishedPublication = function() {
        var btn = angular.element(".publish-btn").button("loading");

        Publication.toUnpublished(tid, hid, function(data) {
            btn.button("reset");
        });
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


    /**
     * Ініціалізація дропдаунів в хедері контента
     */
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
            if ($scope.publicationSections[i].href === 'for-sale-section' && !$scope.publication.head.for_sale)
                $scope.publicationSections.splice(i, 1);

            if ($scope.publicationSections[i].href === 'for-rent-section' && !$scope.publication.head.for_rent)
                $scope.publicationSections.splice(i, 1);

            if ($scope.publicationSections[i].href === 'pub-tags-section' && $scope.tags.length < 1)
                $scope.publicationSections.splice(i, 1);
        }
    }


    /**
     * Ініціалізація скролбара
     */
    function initScrollBar() {
        var sidebar = angular.element(".sidebar-item-detailed-body .detailed-container");

        sidebar.perfectScrollbar("destroy");

        sidebar.perfectScrollbar({
            wheelSpeed: 10,
            useKeyboard: false,
            suppressScrollX: true
        });

        angular.element(window).resize(function() {
            sidebar.perfectScrollbar("update");
        });
    }
});