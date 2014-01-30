'use strict';

app.controller('AppCtrl', function($scope, $rootScope, $routeParams) {


    /**
     * Колекція типів оголошення
     **/
    $rootScope.publicationTypes = [
        { name: "house",     id: 0,  title: "Дома" },
        { name: "flat",      id: 1,  title: "Квартиры" },
        { name: "apartments",id: 2,  title: "Аппартаменты" },
        { name: "dacha",     id: 3,  title: "Дачи" },
        { name: "cottage",   id: 4,  title: "Коттеджы" },
        { name: "room",      id: 5,  title: "Комнаты" },
        { name: "trade",     id: 6,  title: "Торговые помещения" },
        { name: "office",    id: 7,  title: "Офисы" },
        { name: "warehouse", id: 8,  title: "Склады" },
        { name: "business",  id: 9,  title: "Готовый бизнес" },
        { name: "catering",  id: 10, title: "Обьекты общепита" },
        { name: "garage",    id: 11, title: "Гаражы" },
        { name: "land",      id: 12, title: "Земельные участки" }
    ];

    /**
     * Перегляд за зміною урла для встановлення активного
     * пункту меню
     **/
    $scope.$on("$routeChangeSuccess", function() {
        $rootScope.routeSection  = "";
        $rootScope.publicationId = "";

        if ($routeParams.section)
            $rootScope.routeSection = $routeParams.section;

        if ($routeParams.pubId)
            $rootScope.publicationId = $routeParams.pubId;
    });
});