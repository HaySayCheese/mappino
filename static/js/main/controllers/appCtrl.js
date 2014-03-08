'use strict';

app.controller('AppCtrl', function($scope, $rootScope, $location, $cookies) {

    $rootScope.publicationTypes = [
        { name: "house",     id: 0,  title: "Дома",
            filters: [
                "operation_sid",    // Загальні
                "period_sid",       // Тільки в оренді
                "price_from", "price_to", "currency_sid", // Загальні
                "persons_count_from", "persons_count_to", // Тільки в оренді
                "new_buildings",    // Тільки в продажі
                "secondary_market",
                "family",           // Тільки в оренді
                "foreigners",
                "rooms_count_from", "rooms_count_to",     // Тільки в продажі
                "floors_count_from", "floors_count_to",
                "electricity", "hot_water",
                "gas", "cold_water",
                "sewerage",         // Тільки в продажі
                "heating_type_sid"
            ]},
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
     * При закритті діалога додає параметри пошука в урл
     **/
    angular.element(document).on('hidden.bs.modal', function (e) {

        angular.element("body").removeClass("modal-open");
        angular.element(".modal-backdrop").remove();

        $location.path("/search");

        if(!$scope.$$phase)
            $scope.$apply();
    });


    /**
     * Логіка підставлення в урл параметрів пошука
     **/
    $scope.$on("$routeChangeSuccess", function() {
        $scope.urlFiltersPart = $location.url().replace("/search", "");

        angular.element(".modal-backdrop").remove();
    });


    /**
     * Логіка унеможливлення переходу до реєстрації або логіну
     * якщо юзер уже залогінений
     **/
    $scope.$on("$locationChangeStart", function(event, next, current) {

        if (!$cookies.sessionid)
            return;

        if (next.indexOf("/account/registration") != -1 || next.indexOf("/account/login") != -1 || next.indexOf("/account/restore-access") != -1) {
            $location.path("/search");

            if(!$scope.$$phase)
                $scope.$apply();
        }
    });


    $scope.firstEnterInit = function() {

    }


});