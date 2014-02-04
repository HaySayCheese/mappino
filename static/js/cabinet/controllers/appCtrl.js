'use strict';

app.controller('AppCtrl', function($scope, $rootScope, $routeParams, $location) {


    /**
     * Колекція типів оголошення
     **/
    $rootScope.publicationTypes = [
        { name: "house",     id: 0,  title: "Дома" },
        { name: "flat",      id: 1,  title: "Квартиры" },
        { name: "apartments",id: 2,  title: "Аппартаментов" },
        { name: "dacha",     id: 3,  title: "Дачи" },
        { name: "cottage",   id: 4,  title: "Коттеджа" },
        { name: "room",      id: 5,  title: "Комнаты" },
        { name: "trade",     id: 6,  title: "Торгового помещения" },
        { name: "office",    id: 7,  title: "Офиса" },
        { name: "warehouse", id: 8,  title: "Склада" },
        { name: "business",  id: 9,  title: "Готового бизнеса" },
        { name: "catering",  id: 10, title: "Обьекта общепита" },
        { name: "garage",    id: 11, title: "Гаража" },
        { name: "land",      id: 12, title: "Земельного участка" }
    ];


    /**
     * Лоадери
     **/
    $rootScope.loadings = {
        tags: false,
        briefs: false,
        detailed: false
    };


    /**
     * Перегляд за зміною урла для встановлення активного
     * пункту меню
     **/
    $scope.$on("$routeChangeSuccess", function() {
        $rootScope.routeBase     = "";
        $rootScope.routeSection  = "";
        $rootScope.publicationId = "";

        if ($location.path().replace("/", ""))
            $rootScope.routeBase = $location.path().replace("/", "");

        if ($routeParams.section)
            $rootScope.routeSection = $routeParams.section;

        if ($routeParams.pubId)
            $rootScope.publicationId = $routeParams.pubId;
    });
});