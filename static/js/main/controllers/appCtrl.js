'use strict';

app.controller('AppCtrl', function($scope, $rootScope, $location, $cookies, $routeParams) {

    $rootScope.publicationTypes = [
        { name: "house", id: 0, title: "Дома",
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
            ]
        },
        { name: "flat", id: 1, title: "Квартиры",
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
                "total_area_from", "total_area_to",
                "floor_from", "floor_to",
                "planing_sid",
                "lift", "electricity",
                "hot_water", "cold_water",
                "gas",
                "heating_type_sid"  // Тільки в продажі
            ]
        },
        { name: "apartments",id: 2, title: "Аппартаменты",
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
                "total_area_from", "total_area_to",
                "floor_from", "floor_to",
                "planing_sid",
                "lift", "electricity",
                "hot_water", "cold_water",
                "gas",
                "heating_type_sid"  // Тільки в продажі
            ]
        },
        { name: "cottage", id: 3, title: "Коттеджы",
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
            ]
        },
        { name: "room", id: 4, title: "Комнаты",
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
                "total_area_from", "total_area_to",
                "floor_from", "floor_to",
                "lift", "electricity",
                "hot_water", "cold_water",
                "gas",
                "heating_type_sid"  // Тільки в продажі
            ]
        },
        { name: "trade", id: 5, title: "Торговые помещения",
            filters: [
                "operation_sid",
                "price_from", "price_to", "currency_sid",
                "new_buildings",
                "secondary_market",
                "halls_area_from", "halls_area_to",
                "total_area_from", "total_area_to",
                "building_type_sid",
                "gas", "electricity",
                "hot_water", "cold_water",
                "sewerage"
            ]
        },
        { name: "office", id: 6, title: "Офисы",
            filters: [
                "operation_sid",
                "price_from", "price_to", "currency_sid",
                "new_buildings",
                "secondary_market",
                "total_area_from", "total_area_to",
                "cabinets_count_from", "cabinets_count_to",
                "security", "kitchen",
                "hot_water", "cold_water",
            ]
        },
        { name: "warehouse", id: 7, title: "Склады",
            filters: [
                "operation_sid",
                "price_from", "price_to", "currency_sid",
                "new_buildings",
                "secondary_market",
                "halls_area_from", "halls_area_to",
                "gas", "electricity",
                "hot_water", "cold_water",
                "security_alarm", "fire_alarm"
            ]
        },
        { name: "business", id: 8, title: "Готовый бизнес",
            filters: [
                "operation_sid",
                "price_from", "price_to", "currency_sid",
                "new_buildings",
                "secondary_market"
            ]
        },
        { name: "catering", id: 9, title: "Обьекты общепита",
            filters: [
                "operation_sid",
                "price_from", "price_to", "currency_sid",
                "new_buildings",
                "secondary_market",
                "total_area_from", "total_area_to",
                "halls_area_from", "halls_area_to",
                "halls_count_from", "halls_count_to",
                "building_type_sid",
                "gas", "electricity",
                "hot_water", "cold_water"
            ]
        },
        { name: "garage", id: 10, title: "Гаражи",
            filters: [
                "operation_sid",
                "price_from", "price_to", "currency_sid",
                "total_area_from", "total_area_to",
            ]
        },
        { name: "land", id: 11, title: "Земельные участки",
            filters: [
                "operation_sid",
                "price_from", "price_to", "currency_sid",
                "area_from", "area_to",
                "gas", "electricity",
                "water", "sewerage"
            ]
        }
    ];
    $rootScope.currencyTypes = [{
        id: 0,
        name: "USD",
        title: "Дол."
    }, {
        id: 1,
        name: "EUR",
        title: "Евро"
    }, {
        id: 2,
        name: "UAH",
        title: "Грн."
    }];


    $rootScope.loadings = {
        markers: false
    };

    $rootScope.subdommain = "";


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
        $rootScope.publicationIdPart = $routeParams.id;

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