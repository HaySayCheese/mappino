'use strict';

app.controller('AppCtrl', function($scope, $rootScope, $location, $cookies, $routeParams, TXT) {

    $rootScope.pageTitle = TXT.SERVICE_NAME;

    $rootScope.publicationTypes = [
        { name: "flat", id: 0, title: "Квартиры",
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
                "mansard",
                "ground",
                "planing_sid",
                "lift", "electricity",
                "hot_water", "cold_water",
                "gas",
                "heating_type_sid"  // Тільки в продажі
            ]
        },
        { name: "house", id: 1, title: "Дома",
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
        { name: "room", id: 2, title: "Комнаты",
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
                "mansard",
                "ground",
                "lift", "electricity",
                "hot_water", "cold_water",
                "gas",
                "heating_type_sid"  // Тільки в продажі
            ]
        },
        { name: "land", id: 3, title: "Земельные участки",
            filters: [
                "operation_sid",
                "price_from", "price_to", "currency_sid",
                "area_from", "area_to",
                "gas", "electricity",
                "water", "sewerage"
            ]
        },
        { name: "garage", id: 4, title: "Гаражи",
            filters: [
                "operation_sid",
                "price_from", "price_to", "currency_sid",
                "total_area_from", "total_area_to"
            ]
        },
        { name: "office", id: 5, title: "Офисы",
            filters: [
                "operation_sid",
                "price_from", "price_to", "currency_sid",
                "new_buildings",
                "secondary_market",
                "total_area_from", "total_area_to",
                "cabinets_count_from", "cabinets_count_to",
                "security", "kitchen",
                "hot_water", "cold_water"
            ]
        },
        { name: "trade", id: 6, title: "Торговые помещения",
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
                "price_from", "price_to", "currency_sid"
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
    $rootScope.opeartionTypes = {
        sale: 0,
        rent: 1
    };
    $rootScope.rentTypes = {
        undefined: 0,
        daily: 1,
        monthly: 2
    };
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

        $location.path("/");

        if(!$scope.$$phase)
            $scope.$apply();
    });


    /**
     * Логіка підставлення в урл параметрів пошука
     **/
    $scope.$on("$routeChangeSuccess", function() {
        $scope.urlFiltersPart = $location.url().replace("/", "");
        $rootScope.publicationIdPart = $routeParams.id;

        angular.element(".modal-backdrop").remove();

        if ($location.path() == "/")
            $rootScope.pageTitle = TXT.SERVICE_NAME;
    });


    /**
     * Логіка унеможливлення переходу до реєстрації або логіну
     * якщо юзер уже залогінений
     **/
    $scope.$on("$locationChangeStart", function(event, next, current) {

        if (!$cookies.sessionid)
            return;

        if (next.indexOf("/account/registration") != -1 ||
            next.indexOf("/account/login") != -1 ||
            next.indexOf("/account/restore-access") != -1) {
            $location.path("/");

            if(!$scope.$$phase)
                $scope.$apply();
        }
    });
});