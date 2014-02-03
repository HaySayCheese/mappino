'use strict';

app.controller('SidebarItemDetailedCtrl', function($scope, $rootScope, $timeout, $compile, $routeParams, publicationQueries, Briefs, Tags) {

    initScrollBar();

    $scope.publication = "";
    $scope.tags = Tags.getTags();





    /**
     * При зміні урла генерить урл для темплейта
     **/
    $scope.$on("$routeChangeSuccess", function() {
        if (Briefs.isUnpublished($rootScope.publicationId.split(":")[1]) && $rootScope.publicationId)
            loadPublicationData();
    });
    $rootScope.$watch("briefsLoaded", function(loaded) {
        if (loaded && $rootScope.publicationId)
            loadPublicationData();
    });


    /**
     * Функція загрузки даних по оголошенню
     **/
    function loadPublicationData() {
        var type = $rootScope.routeSection,
            tid = $rootScope.publicationId.split(":")[0],
            hid = $rootScope.publicationId.split(":")[1];

        $rootScope.loadings.detailed = true;

        publicationQueries.loadPublication(type, tid, hid).success(function(data) {
            $scope.publication = data;

            $scope.publicationLoaded = true;
            $scope.publicationTemplateUrl = "/ajax/template/cabinet/publications/" + $rootScope.publicationId.split(":")[0] + "/";

            $timeout(function() {
                angular.element("select").selectpicker({
                    style: 'btn-default btn-md'
                });

                $rootScope.loadings.detailed = false;
                $scope.showPublication = true;

                inputChangeInit();
                mapInit();
            }, 200);
        });
    }


    /**
     * При втраті фокуса з інпута
     * викликати запит на відправку на сервер
     **/
    function inputChangeInit() {
        angular.element(".sidebar-item-detailed-body input, textarea").bind("focusout", function(e) {
            var name = e.currentTarget.name.replace("h_", ""),
                value =  e.currentTarget.value;

            sendToServerInputData(name, value, function(newValue) {
                if (newValue)
                    e.currentTarget.value = newValue
            });
        });

        angular.element(".sidebar-item-detailed-body input[type='checkbox']").bind("change", function(e) {
            var name = e.currentTarget.name.replace("h_", ""),
                value =  e.currentTarget.checked;

            sendToServerInputData(name, value);
        });

        angular.element(".sidebar-item-detailed-body select").bind("change", function(e) {
            var name = e.currentTarget.name.replace("h_", ""),
                value =  e.currentTarget.value;

            sendToServerInputData(name, value);
        });
    }


    /**
     * Відправка даних полів на сервер
     **/
    function sendToServerInputData(name, value, callback) {
        var type = $rootScope.routeSection,
            tid = $rootScope.publicationId.split(":")[0],
            hid = $rootScope.publicationId.split(":")[1];

        console.log(name + " - " + value);

        publicationQueries.checkInputs(type, tid, hid, { f: name, v: value })
        .success(function(data) {
            console.log(data);

            if (data.value)
                callback(data.value);
        });
    }


    /**
     * Ініціалізація карти
     **/
    function mapInit() {
        var cityInput = document.getElementById("publication-map-input"),
            center = new google.maps.LatLng(50.448159, 30.524654),
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
            }
        });
    }


    /**
     * Ставить в інпут адрес з координат
     **/
    function setAddressFromLatLng(latLng, input) {
        var geocoder = new google.maps.Geocoder();

        geocoder.geocode({ 'latLng': latLng }, function(results, status) {
            if(status == google.maps.GeocoderStatus.OK)
                input.value = results[0].formatted_address;
        });
    }


    /**
     * Функція скролбара
     **/
    function initScrollBar() {
        var sidebar = angular.element(".sidebar-item-detailed-body");

        sidebar.perfectScrollbar({
            wheelSpeed: 40
        });

        angular.element(window).resize(function() {
            sidebar.perfectScrollbar("update");
        });
    }
});