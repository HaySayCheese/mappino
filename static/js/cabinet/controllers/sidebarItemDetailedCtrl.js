'use strict';

app.controller('SidebarItemDetailedCtrl', function($scope, $rootScope, $timeout, $compile, $routeParams, publicationQueries, Briefs) {

    initScrollBar();

    $scope.publication = "";

//    $scope.$watchCollection("publication.head", function(v) {
//        if (v)
//            console.log(v)
//    });
//    $scope.$watchCollection("publication.body", function(v) {
//        if (v)
//            console.log(v)
//    });
//    $scope.$watchCollection("publication.rent_terms", function(v) {
//        if (v)
//            console.log(v)
//    });
//    $scope.$watchCollection("publication.sale_terms", function(v) {
//        if (v)
//            console.log(v)
//    });


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
            $rootScope.loadings.detailed = false;
            $scope.publicationTemplateUrl = "/ajax/template/cabinet/publications/" + $rootScope.publicationId.split(":")[0] + "/";

            $timeout(function() {
                angular.element("select").selectpicker({
                    style: 'btn-default btn-md'
                });
                inputChangeInit();
            }, 200);
        });
    }


    function inputChangeInit() {
        angular.element("input, textarea").bind("focusout", function(e) {
            var name = e.currentTarget.name.replace("h_", ""),
                value =  e.currentTarget.value;

            sendToServerInputData(name, value, function(newValue) {
                if (newValue)
                    e.currentTarget.value = newValue
            });
        });

        angular.element("input[type='checkbox']").bind("change", function(e) {
            var name = e.currentTarget.name.replace("h_", ""),
                value =  e.currentTarget.checked;

            sendToServerInputData(name, value);
        });

        angular.element("select").bind("change", function(e) {
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
     * Функція скролбара
     **/
    function initScrollBar() {
        var sidebar = angular.element(".sidebar-item-detailed-body");

        sidebar.perfectScrollbar({
            wheelSpeed: 20
        });

        angular.element(window).resize(function() {
            sidebar.perfectScrollbar("update");
        });
    }
});