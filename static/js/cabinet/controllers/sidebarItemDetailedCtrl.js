'use strict';

app.controller('SidebarItemDetailedCtrl', function($scope, $rootScope, $timeout, $compile, $routeParams, Publication, Briefs, Tags) {

    initScrollBar();

    $scope.publicationSections = [];
    $scope.publication = [];
    $scope.tags = Tags.getAll();

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
     * При загрузці тегів оновлює їх масив для дд
     */
    $rootScope.$watch("loadings.tags", function() {
        $scope.tags = Tags.getAll();
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
                $scope.publicationTemplateUrl = "/ajax/template/cabinet/publications/" + tid + "/";

                $timeout(function() {
                    // Послідовність має значення
                    initInputsChange();
                    initDropdowns();

                    $rootScope.loadings.detailed = false;
                    $scope.showPublication = true;

                    $timeout(function() {
                        initMap();
                        initScrollBar();
                    }, 50);
                }, 200);
            } else {
                console.log("actual")
            }
        });
    }


    /**
     * При втраті фокуса з інпута
     * викликати запит на відправку на сервер
     */
    function initInputsChange() {
        angular.element(".sidebar-item-detailed-header select[name='tags-select']").bind('change',function(e) {
            var name = e.currentTarget.name;

            Publication.checkInputs(tid, hid, { f: name, v: $scope.publication.tags });
        });

        angular.element(".sidebar-item-detailed-body input[type='text'], textarea").bind("focusout", function(e) {
            var name = e.currentTarget.name,
                value =  e.currentTarget.value;

            Publication.checkInputs(tid, hid, { f: name, v: value }, function(newValue) {
                if (newValue)
                    e.currentTarget.value = newValue;
            });
        });

        angular.element(".sidebar-item-detailed-body input[type='checkbox']").bind("change", function(e) {
            var name = e.currentTarget.name,
                value =  e.currentTarget.checked;

            Publication.checkInputs(tid, hid, { f: name, v: value });
        });

        angular.element(".sidebar-item-detailed-body select").bind('change',function(e) {
            var name = e.currentTarget.name,
                value =  e.currentTarget.value;

            Publication.checkInputs(tid, hid, { f: name, v: value });
        });
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
                zoom: 8,
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
        var btn = angular.element(".sidebar-item-detailed-body .btn-success").button("loading");

        Publication.publish(tid, hid, function(data) {
            btn.button("reset");
        })
    };


    /**
     * Скрол до розділа
     */
    $scope.scrollToHeader = function(href) {
        document.getElementById(href).scrollIntoView();
    };


    /**
     * Ініціалізація дропдауна
     */
    function initDropdowns() {
        angular.element("select").selectpicker({
            style: 'btn-default btn-md'
        });

        angular.element("h3").each(function(i, e) {
            var header = angular.element(e).context;
            $scope.publicationSections.push({
                href: header.id,
                title: header.innerText
            })
        })
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