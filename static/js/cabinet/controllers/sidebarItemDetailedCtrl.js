'use strict';

app.controller('SidebarItemDetailedCtrl', function($scope, $rootScope, $timeout, $compile, $routeParams, publicationQueries, Briefs, Tags, $upload) {

    initScrollBar();

    $scope.publication = "";
    $scope.tags = Tags.getAll();

    var tid, hid;

    /**
     * При зміні урла грузить дані оголошення
     */
    $scope.$on("$routeChangeSuccess", function() {
        tid = $rootScope.publicationId.split(":")[0];
        hid = $rootScope.publicationId.split(":")[1];

        if (Briefs.isUnpublished($rootScope.publicationId.split(":")[1]) && $rootScope.publicationId)
            loadUnpublishedPublicationData();
    });
    $rootScope.$watch("briefsLoaded", function(loaded) {
        tid = $rootScope.publicationId.split(":")[0];
        hid = $rootScope.publicationId.split(":")[1];

        if (loaded && $rootScope.publicationId && Briefs.isUnpublished($rootScope.publicationId.split(":")[1]))
            loadUnpublishedPublicationData();
    });


    /**
     * Функція загрузки даних по неопублікованому оголошенню
     */
    function loadUnpublishedPublicationData() {
        var type = $rootScope.routeSection;

        $scope.publication = "";
        $rootScope.loadings.detailed = true;


        publicationQueries.loadPublication(type, tid, hid).success(function(data) {
            $scope.publication = data;

            $scope.publicationLoaded = true;
            $scope.publicationTemplateUrl = "/ajax/template/cabinet/publications/" + $rootScope.publicationId.split(":")[0] + "/";

            $timeout(function() {
                inputChangeInit();

                angular.element("select").selectpicker({
                    style: 'btn-default btn-md'
                });

                $rootScope.loadings.detailed = false;
                $scope.showPublication = true;

                mapInit();
            }, 200);
        });
    }


    /**
     * При втраті фокуса з інпута
     * викликати запит на відправку на сервер
     */
    function inputChangeInit() {
        angular.element(".sidebar-item-detailed-body input[type='text'], textarea").bind("focusout", function(e) {
            var name = e.currentTarget.name.replace("h_", ""),
                value =  e.currentTarget.value;

            sendToServerInputData(name, value, function(newValue) {
                if (newValue)
                    e.currentTarget.value = newValue;

                if (name == "title")
                    Briefs.updateBriefOfPublication(tid, hid, name, newValue ? newValue : value);
            });
        });

        angular.element(".sidebar-item-detailed-body input[type='checkbox']").bind("change", function(e) {
            var name = e.currentTarget.name.replace("h_", ""),
                value =  e.currentTarget.checked;

            if (name == "for_rent" || name == "for_sale")
                Briefs.updateBriefOfPublication(tid, hid, name, value);

            sendToServerInputData(name, value);
        });

        angular.element(".sidebar-item-detailed-body select").bind('change',function(e) {
            var name = e.currentTarget.name.replace("h_", ""),
                value =  e.currentTarget.value;

            sendToServerInputData(name, value);
        });
    }


    /**
     * Відправка даних полів на сервер
     */
    function sendToServerInputData(name, value, callback) {
        var type = $rootScope.routeSection;

        publicationQueries.checkInputs(type, tid, hid, { f: name, v: value }).success(function(data) {
            if (data.value)
                callback(data.value);
        });
    }


    /**
     * Ініціалізація карти
     */
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
     */
    function setAddressFromLatLng(latLng, input) {
        var geocoder = new google.maps.Geocoder();

        geocoder.geocode({ 'latLng': latLng }, function(results, status) {
            if(status == google.maps.GeocoderStatus.OK)
                input.value = results[0].formatted_address;
        });
    }


    /**
     * Ініціалізація області загрузки зображень
     */
    $scope.multipleSelect = function() {
        $timeout(function() {
            angular.element(".image-upload-block input[type='file']").click();
        }, 0);

    };
    $scope.onFileSelect = function(files) {
        $scope.publication.head.photos = [];

        for (var i = 0; i < files.length; i++) {
            $scope.publication.head.photos.push(files[i]);

            console.log($scope.publication.head.photos)
        }
    };


    /**
     * Функція скролбара
     */
    function initScrollBar() {
        var sidebar = angular.element(".sidebar-item-detailed-body");

        sidebar.perfectScrollbar("update");
        sidebar.perfectScrollbar({
            wheelSpeed: 40,
            useKeyboard: false
        });
        angular.element(window).resize(function() {
            sidebar.perfectScrollbar("update");
        });
    }
});