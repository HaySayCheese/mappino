(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});

var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var RealtyTypesService = (function () {
    function RealtyTypesService() {
        "use strict";

        _classCallCheck(this, RealtyTypesService);

        this._realty_types = [{
            id: 0,
            name: "flat",
            title: "Квартиры",
            filters: ["op_sid", "pr_sid", "p_min", "p_max", "cu_sid", "p_c_min", "p_c_max", "n_b", "s_m", "fml", "frg", "r_c_min", "r_c_max", "t_a_min", "t_a_max", "f_min", "f_max", "msd", "grd", "pl_sid", "lft", "elt", "h_w", "c_w", "gas", "h_t_sid"]
        }, {
            id: 1,
            name: "house",
            title: "Дома",
            filters: ["op_sid", "pr_sid", "p_min", "p_max", "cu_sid", "p_c_min", "p_c_max", "n_b", "s_m", "fml", "frg", "r_c_min", "r_c_max", "f_c_min", "f_c_max", "elt", "h_w", "gas", "c_w", "swg", "h_t_sid"]
        }, {
            id: 2,
            name: "room",
            title: "Комнаты",
            filters: ["op_sid", "pr_sid", "p_min", "p_max", "cu_sid", "p_c_min", "p_c_max", "n_b", "s_m", "fml", "frg", "r_c_min", "r_c_max", "t_a_min", "t_a_max", "f_min", "f_max", "msd", "grd", "lft", "elt", "h_w", "c_w", "gas", "h_t_sid"]
        }, {
            id: 3,
            name: "land",
            title: "Земельные участки",
            filters: ["op_sid", "p_min", "p_max", "cu_sid", "a_min", "a_max", "gas", "elt", "wtr", "swg"]
        }, {
            id: 4,
            name: "garage",
            title: "Гаражи",
            filters: ["op_sid", "p_min", "p_max", "cu_sid", "t_a_min", "t_a_max"]
        }, {
            id: 5,
            name: "office",
            title: "Офисы",
            filters: ["op_sid", "p_min", "p_max", "cu_sid", "n_b", "s_m", "t_a_min", "t_a_max", "c_c_min", "c_c_max", "sct", "ktn", "h_w", "c_w"]
        }, {
            id: 6,
            name: "trade",
            title: "Торговые помещения",
            filters: ["op_sid", "p_min", "p_max", "cu_sid", "n_b", "s_m", "h_a_min", "h_a_max", "t_a_min", "t_a_max", "b_t_sid", "gas", "elt", "h_w", "c_w", "swg"]
        }, {
            id: 7,
            name: "warehouse",
            title: "Склады",
            filters: ["op_sid", "p_min", "p_max", "cu_sid", "n_b", "s_m", "h_a_min", "h_a_max", "gas", "elt", "h_w", "c_w", "s_a", "f_a"]
        }, {
            id: 8,
            name: "business",
            title: "Готовый бизнес",
            filters: ["op_sid", "p_min", "p_max", "cu_sid"]
        }];
    }

    _createClass(RealtyTypesService, [{
        key: "realty_types",
        get: function () {
            return this._realty_types;
        }
    }]);

    return RealtyTypesService;
})();

exports.RealtyTypesService = RealtyTypesService;

},{}],2:[function(require,module,exports){
"use strict";

var _commonBModulesTypesServicesRealtyTypesServiceJs = require("../_common/bModules/Types/services/realty-types.service.js");

var _controllersAppControllerJs = require("./controllers/app.controller.js");

var _controllersMapControllerJs = require("./controllers/map.controller.js");

var _controllersFiltersPanelControllerJs = require("./controllers/filters-panel.controller.js");

var _controllersPlaceAutocompleteControllerJs = require("./controllers/place-autocomplete.controller.js");

var _handlersPanelsHendlerJs = require("./handlers/panels.hendler.js");

var _servicesFiltersServiceJs = require("./services/filters.service.js");

var _servicesMarkersServiceJs = require("./services/markers.service.js");

var _directivesTabsPanelDirectiveJs = require("./directives/tabs-panel.directive.js");

var app = angular.module("mappino.pages.map", ["ngMaterial", "ngCookies", "ngResource", "ui.router"]);

app.config(["$stateProvider", "$urlRouterProvider", "$locationProvider", function ($stateProvider, $urlRouterProvider, $locationProvider) {
    $urlRouterProvider.otherwise("/0/0/");

    $stateProvider.state("base", {
        url: "/:left_panel_index/:right_panel_index/"
    });

    $locationProvider.hashPrefix("!");
}]);

app.config(["$interpolateProvider", "$resourceProvider", function ($interpolateProvider, $resourceProvider) {
    $interpolateProvider.startSymbol("[[");
    $interpolateProvider.endSymbol("]]");

    $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

app.config(["$mdThemingProvider", "$mdIconProvider", function ($mdThemingProvider, $mdIconProvider) {
    $mdThemingProvider.setDefaultTheme("default");

    $mdThemingProvider.theme("default").primaryPalette("blue");
}]);

app.run(["$http", "$cookies", function ($http, $cookies) {
    $http.defaults.headers.common["X-CSRFToken"] = $cookies.csrftoken;
}]);

/** Handlers */
app.service("PanelsHandler", _handlersPanelsHendlerJs.PanelsHandler);

/** bModule services */
app.service("RealtyTypesService", _commonBModulesTypesServicesRealtyTypesServiceJs.RealtyTypesService);

/** Services */
app.service("FiltersService", _servicesFiltersServiceJs.FiltersService);
app.service("MarkersService", _servicesMarkersServiceJs.MarkersService);

/** Directives */
app.directive("tabBodyCollapsible", _directivesTabsPanelDirectiveJs.tabBodyCollapsible);
app.directive("tabBodySectionCollapsible", _directivesTabsPanelDirectiveJs.tabBodySectionCollapsible);

/** Controllers */
app.controller("AppController", _controllersAppControllerJs.AppController);
app.controller("FiltersPanelController", _controllersFiltersPanelControllerJs.FiltersPanelController);
app.controller("MapController", _controllersMapControllerJs.MapController);
app.controller("PlaceAutocompleteController", _controllersPlaceAutocompleteControllerJs.PlaceAutocompleteController);

},{"../_common/bModules/Types/services/realty-types.service.js":1,"./controllers/app.controller.js":3,"./controllers/filters-panel.controller.js":4,"./controllers/map.controller.js":5,"./controllers/place-autocomplete.controller.js":6,"./directives/tabs-panel.directive.js":7,"./handlers/panels.hendler.js":8,"./services/filters.service.js":9,"./services/markers.service.js":10}],3:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, '__esModule', {
    value: true
});

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError('Cannot call a class as a function'); } }

var AppController = function AppController($state, $rootScope, $location, panelsHandler) {
    _classCallCheck(this, AppController);
};

exports.AppController = AppController;

AppController.$inject = ['$state', '$rootScope', '$location', 'PanelsHandler'];

},{}],4:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, '__esModule', {
    value: true
});

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError('Cannot call a class as a function'); } }

var FiltersPanelController = function FiltersPanelController($scope, filtersService, realtyTypesService) {
    _classCallCheck(this, FiltersPanelController);

    this.$scope = $scope;

    $scope.filters = filtersService.filters.panels;
    $scope.realtyTypes = realtyTypesService.realty_types;
};

exports.FiltersPanelController = FiltersPanelController;

FiltersPanelController.$inject = ['$scope', 'FiltersService', 'RealtyTypesService'];

},{}],5:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, '__esModule', {
    value: true
});

var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ('value' in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError('Cannot call a class as a function'); } }

var MapController = (function () {
    function MapController($scope, filtersService, markersService) {
        var _this = this;

        _classCallCheck(this, MapController);

        this.$scope = $scope;
        this.filtersService = filtersService;
        this.markersService = markersService;

        this._map = null;

        google.maps.event.addDomListener(window, 'load', this.initMap());

        $scope.$on('pages.map.MarkersService.MarkersIsLoaded', function () {
            markersService.place(_this._map);
        });

        $scope.$on('pages.map.PlaceAutocompleteController.PlaceChanged', function (event, place) {
            _this.positioningMap(place);
        });
    }

    _createClass(MapController, [{
        key: 'initMap',
        value: function initMap() {
            var _this2 = this;

            var map_options = {
                center: new google.maps.LatLng(this.filtersService.filters.map.l.split(',')[0], this.filtersService.filters.map.l.split(',')[1]),
                zoom: parseInt(this.filtersService.filters.map.z),
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                disableDefaultUI: true,
                styles: [{ 'featureType': 'all', 'stylers': [{ 'saturation': 0 }, { 'hue': '#e7ecf0' }] }, { 'featureType': 'road', 'stylers': [{ 'saturation': -70 }] }, { 'featureType': 'transit', 'stylers': [{ 'visibility': 'off' }] }, { 'featureType': 'poi', 'stylers': [{ 'visibility': 'off' }] }, { 'featureType': 'water', 'stylers': [{ 'visibility': 'simplified' }, { 'saturation': -60 }] }]
            };

            this._map = new google.maps.Map(document.getElementById('map'), map_options);

            google.maps.event.addListener(this._map, 'idle', function () {
                _this2.filtersService.update('map', {
                    z: _this2._map.getZoom(),
                    v: _this2._map.getBounds(),
                    l: _this2._map.getCenter().toUrlValue()
                });
            });
        }
    }, {
        key: 'positioningMap',
        value: function positioningMap(place) {
            if (!place.geometry) return;

            if (place.geometry.viewport) {
                this._map.fitBounds(place.geometry.viewport);
            } else {
                this._map.panTo(place.geometry.location);
                this._map.setZoom(17);
            }
        }
    }]);

    return MapController;
})();

exports.MapController = MapController;

MapController.$inject = ['$scope', 'FiltersService', 'MarkersService'];

},{}],6:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});

var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var PlaceAutocompleteController = (function () {
    function PlaceAutocompleteController($scope, $rootScope, filtersService) {
        var _this = this;

        _classCallCheck(this, PlaceAutocompleteController);

        var self = this;
        this._autocomplete = null;
        this._autocompleteInput = document.getElementById("place-autocomplete");

        /** Listen events */
        google.maps.event.addDomListener(window, "load", function () {
            return _this.initAutocomplete(self);
        });

        $scope.$on("pages.map.FiltersService.UpdatedFromUrl", function (event, filters) {
            _this._autocompleteInput.value = filters.map.c;
        });
    }

    _createClass(PlaceAutocompleteController, [{
        key: "initAutocomplete",
        value: function initAutocomplete(self) {
            self._autocomplete = new google.maps.places.Autocomplete(this._autocompleteInput, {
                componentRestrictions: {
                    country: "ua"
                }
            });

            google.maps.event.addListener(self._autocomplete, "place_changed", function () {
                self.filtersService.update("map", {
                    c: self._autocomplete.getPlace().formatted_address
                });

                self.$rootScope.$broadcast("pages.map.PlaceAutocompleteController.PlaceChanged", self._autocomplete.getPlace());
                //
                //if (!self.$scope.$$phase)
                //    self.$scope.$apply();
            });
        }
    }]);

    return PlaceAutocompleteController;
})();

exports.PlaceAutocompleteController = PlaceAutocompleteController;

PlaceAutocompleteController.$inject = ["$scope", "$rootScope", "FiltersService"];

},{}],7:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, '__esModule', {
    value: true
});
exports.tabBodyCollapsible = tabBodyCollapsible;
exports.tabBodySectionCollapsible = tabBodySectionCollapsible;

function tabBodyCollapsible() {
    return {
        restrict: 'E',

        link: function link(scope, element, attrs, modelCtrl) {
            angular.element('[toggle-tab-body]').on('click', function (_element) {
                angular.element(_element.currentTarget).toggleClass('-tab-body-closed');
                angular.element(element).toggleClass('-closed');
            });
        }
    };
}

function tabBodySectionCollapsible() {
    return {
        restrict: 'E',

        link: function link(scope, element, attrs, modelCtrl) {
            angular.element('[toggle-tab-body-section]').on('click', function (_element) {
                angular.element(_element.currentTarget).toggleClass('-tab-body-section-closed');
                angular.element(element).toggleClass('-closed');
            });
        }
    };
}

},{}],8:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, '__esModule', {
    value: true
});

var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ('value' in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError('Cannot call a class as a function'); } }

var PanelsHandler = (function () {
    function PanelsHandler($state, $stateParams, $rootScope, $location) {
        var _this = this;

        _classCallCheck(this, PanelsHandler);

        this.$state = $state;
        this.$stateParams = $stateParams;
        this.$rootScope = $rootScope;
        this.$location = $location;

        this._location_search = null;

        $rootScope.panelsIndex = {
            leftPanelIndex: 0,
            rightPanelIndex: 0
        };

        $rootScope.$watch('panelsIndex.leftPanelIndex', function (newValue, oldValue) {
            $state.go('base', { left_panel_index: newValue });
        }, true);

        $rootScope.$watch('panelsIndex.rightPanelIndex', function (newValue, oldValue) {
            $state.go('base', { right_panel_index: newValue });
        }, true);

        /**
         * Відновлюємо фільтри в урлі після зміни панелі
         **/
        var _onceUpdateTabsFromUrl = _.once(this.onceUpdateTabsFromUrl);
        $rootScope.$on('$stateChangeStart', function () {
            if (!_.isNull($location.search())) {
                _this._location_search = $location.search();
            }
        });
        $rootScope.$on('$stateChangeSuccess', function () {
            _onceUpdateTabsFromUrl(_this);

            if (!_.isNull(_this._location_search)) {
                $location.search(_this._location_search);
            }
        });
    }

    _createClass(PanelsHandler, [{
        key: 'onceUpdateTabsFromUrl',
        value: function onceUpdateTabsFromUrl(self) {
            self.$rootScope.panelsIndex = {
                leftPanelIndex: self.$stateParams.left_panel_index || 0,
                rightPanelIndex: self.$stateParams.right_panel_index || 0
            };
        }
    }]);

    return PanelsHandler;
})();

exports.PanelsHandler = PanelsHandler;

PanelsHandler.$inject = ['$state', '$stateParams', '$rootScope', '$location'];

},{}],9:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});

var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var FiltersService = (function () {
    function FiltersService($rootScope, $timeout, $location, realtyTypesService) {
        _classCallCheck(this, FiltersService);

        this.$rootScope = $rootScope;
        this.$timeout = $timeout;
        this.$location = $location;
        this.realtyTypesService = realtyTypesService;

        this._filters_for_load_markers = {
            zoom: null,
            viewport: null,
            filters: []
        };
        this._filters = {
            map: {
                c: null, // city
                l: "48.455935,34.41285", // lat_lng
                v: null, // viewport
                z: 6 // zoom
            },
            panels: {
                red: {
                    r_t_sid: null
                },
                blue: {
                    b_t_sid: null
                },
                green: {
                    g_t_sid: null
                },
                yellow: {
                    y_t_sid: null
                }
            },
            base: {
                // Загальні
                op_sid: 0, // operation_sid

                // Дропдауни
                cu_sid: 0, // currency_sid
                h_t_sid: 0, // heating_type_sid
                pr_sid: 0, // period_sid
                pl_sid: 0, // planing_sid
                b_t_sid: 0, // building_type_sid

                // Поля вводу
                p_min: null, // price_min
                p_max: null, // price_max
                r_c_min: null, // rooms_count_min
                r_c_max: null, // rooms_count_max
                f_c_min: null, // floors_count_min
                f_c_max: null, // floors_count_max
                p_c_min: null, // persons_count_min
                p_c_max: null, // persons_count_max
                t_a_min: null, // total_area_min
                t_a_max: null, // total_area_max
                f_min: null, // floor_min
                f_max: null, // floor_max
                h_a_min: null, // halls_area_min
                h_a_max: null, // halls_area_max
                c_c_min: null, // cabinets_count_min
                c_c_max: null, // cabinets_count_max
                h_c_min: null, // halls_count_min
                h_c_max: null, // halls_count_max
                c_h_min: null, // ceiling_height_min
                c_h_max: null, // ceiling_height_max
                a_min: null, // area_min
                a_max: null, // area_max

                // Чекбокси
                n_b: true, // new_buildings
                s_m: true, // secondary_market
                fml: false, // family
                frg: false, // foreigners
                elt: false, // electricity
                gas: false, // gas
                h_w: false, // hot_water
                c_w: false, // cold_water
                swg: false, // sewerage
                lft: false, // lift
                sct: false, // security
                ktn: false, // kitchen
                s_a: false, // security_alarm
                f_a: false, // fire_alarm
                pit: false, // pit
                wtr: false, // water
                msd: true, // mansard
                grd: true // ground
            }
        };
        this.updateFiltersFromUrl();
    }

    _createClass(FiltersService, [{
        key: "update",
        value: function update(filter_object_name, filters_object) {
            var _this = this;

            for (var filter in filters_object) {
                if (filters_object.hasOwnProperty(filter)) {
                    this._filters[filter_object_name][filter] = filters_object[filter];
                }
            }

            this.updateUrlFromFilters();
            this.createFormattedObjectForLoadMarkers();

            this.$timeout(function () {
                return _this.$rootScope.$broadcast("pages.map.FiltersService.FiltersUpdated", _this._filters);
            });
        }
    }, {
        key: "createFiltersForPanel",
        value: function createFiltersForPanel(panel_color) {
            var _this2 = this;

            var self = this,
                panel_prefix = panel_color.toString().substring(0, 1) + "_",
                type_sid = this._filters.panels[panel_color][panel_prefix + "t_sid"],
                location_search = this.$location.search();

            if (_.isNull(type_sid)) {
                // Очищаємо обєкт з фільтрами
                this._filters.panels[panel_color] = {};

                // Створюємо параметр з типом оголошення в обєкті з фільтрами
                this._filters.panels[panel_color][panel_prefix + "t_sid"] = type_sid;

                // Видаляємо фільтри з урла
                for (var s_key in location_search) {
                    if (location_search.hasOwnProperty(s_key)) {
                        if (s_key.match(new RegExp("^" + panel_prefix, "m"))) {
                            this.$location.search(s_key, null);
                        }
                    }
                }
            }

            // Створюємо набір фільтрів для панелі за набором
            if (!_.isNull(type_sid)) {
                var realty_type_filters = _.where(self.realtyTypesService.realty_types, { "id": type_sid })[0].filters;

                for (var i = 0, len = realty_type_filters.length; i < len; i++) {
                    var filter_name = panel_prefix + realty_type_filters[i];

                    if (_.isUndefined(this._filters.panels[panel_color][filter_name])) {
                        this._filters.panels[panel_color][filter_name] = this._filters.base[realty_type_filters[i]];
                    }
                }
            }

            this.$timeout(function () {
                return _this2.$rootScope.$broadcast("pages.map.FiltersService.FiltersUpdated", _this2._filters);
            });
        }
    }, {
        key: "updateFiltersFromUrl",
        value: function updateFiltersFromUrl() {
            var _this3 = this;

            var location_search = this.$location.search(),
                filters_panels = this._filters.panels;

            for (var key in location_search) {
                if (location_search.hasOwnProperty(key)) {

                    if (key.toString() === "token") {
                        continue;
                    }
                    if (location_search[key] === "true") {
                        location_search[key] = true;
                    }
                    if (location_search[key] === "false") {
                        location_search[key] = false;
                    }
                    if (key.toString().indexOf("_sid") !== -1) {
                        location_search[key] = parseInt(location_search[key]);
                    }
                    if (/^r_/.test(key.toString())) {
                        filters_panels["red"][key] = location_search[key];
                    }
                    if (/^b_/.test(key.toString())) {
                        filters_panels["blue"][key] = location_search[key];
                    }
                    if (/^g_/.test(key.toString())) {
                        filters_panels["green"][key] = location_search[key];
                    }
                    if (/^y_/.test(key.toString())) {
                        filters_panels["yellow"][key] = location_search[key];
                    }
                    if (_.include(["c", "l", "z"], key)) {
                        this._filters["map"][key] = location_search[key];
                    }
                }
            }

            if (_.isUndefined(location_search["r_t_sid"]) && _.isUndefined(location_search["b_t_sid"]) && _.isUndefined(location_search["g_t_sid"]) && _.isUndefined(location_search["y_t_sid"])) {
                // -
                filters_panels["red"]["r_t_sid"] = 0;
                this.createFiltersForPanel("red");
            }
            if (!_.isUndefined(location_search["r_t_sid"])) {
                this.createFiltersForPanel("red");
            }
            if (!_.isUndefined(location_search["b_t_sid"])) {
                this.createFiltersForPanel("blue");
            }
            if (!_.isUndefined(location_search["g_t_sid"])) {
                this.createFiltersForPanel("green");
            }
            if (!_.isUndefined(location_search["y_t_sid"])) {
                this.createFiltersForPanel("yellow");
            }

            this.$timeout(function () {
                return _this3.$rootScope.$broadcast("pages.map.FiltersService.UpdatedFromUrl", _this3._filters);
            });
        }
    }, {
        key: "updateUrlFromFilters",
        value: function updateUrlFromFilters() {
            var location_search = "",
                map_filters = this._filters["map"],
                panels_filters = this._filters["panels"],
                _formattedPanelFilters = {};

            // reset to empty object
            this._filters_for_load_markers = {
                zoom: null,
                viewport: null,
                filters: []
            };

            // create location search from map filters
            for (var map_filter in map_filters) {
                if (map_filters.hasOwnProperty(map_filter) && !_.include(["v"], map_filter)) {
                    if (!map_filters[map_filter]) {
                        continue;
                    }
                    if (!_.include(["", null], map_filters[map_filter])) {
                        location_search += (location_search.length !== 0 ? "&" : "") + map_filter + "=" + map_filters[map_filter];
                    }
                }
            }

            // create location search from panels filters
            for (var panel in panels_filters) {
                if (panels_filters.hasOwnProperty(panel)) {
                    _formattedPanelFilters = {
                        panel: panel
                    };

                    for (var panel_filter in panels_filters[panel]) {
                        if (panels_filters[panel].hasOwnProperty(panel_filter)) {

                            if (panel_filter.indexOf("t_sid") !== -1 && _.isNull(panels_filters[panel][panel_filter])) {
                                _formattedPanelFilters = null;
                                continue;
                            }

                            if (_.include(["", null], panels_filters[panel][panel_filter])) {
                                continue;
                            }

                            _formattedPanelFilters[panel_filter.substr(2, panel_filter.length)] = panels_filters[panel][panel_filter];

                            if (panels_filters[panel][panel_filter] === this._filters["base"][panel_filter.substr(2, panel_filter.length)]) {
                                continue;
                            }

                            // i love js
                            //if (_.include(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], filters_panels[panel][filter])) {
                            //    filters_panels[panel][filter] = parseInt(filters_panels[panel][filter]);
                            //}

                            location_search += (location_search.length !== 0 ? "&" : "") + panel_filter + "=" + panels_filters[panel][panel_filter];
                        }
                    }

                    if (!_.isNull(_formattedPanelFilters)) this._filters_for_load_markers["filters"].push(_formattedPanelFilters);
                }
            }

            console.info("updateUrlFromPanelsFilters method: panels filters updated");

            this.$location.search(location_search);

            if (!this.$rootScope.$$phase) this.$rootScope.$apply();
        }
    }, {
        key: "createFormattedObjectForLoadMarkers",
        value: function createFormattedObjectForLoadMarkers() {
            var _this4 = this;

            this._filters_for_load_markers.zoom = this._filters.map.z;
            this.createFormattedViewportForLoadMarkers();

            this.$timeout(function () {
                return _this4.$rootScope.$broadcast("pages.map.FiltersService.CreatedFormattedFilters", _this4._filters_for_load_markers);
            });
        }
    }, {
        key: "createFormattedViewportForLoadMarkers",
        value: function createFormattedViewportForLoadMarkers() {
            var filters_map = this._filters.map;

            var sneLat = filters_map.v.getNorthEast().lat().toString(),
                sneLng = filters_map.v.getNorthEast().lng().toString(),
                sswLat = filters_map.v.getSouthWest().lat().toString(),
                sswLng = filters_map.v.getSouthWest().lng().toString();

            var neLat = sneLat.replace(sneLat.substring(sneLat.indexOf(".") + 3, sneLat.length), ""),
                neLng = sneLng.replace(sneLng.substring(sneLng.indexOf(".") + 3, sneLng.length), ""),
                swLat = sswLat.replace(sswLat.substring(sswLat.indexOf(".") + 3, sswLat.length), ""),
                swLng = sswLng.replace(sswLng.substring(sswLng.indexOf(".") + 3, sswLng.length), "");

            this._filters_for_load_markers.viewport = {
                "ne_lat": neLat,
                "ne_lng": neLng,
                "sw_lat": swLat,
                "sw_lng": swLng
            };

            console.log(this._filters_for_load_markers);
        }
    }, {
        key: "filters",
        get: function () {
            return this._filters;
        }
    }]);

    return FiltersService;
})();

exports.FiltersService = FiltersService;

FiltersService.$inject = ["$rootScope", "$timeout", "$location", "RealtyTypesService"];

},{}],10:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, '__esModule', {
    value: true
});

var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ('value' in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError('Cannot call a class as a function'); } }

var MarkersService = (function () {
    function MarkersService($rootScope, $http, $timeout) {
        _classCallCheck(this, MarkersService);

        var self = this;

        this.$rootScope = $rootScope;
        this.$http = $http;
        this.$timeout = $timeout;

        this._filters_for_load_markers = null;
        this._response_markers = {
            red: {},
            blue: {},
            green: {}
        };
        this._markers = {
            red: {},
            blue: {},
            green: {}
        };

        $rootScope.$on('pages.map.FiltersService.CreatedFormattedFilters', function (event, formatted_filters) {
            self._filters_for_load_markers = formatted_filters;

            self.load();
        });
    }

    _createClass(MarkersService, [{
        key: 'load',
        value: function load() {
            var self = this;

            this.$http.get('/ajax/api/markers/?p=' + JSON.stringify(this._filters_for_load_markers)).success(function (response) {
                self.clearResponseMarkersObject();

                self._response_markers = response;
                self.$timeout(function () {
                    return self.$rootScope.$broadcast('pages.map.MarkersService.MarkersIsLoaded');
                });
            });
        }
    }, {
        key: 'place',
        value: function place(map) {
            var _this = this;

            // видаляємо маркери з карти яких нема в відповіді з сервера
            for (var panel in this._markers) {
                if (this._markers.hasOwnProperty(panel)) {
                    for (var marker in this._markers[panel]) {
                        if (this._markers[panel].hasOwnProperty(marker)) {
                            if (!this._response_markers[panel][marker]) {
                                this._markers[panel][marker].setMap(null);
                                console.log('deleted: ' + this._markers[panel][marker]);

                                delete this._markers[panel][marker];
                            }
                            console.log(this._markers);
                        }
                    }
                }
            }

            // додаємо новві маркери на карту
            for (var panel in this._response_markers) {
                if (this._response_markers.hasOwnProperty(panel)) {
                    for (var marker in this._response_markers[panel]) {
                        if (this._response_markers[panel].hasOwnProperty(marker)) {

                            if (!this._markers[panel][marker]) {
                                this._markers[panel][marker] = new google.maps.Marker({
                                    position: new google.maps.LatLng(marker.split(':')[0], marker.split(':')[1]),
                                    map: map,
                                    title: 'Hello World!'
                                });
                                this._markers[panel][marker].setMap(map);
                                console.log('added: ' + this._markers[panel][marker]);
                            }

                            console.log(this._markers);
                        }
                    }
                }
            }

            this.$timeout(function () {
                return _this.$rootScope.$broadcast('pages.map.MarkersService.MarkersPlaced');
            });
        }
    }, {
        key: 'clearResponseMarkersObject',
        value: function clearResponseMarkersObject() {
            this._response_markers = {
                red: {},
                blue: {},
                green: {}
            };
        }
    }]);

    return MarkersService;
})();

exports.MarkersService = MarkersService;

MarkersService.$inject = ['$rootScope', '$http', '$timeout'];

},{}]},{},[2])
//# sourceMappingURL=data:application/json;charset:utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIm5vZGVfbW9kdWxlcy9icm93c2VyaWZ5L25vZGVfbW9kdWxlcy9icm93c2VyLXBhY2svX3ByZWx1ZGUuanMiLCJEOi9Qcm9qZWN0cy9tYXBwaW5vL3N0YXRpYy9zb3VyY2Uvc2NyaXB0cy9fY29tbW9uL2JNb2R1bGVzL1R5cGVzL3NlcnZpY2VzL3JlYWx0eS10eXBlcy5zZXJ2aWNlLmpzIiwiRDovUHJvamVjdHMvbWFwcGluby9zdGF0aWMvc291cmNlL3NjcmlwdHMvbWFwL2FwcC5qcyIsIkQ6L1Byb2plY3RzL21hcHBpbm8vc3RhdGljL3NvdXJjZS9zY3JpcHRzL21hcC9jb250cm9sbGVycy9hcHAuY29udHJvbGxlci5qcyIsIkQ6L1Byb2plY3RzL21hcHBpbm8vc3RhdGljL3NvdXJjZS9zY3JpcHRzL21hcC9jb250cm9sbGVycy9maWx0ZXJzLXBhbmVsLmNvbnRyb2xsZXIuanMiLCJEOi9Qcm9qZWN0cy9tYXBwaW5vL3N0YXRpYy9zb3VyY2Uvc2NyaXB0cy9tYXAvY29udHJvbGxlcnMvbWFwLmNvbnRyb2xsZXIuanMiLCJEOi9Qcm9qZWN0cy9tYXBwaW5vL3N0YXRpYy9zb3VyY2Uvc2NyaXB0cy9tYXAvY29udHJvbGxlcnMvcGxhY2UtYXV0b2NvbXBsZXRlLmNvbnRyb2xsZXIuanMiLCJEOi9Qcm9qZWN0cy9tYXBwaW5vL3N0YXRpYy9zb3VyY2Uvc2NyaXB0cy9tYXAvZGlyZWN0aXZlcy90YWJzLXBhbmVsLmRpcmVjdGl2ZS5qcyIsIkQ6L1Byb2plY3RzL21hcHBpbm8vc3RhdGljL3NvdXJjZS9zY3JpcHRzL21hcC9oYW5kbGVycy9wYW5lbHMuaGVuZGxlci5qcyIsIkQ6L1Byb2plY3RzL21hcHBpbm8vc3RhdGljL3NvdXJjZS9zY3JpcHRzL21hcC9zZXJ2aWNlcy9maWx0ZXJzLnNlcnZpY2UuanMiLCJEOi9Qcm9qZWN0cy9tYXBwaW5vL3N0YXRpYy9zb3VyY2Uvc2NyaXB0cy9tYXAvc2VydmljZXMvbWFya2Vycy5zZXJ2aWNlLmpzIl0sIm5hbWVzIjpb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Q0FBQyxDQUFDO1NBQzdGOzs7ZUFJeUIsc0NBQUc7QUFDekIsZ0JBQUksQ0FBQyxpQkFBaUIsR0FBRztBQUNyQixtQkFBRyxFQUFLLEVBQUU7QUFDVixvQkFBSSxFQUFJLEVBQUU7QUFDVixxQkFBSyxFQUFHLEVBQUU7YUFDYixDQUFDO1NBQ0w7OztXQWhHUSxjQUFjOzs7UUFBZCxjQUFjLEdBQWQsY0FBYzs7QUFtRzNCLGNBQWMsQ0FBQyxPQUFPLEdBQUcsQ0FDckIsWUFBWSxFQUNaLE9BQU8sRUFDUCxVQUFVLENBQ2IsQ0FBQyIsImZpbGUiOiJnZW5lcmF0ZWQuanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlc0NvbnRlbnQiOlsiKGZ1bmN0aW9uIGUodCxuLHIpe2Z1bmN0aW9uIHMobyx1KXtpZighbltvXSl7aWYoIXRbb10pe3ZhciBhPXR5cGVvZiByZXF1aXJlPT1cImZ1bmN0aW9uXCImJnJlcXVpcmU7aWYoIXUmJmEpcmV0dXJuIGEobywhMCk7aWYoaSlyZXR1cm4gaShvLCEwKTt2YXIgZj1uZXcgRXJyb3IoXCJDYW5ub3QgZmluZCBtb2R1bGUgJ1wiK28rXCInXCIpO3Rocm93IGYuY29kZT1cIk1PRFVMRV9OT1RfRk9VTkRcIixmfXZhciBsPW5bb109e2V4cG9ydHM6e319O3Rbb11bMF0uY2FsbChsLmV4cG9ydHMsZnVuY3Rpb24oZSl7dmFyIG49dFtvXVsxXVtlXTtyZXR1cm4gcyhuP246ZSl9LGwsbC5leHBvcnRzLGUsdCxuLHIpfXJldHVybiBuW29dLmV4cG9ydHN9dmFyIGk9dHlwZW9mIHJlcXVpcmU9PVwiZnVuY3Rpb25cIiYmcmVxdWlyZTtmb3IodmFyIG89MDtvPHIubGVuZ3RoO28rKylzKHJbb10pO3JldHVybiBzfSkiLCJleHBvcnQgY2xhc3MgUmVhbHR5VHlwZXNTZXJ2aWNlIHtcclxuICAgIGNvbnN0cnVjdG9yKCkge1xyXG4gICAgICAgIFwidXNlIHN0cmljdFwiO1xyXG5cclxuICAgICAgICB0aGlzLl9yZWFsdHlfdHlwZXMgPSBbXHJcbiAgICAgICAgICAgIHtcclxuICAgICAgICAgICAgICAgIGlkOiAgICAgMCxcclxuICAgICAgICAgICAgICAgIG5hbWU6ICAgXCJmbGF0XCIsXHJcbiAgICAgICAgICAgICAgICB0aXRsZTogIFwi0JrQstCw0YDRgtC40YDRi1wiLFxyXG4gICAgICAgICAgICAgICAgZmlsdGVyczogW1xyXG4gICAgICAgICAgICAgICAgICAgIFwib3Bfc2lkXCIsIFwicHJfc2lkXCIsIFwicF9taW5cIiwgXCJwX21heFwiLCBcImN1X3NpZFwiLCBcInBfY19taW5cIiwgXCJwX2NfbWF4XCIsIFwibl9iXCIsXHJcbiAgICAgICAgICAgICAgICAgICAgXCJzX21cIiwgXCJmbWxcIiwgXCJmcmdcIiwgXCJyX2NfbWluXCIsIFwicl9jX21heFwiLCBcInRfYV9taW5cIiwgXCJ0X2FfbWF4XCIsIFwiZl9taW5cIiwgXCJmX21heFwiLFxyXG4gICAgICAgICAgICAgICAgICAgIFwibXNkXCIsIFwiZ3JkXCIsIFwicGxfc2lkXCIsIFwibGZ0XCIsIFwiZWx0XCIsIFwiaF93XCIsIFwiY193XCIsIFwiZ2FzXCIsIFwiaF90X3NpZFwiXHJcbiAgICAgICAgICAgICAgICBdXHJcbiAgICAgICAgICAgIH0sIHtcclxuICAgICAgICAgICAgICAgIGlkOiAgICAgMSxcclxuICAgICAgICAgICAgICAgIG5hbWU6ICAgXCJob3VzZVwiLFxyXG4gICAgICAgICAgICAgICAgdGl0bGU6ICBcItCU0L7QvNCwXCIsXHJcbiAgICAgICAgICAgICAgICBmaWx0ZXJzOiBbXHJcbiAgICAgICAgICAgICAgICAgICAgXCJvcF9zaWRcIiwgXCJwcl9zaWRcIiwgXCJwX21pblwiLCBcInBfbWF4XCIsIFwiY3Vfc2lkXCIsIFwicF9jX21pblwiLCBcInBfY19tYXhcIiwgXCJuX2JcIixcclxuICAgICAgICAgICAgICAgICAgICBcInNfbVwiLCBcImZtbFwiLCBcImZyZ1wiLCBcInJfY19taW5cIiwgXCJyX2NfbWF4XCIsIFwiZl9jX21pblwiLCBcImZfY19tYXhcIiwgXCJlbHRcIiwgXCJoX3dcIixcclxuICAgICAgICAgICAgICAgICAgICBcImdhc1wiLCBcImNfd1wiLCBcInN3Z1wiLCBcImhfdF9zaWRcIlxyXG4gICAgICAgICAgICAgICAgXVxyXG4gICAgICAgICAgICB9LCB7XHJcbiAgICAgICAgICAgICAgICBpZDogICAgIDIsXHJcbiAgICAgICAgICAgICAgICBuYW1lOiAgIFwicm9vbVwiLFxyXG4gICAgICAgICAgICAgICAgdGl0bGU6ICBcItCa0L7QvNC90LDRgtGLXCIsXHJcbiAgICAgICAgICAgICAgICBmaWx0ZXJzOiBbXHJcbiAgICAgICAgICAgICAgICAgICAgXCJvcF9zaWRcIiwgXCJwcl9zaWRcIiwgXCJwX21pblwiLCBcInBfbWF4XCIsIFwiY3Vfc2lkXCIsIFwicF9jX21pblwiLCBcInBfY19tYXhcIiwgXCJuX2JcIixcclxuICAgICAgICAgICAgICAgICAgICBcInNfbVwiLCBcImZtbFwiLCBcImZyZ1wiLCBcInJfY19taW5cIiwgXCJyX2NfbWF4XCIsIFwidF9hX21pblwiLCBcInRfYV9tYXhcIiwgXCJmX21pblwiLCBcImZfbWF4XCIsXHJcbiAgICAgICAgICAgICAgICAgICAgXCJtc2RcIiwgXCJncmRcIiwgXCJsZnRcIiwgXCJlbHRcIiwgXCJoX3dcIiwgXCJjX3dcIiwgXCJnYXNcIiwgXCJoX3Rfc2lkXCJcclxuICAgICAgICAgICAgICAgIF1cclxuICAgICAgICAgICAgfSwge1xyXG4gICAgICAgICAgICAgICAgaWQ6ICAgICAzLFxyXG4gICAgICAgICAgICAgICAgbmFtZTogICBcImxhbmRcIixcclxuICAgICAgICAgICAgICAgIHRpdGxlOiAgXCLQl9C10LzQtdC70YzQvdGL0LUg0YPRh9Cw0YHRgtC60LhcIixcclxuICAgICAgICAgICAgICAgIGZpbHRlcnM6IFtcclxuICAgICAgICAgICAgICAgICAgICBcIm9wX3NpZFwiLCBcInBfbWluXCIsIFwicF9tYXhcIiwgXCJjdV9zaWRcIiwgXCJhX21pblwiLCBcImFfbWF4XCIsIFwiZ2FzXCIsIFwiZWx0XCIsIFwid3RyXCIsIFwic3dnXCJcclxuICAgICAgICAgICAgICAgIF1cclxuICAgICAgICAgICAgfSwge1xyXG4gICAgICAgICAgICAgICAgaWQ6ICAgICA0LFxyXG4gICAgICAgICAgICAgICAgbmFtZTogICBcImdhcmFnZVwiLFxyXG4gICAgICAgICAgICAgICAgdGl0bGU6ICBcItCT0LDRgNCw0LbQuFwiLFxyXG4gICAgICAgICAgICAgICAgZmlsdGVyczogW1xyXG4gICAgICAgICAgICAgICAgICAgIFwib3Bfc2lkXCIsIFwicF9taW5cIiwgXCJwX21heFwiLCBcImN1X3NpZFwiLCBcInRfYV9taW5cIiwgXCJ0X2FfbWF4XCJcclxuICAgICAgICAgICAgICAgIF1cclxuICAgICAgICAgICAgfSwge1xyXG4gICAgICAgICAgICAgICAgaWQ6ICAgICA1LFxyXG4gICAgICAgICAgICAgICAgbmFtZTogICBcIm9mZmljZVwiLFxyXG4gICAgICAgICAgICAgICAgdGl0bGU6ICBcItCe0YTQuNGB0YtcIixcclxuICAgICAgICAgICAgICAgIGZpbHRlcnM6IFtcclxuICAgICAgICAgICAgICAgICAgICBcIm9wX3NpZFwiLCBcInBfbWluXCIsIFwicF9tYXhcIiwgXCJjdV9zaWRcIiwgXCJuX2JcIiwgXCJzX21cIiwgXCJ0X2FfbWluXCIsIFwidF9hX21heFwiLFxyXG4gICAgICAgICAgICAgICAgICAgIFwiY19jX21pblwiLCBcImNfY19tYXhcIiwgXCJzY3RcIiwgXCJrdG5cIiwgXCJoX3dcIiwgXCJjX3dcIlxyXG4gICAgICAgICAgICAgICAgXVxyXG4gICAgICAgICAgICB9LCB7XHJcbiAgICAgICAgICAgICAgICBpZDogICAgIDYsXHJcbiAgICAgICAgICAgICAgICBuYW1lOiAgIFwidHJhZGVcIixcclxuICAgICAgICAgICAgICAgIHRpdGxlOiAgXCLQotC+0YDQs9C+0LLRi9C1INC/0L7QvNC10YnQtdC90LjRj1wiLFxyXG4gICAgICAgICAgICAgICAgZmlsdGVyczogW1xyXG4gICAgICAgICAgICAgICAgICAgIFwib3Bfc2lkXCIsIFwicF9taW5cIiwgXCJwX21heFwiLCBcImN1X3NpZFwiLCBcIm5fYlwiLCBcInNfbVwiLCBcImhfYV9taW5cIiwgXCJoX2FfbWF4XCIsXHJcbiAgICAgICAgICAgICAgICAgICAgXCJ0X2FfbWluXCIsIFwidF9hX21heFwiLCBcImJfdF9zaWRcIiwgXCJnYXNcIiwgXCJlbHRcIiwgXCJoX3dcIiwgXCJjX3dcIiwgXCJzd2dcIlxyXG4gICAgICAgICAgICAgICAgXVxyXG4gICAgICAgICAgICB9LCB7XHJcbiAgICAgICAgICAgICAgICBpZDogICAgIDcsXHJcbiAgICAgICAgICAgICAgICBuYW1lOiAgIFwid2FyZWhvdXNlXCIsXHJcbiAgICAgICAgICAgICAgICB0aXRsZTogIFwi0KHQutC70LDQtNGLXCIsXHJcbiAgICAgICAgICAgICAgICBmaWx0ZXJzOiBbXHJcbiAgICAgICAgICAgICAgICAgICAgXCJvcF9zaWRcIiwgXCJwX21pblwiLCBcInBfbWF4XCIsIFwiY3Vfc2lkXCIsIFwibl9iXCIsIFwic19tXCIsIFwiaF9hX21pblwiLCBcImhfYV9tYXhcIixcclxuICAgICAgICAgICAgICAgICAgICBcImdhc1wiLCBcImVsdFwiLCBcImhfd1wiLCBcImNfd1wiLCBcInNfYVwiLCBcImZfYVwiXHJcbiAgICAgICAgICAgICAgICBdXHJcbiAgICAgICAgICAgIH0sIHtcclxuICAgICAgICAgICAgICAgIGlkOiAgICAgOCxcclxuICAgICAgICAgICAgICAgIG5hbWU6ICAgXCJidXNpbmVzc1wiLFxyXG4gICAgICAgICAgICAgICAgdGl0bGU6ICBcItCT0L7RgtC+0LLRi9C5INCx0LjQt9C90LXRgVwiLFxyXG4gICAgICAgICAgICAgICAgZmlsdGVyczogW1xyXG4gICAgICAgICAgICAgICAgICAgIFwib3Bfc2lkXCIsIFwicF9taW5cIiwgXCJwX21heFwiLCBcImN1X3NpZFwiXHJcbiAgICAgICAgICAgICAgICBdXHJcbiAgICAgICAgICAgIH1dO1xyXG4gICAgfVxyXG5cclxuICAgIGdldCByZWFsdHlfdHlwZXMoKSB7XHJcbiAgICAgICAgcmV0dXJuIHRoaXMuX3JlYWx0eV90eXBlcztcclxuICAgIH1cclxufVxyXG4iLCJpbXBvcnQgeyBSZWFsdHlUeXBlc1NlcnZpY2UgfSBmcm9tIFwiLi4vX2NvbW1vbi9iTW9kdWxlcy9UeXBlcy9zZXJ2aWNlcy9yZWFsdHktdHlwZXMuc2VydmljZS5qc1wiO1xyXG5cclxuaW1wb3J0IHsgQXBwQ29udHJvbGxlciB9IGZyb20gXCIuL2NvbnRyb2xsZXJzL2FwcC5jb250cm9sbGVyLmpzXCI7XHJcbmltcG9ydCB7IE1hcENvbnRyb2xsZXIgfSBmcm9tIFwiLi9jb250cm9sbGVycy9tYXAuY29udHJvbGxlci5qc1wiO1xyXG5pbXBvcnQgeyBGaWx0ZXJzUGFuZWxDb250cm9sbGVyIH0gZnJvbSBcIi4vY29udHJvbGxlcnMvZmlsdGVycy1wYW5lbC5jb250cm9sbGVyLmpzXCI7XHJcbmltcG9ydCB7IFBsYWNlQXV0b2NvbXBsZXRlQ29udHJvbGxlciB9IGZyb20gXCIuL2NvbnRyb2xsZXJzL3BsYWNlLWF1dG9jb21wbGV0ZS5jb250cm9sbGVyLmpzXCI7XHJcblxyXG5pbXBvcnQgeyBQYW5lbHNIYW5kbGVyIH0gZnJvbSBcIi4vaGFuZGxlcnMvcGFuZWxzLmhlbmRsZXIuanNcIjtcclxuXHJcbmltcG9ydCB7IEZpbHRlcnNTZXJ2aWNlIH0gZnJvbSBcIi4vc2VydmljZXMvZmlsdGVycy5zZXJ2aWNlLmpzXCI7XHJcbmltcG9ydCB7IE1hcmtlcnNTZXJ2aWNlIH0gZnJvbSBcIi4vc2VydmljZXMvbWFya2Vycy5zZXJ2aWNlLmpzXCI7XHJcbmltcG9ydCB7IHRhYkJvZHlDb2xsYXBzaWJsZSwgdGFiQm9keVNlY3Rpb25Db2xsYXBzaWJsZSB9IGZyb20gXCIuL2RpcmVjdGl2ZXMvdGFicy1wYW5lbC5kaXJlY3RpdmUuanNcIjtcclxuXHJcblxyXG5cclxudmFyIGFwcCA9IGFuZ3VsYXIubW9kdWxlKCdtYXBwaW5vLnBhZ2VzLm1hcCcsIFtcclxuICAgICduZ01hdGVyaWFsJyxcclxuICAgICduZ0Nvb2tpZXMnLFxyXG4gICAgJ25nUmVzb3VyY2UnLFxyXG4gICAgJ3VpLnJvdXRlcidcclxuXSk7XHJcblxyXG5cclxuYXBwLmNvbmZpZyhbJyRzdGF0ZVByb3ZpZGVyJywgJyR1cmxSb3V0ZXJQcm92aWRlcicsICckbG9jYXRpb25Qcm92aWRlcicsICgkc3RhdGVQcm92aWRlciwgJHVybFJvdXRlclByb3ZpZGVyLCAkbG9jYXRpb25Qcm92aWRlcikgPT4ge1xyXG4gICAgJHVybFJvdXRlclByb3ZpZGVyLm90aGVyd2lzZShcIi8wLzAvXCIpO1xyXG5cclxuICAgICRzdGF0ZVByb3ZpZGVyXHJcbiAgICAgICAgLnN0YXRlKCdiYXNlJywge1xyXG4gICAgICAgICAgICB1cmw6IFwiLzpsZWZ0X3BhbmVsX2luZGV4LzpyaWdodF9wYW5lbF9pbmRleC9cIlxyXG4gICAgICAgIH0pO1xyXG5cclxuICAgICRsb2NhdGlvblByb3ZpZGVyLmhhc2hQcmVmaXgoJyEnKTtcclxufV0pO1xyXG5cclxuXHJcblxyXG5hcHAuY29uZmlnKFsnJGludGVycG9sYXRlUHJvdmlkZXInLCAnJHJlc291cmNlUHJvdmlkZXInLCAoJGludGVycG9sYXRlUHJvdmlkZXIsICRyZXNvdXJjZVByb3ZpZGVyKSA9PiB7XHJcbiAgICAgICAgJGludGVycG9sYXRlUHJvdmlkZXIuc3RhcnRTeW1ib2woJ1tbJyk7XHJcbiAgICAgICAgJGludGVycG9sYXRlUHJvdmlkZXIuZW5kU3ltYm9sKCddXScpO1xyXG5cclxuICAgICAgICAkcmVzb3VyY2VQcm92aWRlci5kZWZhdWx0cy5zdHJpcFRyYWlsaW5nU2xhc2hlcyA9IGZhbHNlO1xyXG4gICAgfVxyXG5dKTtcclxuXHJcblxyXG5cclxuYXBwLmNvbmZpZyhbJyRtZFRoZW1pbmdQcm92aWRlcicsICckbWRJY29uUHJvdmlkZXInLCAoJG1kVGhlbWluZ1Byb3ZpZGVyLCAkbWRJY29uUHJvdmlkZXIpID0+IHtcclxuICAgICRtZFRoZW1pbmdQcm92aWRlci5zZXREZWZhdWx0VGhlbWUoJ2RlZmF1bHQnKTtcclxuXHJcbiAgICAkbWRUaGVtaW5nUHJvdmlkZXIudGhlbWUoJ2RlZmF1bHQnKVxyXG4gICAgICAgIC5wcmltYXJ5UGFsZXR0ZSgnYmx1ZScpO1xyXG59XSk7XHJcblxyXG5cclxuXHJcbmFwcC5ydW4oWyckaHR0cCcsICckY29va2llcycsICgkaHR0cCwgJGNvb2tpZXMpID0+IHtcclxuICAgICRodHRwLmRlZmF1bHRzLmhlYWRlcnMuY29tbW9uWydYLUNTUkZUb2tlbiddID0gJGNvb2tpZXMuY3NyZnRva2VuO1xyXG59XSk7XHJcblxyXG5cclxuXHJcbi8qKiBIYW5kbGVycyAqL1xyXG5hcHAuc2VydmljZSgnUGFuZWxzSGFuZGxlcicsIFBhbmVsc0hhbmRsZXIpO1xyXG5cclxuXHJcbi8qKiBiTW9kdWxlIHNlcnZpY2VzICovXHJcbmFwcC5zZXJ2aWNlKCdSZWFsdHlUeXBlc1NlcnZpY2UnLCBSZWFsdHlUeXBlc1NlcnZpY2UpO1xyXG5cclxuXHJcbi8qKiBTZXJ2aWNlcyAqL1xyXG5hcHAuc2VydmljZSgnRmlsdGVyc1NlcnZpY2UnLCBGaWx0ZXJzU2VydmljZSk7XHJcbmFwcC5zZXJ2aWNlKCdNYXJrZXJzU2VydmljZScsIE1hcmtlcnNTZXJ2aWNlKTtcclxuXHJcblxyXG5cclxuLyoqIERpcmVjdGl2ZXMgKi9cclxuYXBwLmRpcmVjdGl2ZSgndGFiQm9keUNvbGxhcHNpYmxlJywgdGFiQm9keUNvbGxhcHNpYmxlKTtcclxuYXBwLmRpcmVjdGl2ZSgndGFiQm9keVNlY3Rpb25Db2xsYXBzaWJsZScsIHRhYkJvZHlTZWN0aW9uQ29sbGFwc2libGUpO1xyXG5cclxuXHJcbi8qKiBDb250cm9sbGVycyAqL1xyXG5hcHAuY29udHJvbGxlcignQXBwQ29udHJvbGxlcicsIEFwcENvbnRyb2xsZXIpO1xyXG5hcHAuY29udHJvbGxlcignRmlsdGVyc1BhbmVsQ29udHJvbGxlcicsIEZpbHRlcnNQYW5lbENvbnRyb2xsZXIpO1xyXG5hcHAuY29udHJvbGxlcignTWFwQ29udHJvbGxlcicsIE1hcENvbnRyb2xsZXIpO1xyXG5hcHAuY29udHJvbGxlcignUGxhY2VBdXRvY29tcGxldGVDb250cm9sbGVyJywgUGxhY2VBdXRvY29tcGxldGVDb250cm9sbGVyKTsiLCJleHBvcnQgY2xhc3MgQXBwQ29udHJvbGxlciB7XHJcbiAgICBjb25zdHJ1Y3Rvcigkc3RhdGUsICRyb290U2NvcGUsICRsb2NhdGlvbiwgcGFuZWxzSGFuZGxlcikge1xyXG5cclxuICAgIH1cclxufVxyXG5cclxuQXBwQ29udHJvbGxlci4kaW5qZWN0ID0gWyckc3RhdGUnLCAnJHJvb3RTY29wZScsICckbG9jYXRpb24nLCAnUGFuZWxzSGFuZGxlciddOyIsImV4cG9ydCBjbGFzcyBGaWx0ZXJzUGFuZWxDb250cm9sbGVyIHtcclxuICAgIGNvbnN0cnVjdG9yKCRzY29wZSwgZmlsdGVyc1NlcnZpY2UsIHJlYWx0eVR5cGVzU2VydmljZSkge1xyXG4gICAgXHR0aGlzLiRzY29wZSBcdFx0PSAkc2NvcGU7XHJcbiAgICBcdFxyXG4gICAgICAgICRzY29wZS5maWx0ZXJzIFx0XHQ9IGZpbHRlcnNTZXJ2aWNlLmZpbHRlcnMucGFuZWxzO1xyXG4gICAgICAgICRzY29wZS5yZWFsdHlUeXBlcyBcdD0gcmVhbHR5VHlwZXNTZXJ2aWNlLnJlYWx0eV90eXBlcztcclxuICAgIH1cclxufVxyXG5cclxuRmlsdGVyc1BhbmVsQ29udHJvbGxlci4kaW5qZWN0ID0gWyckc2NvcGUnLCAnRmlsdGVyc1NlcnZpY2UnLCAnUmVhbHR5VHlwZXNTZXJ2aWNlJ107IiwiZXhwb3J0IGNsYXNzIE1hcENvbnRyb2xsZXIge1xyXG4gICAgY29uc3RydWN0b3IoJHNjb3BlLCBmaWx0ZXJzU2VydmljZSwgbWFya2Vyc1NlcnZpY2UpIHtcclxuICAgICAgICB0aGlzLiRzY29wZSAgICAgICAgID0gJHNjb3BlO1xyXG4gICAgICAgIHRoaXMuZmlsdGVyc1NlcnZpY2UgPSBmaWx0ZXJzU2VydmljZTtcclxuICAgICAgICB0aGlzLm1hcmtlcnNTZXJ2aWNlID0gbWFya2Vyc1NlcnZpY2U7XHJcblxyXG4gICAgICAgIHRoaXMuX21hcCA9IG51bGw7XHJcblxyXG4gICAgICAgIGdvb2dsZS5tYXBzLmV2ZW50LmFkZERvbUxpc3RlbmVyKHdpbmRvdywgXCJsb2FkXCIsIHRoaXMuaW5pdE1hcCgpKTtcclxuXHJcbiAgICAgICAgJHNjb3BlLiRvbigncGFnZXMubWFwLk1hcmtlcnNTZXJ2aWNlLk1hcmtlcnNJc0xvYWRlZCcsICgpID0+IHtcclxuICAgICAgICAgICAgbWFya2Vyc1NlcnZpY2UucGxhY2UodGhpcy5fbWFwKTtcclxuICAgICAgICB9KTtcclxuXHJcbiAgICAgICAgJHNjb3BlLiRvbigncGFnZXMubWFwLlBsYWNlQXV0b2NvbXBsZXRlQ29udHJvbGxlci5QbGFjZUNoYW5nZWQnLCAoZXZlbnQsIHBsYWNlKSA9PiB7XHJcbiAgICAgICAgICAgIHRoaXMucG9zaXRpb25pbmdNYXAocGxhY2UpO1xyXG4gICAgICAgIH0pO1xyXG4gICAgfVxyXG5cclxuXHJcblxyXG4gICAgaW5pdE1hcCgpIHtcclxuICAgICAgICB2YXIgbWFwX29wdGlvbnMgPSB7XHJcbiAgICAgICAgICAgIGNlbnRlcjogICAgIG5ldyBnb29nbGUubWFwcy5MYXRMbmcodGhpcy5maWx0ZXJzU2VydmljZS5maWx0ZXJzLm1hcC5sLnNwbGl0KCcsJylbMF0sIHRoaXMuZmlsdGVyc1NlcnZpY2UuZmlsdGVycy5tYXAubC5zcGxpdCgnLCcpWzFdKSxcclxuICAgICAgICAgICAgem9vbTogICAgICAgcGFyc2VJbnQodGhpcy5maWx0ZXJzU2VydmljZS5maWx0ZXJzLm1hcC56KSxcclxuICAgICAgICAgICAgbWFwVHlwZUlkOiAgZ29vZ2xlLm1hcHMuTWFwVHlwZUlkLlJPQURNQVAsXHJcbiAgICAgICAgICAgIGRpc2FibGVEZWZhdWx0VUk6IHRydWUsXHJcbiAgICAgICAgICAgIHN0eWxlczogW3tcImZlYXR1cmVUeXBlXCI6XCJhbGxcIixcInN0eWxlcnNcIjpbe1wic2F0dXJhdGlvblwiOjB9LHtcImh1ZVwiOlwiI2U3ZWNmMFwifV19LHtcImZlYXR1cmVUeXBlXCI6XCJyb2FkXCIsXCJzdHlsZXJzXCI6W3tcInNhdHVyYXRpb25cIjotNzB9XX0se1wiZmVhdHVyZVR5cGVcIjpcInRyYW5zaXRcIixcInN0eWxlcnNcIjpbe1widmlzaWJpbGl0eVwiOlwib2ZmXCJ9XX0se1wiZmVhdHVyZVR5cGVcIjpcInBvaVwiLFwic3R5bGVyc1wiOlt7XCJ2aXNpYmlsaXR5XCI6XCJvZmZcIn1dfSx7XCJmZWF0dXJlVHlwZVwiOlwid2F0ZXJcIixcInN0eWxlcnNcIjpbe1widmlzaWJpbGl0eVwiOlwic2ltcGxpZmllZFwifSx7XCJzYXR1cmF0aW9uXCI6LTYwfV19XVxyXG4gICAgICAgIH07XHJcblxyXG4gICAgICAgIHRoaXMuX21hcCA9IG5ldyBnb29nbGUubWFwcy5NYXAoZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoXCJtYXBcIiksIG1hcF9vcHRpb25zKTtcclxuXHJcbiAgICAgICAgZ29vZ2xlLm1hcHMuZXZlbnQuYWRkTGlzdGVuZXIodGhpcy5fbWFwLCAnaWRsZScsICgpID0+IHtcclxuICAgICAgICAgICAgdGhpcy5maWx0ZXJzU2VydmljZS51cGRhdGUoJ21hcCcsIHtcclxuICAgICAgICAgICAgICAgIHo6IHRoaXMuX21hcC5nZXRab29tKCksXHJcbiAgICAgICAgICAgICAgICB2OiB0aGlzLl9tYXAuZ2V0Qm91bmRzKCksXHJcbiAgICAgICAgICAgICAgICBsOiB0aGlzLl9tYXAuZ2V0Q2VudGVyKCkudG9VcmxWYWx1ZSgpXHJcbiAgICAgICAgICAgIH0pO1xyXG4gICAgICAgIH0pO1xyXG4gICAgfVxyXG5cclxuXHJcblxyXG4gICAgcG9zaXRpb25pbmdNYXAocGxhY2UpIHtcclxuICAgICAgICBpZiAoIXBsYWNlLmdlb21ldHJ5KVxyXG4gICAgICAgICAgICByZXR1cm47XHJcblxyXG4gICAgICAgIGlmIChwbGFjZS5nZW9tZXRyeS52aWV3cG9ydCkge1xyXG4gICAgICAgICAgICB0aGlzLl9tYXAuZml0Qm91bmRzKHBsYWNlLmdlb21ldHJ5LnZpZXdwb3J0KTtcclxuICAgICAgICB9IGVsc2Uge1xyXG4gICAgICAgICAgICB0aGlzLl9tYXAucGFuVG8ocGxhY2UuZ2VvbWV0cnkubG9jYXRpb24pO1xyXG4gICAgICAgICAgICB0aGlzLl9tYXAuc2V0Wm9vbSgxNyk7XHJcbiAgICAgICAgfVxyXG4gICAgfVxyXG59XHJcblxyXG5NYXBDb250cm9sbGVyLiRpbmplY3QgPSBbJyRzY29wZScsICdGaWx0ZXJzU2VydmljZScsICdNYXJrZXJzU2VydmljZSddOyIsImV4cG9ydCBjbGFzcyBQbGFjZUF1dG9jb21wbGV0ZUNvbnRyb2xsZXIge1xyXG4gICAgY29uc3RydWN0b3IoJHNjb3BlLCAkcm9vdFNjb3BlLCBmaWx0ZXJzU2VydmljZSkge1xyXG4gICAgICAgIHZhciBzZWxmID0gdGhpcztcclxuICAgICAgICB0aGlzLl9hdXRvY29tcGxldGUgPSBudWxsO1xyXG4gICAgICAgIHRoaXMuX2F1dG9jb21wbGV0ZUlucHV0ID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoXCJwbGFjZS1hdXRvY29tcGxldGVcIik7XHJcblxyXG5cclxuICAgICAgICAvKiogTGlzdGVuIGV2ZW50cyAqL1xyXG4gICAgICAgIGdvb2dsZS5tYXBzLmV2ZW50LmFkZERvbUxpc3RlbmVyKHdpbmRvdywgXCJsb2FkXCIsICgpID0+IHRoaXMuaW5pdEF1dG9jb21wbGV0ZShzZWxmKSk7XHJcblxyXG4gICAgICAgICRzY29wZS4kb24oJ3BhZ2VzLm1hcC5GaWx0ZXJzU2VydmljZS5VcGRhdGVkRnJvbVVybCcsIChldmVudCwgZmlsdGVycykgPT4ge1xyXG4gICAgICAgICAgICB0aGlzLl9hdXRvY29tcGxldGVJbnB1dC52YWx1ZSA9IGZpbHRlcnMubWFwLmM7XHJcbiAgICAgICAgfSk7XHJcbiAgICB9XHJcblxyXG5cclxuXHJcbiAgICBpbml0QXV0b2NvbXBsZXRlKHNlbGYpIHtcclxuICAgICAgICBzZWxmLl9hdXRvY29tcGxldGUgPSBuZXcgZ29vZ2xlLm1hcHMucGxhY2VzLkF1dG9jb21wbGV0ZSh0aGlzLl9hdXRvY29tcGxldGVJbnB1dCwge1xyXG4gICAgICAgICAgICBjb21wb25lbnRSZXN0cmljdGlvbnM6IHtcclxuICAgICAgICAgICAgICAgIGNvdW50cnk6IFwidWFcIlxyXG4gICAgICAgICAgICB9XHJcbiAgICAgICAgfSk7XHJcblxyXG4gICAgICAgIGdvb2dsZS5tYXBzLmV2ZW50LmFkZExpc3RlbmVyKHNlbGYuX2F1dG9jb21wbGV0ZSwgJ3BsYWNlX2NoYW5nZWQnLCBmdW5jdGlvbigpIHtcclxuICAgICAgICAgICAgc2VsZi5maWx0ZXJzU2VydmljZS51cGRhdGUoJ21hcCcsIHtcclxuICAgICAgICAgICAgICAgIGM6IHNlbGYuX2F1dG9jb21wbGV0ZS5nZXRQbGFjZSgpLmZvcm1hdHRlZF9hZGRyZXNzXHJcbiAgICAgICAgICAgIH0pO1xyXG5cclxuICAgICAgICAgICAgc2VsZi4kcm9vdFNjb3BlLiRicm9hZGNhc3QoJ3BhZ2VzLm1hcC5QbGFjZUF1dG9jb21wbGV0ZUNvbnRyb2xsZXIuUGxhY2VDaGFuZ2VkJywgc2VsZi5fYXV0b2NvbXBsZXRlLmdldFBsYWNlKCkpO1xyXG4gICAgICAgICAgICAvL1xyXG4gICAgICAgICAgICAvL2lmICghc2VsZi4kc2NvcGUuJCRwaGFzZSlcclxuICAgICAgICAgICAgLy8gICAgc2VsZi4kc2NvcGUuJGFwcGx5KCk7XHJcbiAgICAgICAgfSk7XHJcbiAgICB9XHJcbn1cclxuXHJcblBsYWNlQXV0b2NvbXBsZXRlQ29udHJvbGxlci4kaW5qZWN0ID0gWyckc2NvcGUnLCAnJHJvb3RTY29wZScsICdGaWx0ZXJzU2VydmljZSddOyIsImV4cG9ydCBmdW5jdGlvbiB0YWJCb2R5Q29sbGFwc2libGUoKSB7XHJcbiAgICByZXR1cm4ge1xyXG4gICAgICAgIHJlc3RyaWN0OiAnRScsXHJcblxyXG4gICAgICAgIGxpbms6IGZ1bmN0aW9uKHNjb3BlLCBlbGVtZW50LCBhdHRycywgbW9kZWxDdHJsKSB7XHJcbiAgICAgICAgICAgIGFuZ3VsYXIuZWxlbWVudCgnW3RvZ2dsZS10YWItYm9keV0nKS5vbignY2xpY2snLCAoX2VsZW1lbnQpID0+IHtcclxuICAgICAgICAgICAgICAgIGFuZ3VsYXIuZWxlbWVudChfZWxlbWVudC5jdXJyZW50VGFyZ2V0KS50b2dnbGVDbGFzcygnLXRhYi1ib2R5LWNsb3NlZCcpO1xyXG4gICAgICAgICAgICAgICAgYW5ndWxhci5lbGVtZW50KGVsZW1lbnQpLnRvZ2dsZUNsYXNzKCctY2xvc2VkJyk7XHJcbiAgICAgICAgICAgIH0pO1xyXG4gICAgICAgIH1cclxuICAgIH07XHJcbn1cclxuXHJcblxyXG5leHBvcnQgZnVuY3Rpb24gdGFiQm9keVNlY3Rpb25Db2xsYXBzaWJsZSgpIHtcclxuICAgIHJldHVybiB7XHJcbiAgICAgICAgcmVzdHJpY3Q6ICdFJyxcclxuXHJcbiAgICAgICAgbGluazogZnVuY3Rpb24oc2NvcGUsIGVsZW1lbnQsIGF0dHJzLCBtb2RlbEN0cmwpIHtcclxuICAgICAgICAgICAgYW5ndWxhci5lbGVtZW50KCdbdG9nZ2xlLXRhYi1ib2R5LXNlY3Rpb25dJykub24oJ2NsaWNrJywgKF9lbGVtZW50KSA9PiB7XHJcbiAgICAgICAgICAgICAgICBhbmd1bGFyLmVsZW1lbnQoX2VsZW1lbnQuY3VycmVudFRhcmdldCkudG9nZ2xlQ2xhc3MoJy10YWItYm9keS1zZWN0aW9uLWNsb3NlZCcpO1xyXG4gICAgICAgICAgICAgICAgYW5ndWxhci5lbGVtZW50KGVsZW1lbnQpLnRvZ2dsZUNsYXNzKCctY2xvc2VkJyk7XHJcbiAgICAgICAgICAgIH0pO1xyXG4gICAgICAgIH1cclxuICAgIH07XHJcbn0iLCJleHBvcnQgY2xhc3MgUGFuZWxzSGFuZGxlciB7XHJcbiAgICBjb25zdHJ1Y3Rvcigkc3RhdGUsICRzdGF0ZVBhcmFtcywgJHJvb3RTY29wZSwgJGxvY2F0aW9uKSB7XHJcbiAgICAgICAgdGhpcy4kc3RhdGUgICAgICAgICA9ICRzdGF0ZTtcclxuICAgICAgICB0aGlzLiRzdGF0ZVBhcmFtcyAgID0gJHN0YXRlUGFyYW1zO1xyXG4gICAgICAgIHRoaXMuJHJvb3RTY29wZSAgICAgPSAkcm9vdFNjb3BlO1xyXG4gICAgICAgIHRoaXMuJGxvY2F0aW9uICAgICAgPSAkbG9jYXRpb247XHJcblxyXG4gICAgICAgIHRoaXMuX2xvY2F0aW9uX3NlYXJjaCA9IG51bGw7XHJcblxyXG4gICAgICAgICRyb290U2NvcGUucGFuZWxzSW5kZXggPSB7XHJcbiAgICAgICAgICAgIGxlZnRQYW5lbEluZGV4OiAgICAgMCxcclxuICAgICAgICAgICAgcmlnaHRQYW5lbEluZGV4OiAgICAwXHJcbiAgICAgICAgfTtcclxuXHJcbiAgICAgICAgJHJvb3RTY29wZS4kd2F0Y2goJ3BhbmVsc0luZGV4LmxlZnRQYW5lbEluZGV4JywgKG5ld1ZhbHVlLCBvbGRWYWx1ZSkgPT4ge1xyXG4gICAgICAgICAgICAkc3RhdGUuZ28oJ2Jhc2UnLCB7IGxlZnRfcGFuZWxfaW5kZXg6IG5ld1ZhbHVlIH0pO1xyXG4gICAgICAgIH0sIHRydWUpO1xyXG4gICAgICAgIFxyXG4gICAgICAgICRyb290U2NvcGUuJHdhdGNoKCdwYW5lbHNJbmRleC5yaWdodFBhbmVsSW5kZXgnLCAobmV3VmFsdWUsIG9sZFZhbHVlKSA9PiB7XHJcbiAgICAgICAgICAgICRzdGF0ZS5nbygnYmFzZScsIHsgcmlnaHRfcGFuZWxfaW5kZXg6IG5ld1ZhbHVlIH0pO1xyXG4gICAgICAgIH0sIHRydWUpO1xyXG5cclxuXHJcbiAgICAgICAgLyoqXHJcbiAgICAgICAgICog0JLRltC00L3QvtCy0LvRjtGU0LzQviDRhNGW0LvRjNGC0YDQuCDQsiDRg9GA0LvRliDQv9GW0YHQu9GPINC30LzRltC90Lgg0L/QsNC90LXQu9GWXHJcbiAgICAgICAgICoqL1xyXG4gICAgICAgIHZhciBfb25jZVVwZGF0ZVRhYnNGcm9tVXJsID0gXy5vbmNlKHRoaXMub25jZVVwZGF0ZVRhYnNGcm9tVXJsKTtcclxuICAgICAgICAkcm9vdFNjb3BlLiRvbignJHN0YXRlQ2hhbmdlU3RhcnQnLCAoKSA9PiB7XHJcbiAgICAgICAgICAgIGlmICghXy5pc051bGwoJGxvY2F0aW9uLnNlYXJjaCgpKSkge1xyXG4gICAgICAgICAgICAgICAgdGhpcy5fbG9jYXRpb25fc2VhcmNoID0gJGxvY2F0aW9uLnNlYXJjaCgpO1xyXG4gICAgICAgICAgICB9XHJcbiAgICAgICAgfSk7XHJcbiAgICAgICAgJHJvb3RTY29wZS4kb24oJyRzdGF0ZUNoYW5nZVN1Y2Nlc3MnLCAoKSA9PiB7XHJcbiAgICAgICAgICAgIF9vbmNlVXBkYXRlVGFic0Zyb21VcmwodGhpcyk7XHJcblxyXG4gICAgICAgICAgICBpZiAoIV8uaXNOdWxsKHRoaXMuX2xvY2F0aW9uX3NlYXJjaCkpIHtcclxuICAgICAgICAgICAgICAgICRsb2NhdGlvbi5zZWFyY2godGhpcy5fbG9jYXRpb25fc2VhcmNoKTtcclxuICAgICAgICAgICAgfVxyXG4gICAgICAgIH0pO1xyXG4gICAgfVxyXG5cclxuXHJcblxyXG4gICAgb25jZVVwZGF0ZVRhYnNGcm9tVXJsKHNlbGYpIHtcclxuICAgICAgICBzZWxmLiRyb290U2NvcGUucGFuZWxzSW5kZXggPSB7XHJcbiAgICAgICAgICAgIGxlZnRQYW5lbEluZGV4OiAgICAgc2VsZi4kc3RhdGVQYXJhbXMubGVmdF9wYW5lbF9pbmRleCAgICB8fCAwLFxyXG4gICAgICAgICAgICByaWdodFBhbmVsSW5kZXg6ICAgIHNlbGYuJHN0YXRlUGFyYW1zLnJpZ2h0X3BhbmVsX2luZGV4ICAgfHwgMFxyXG4gICAgICAgIH07XHJcbiAgICB9XHJcbn1cclxuXHJcblBhbmVsc0hhbmRsZXIuJGluamVjdCA9IFsnJHN0YXRlJywgJyRzdGF0ZVBhcmFtcycsICckcm9vdFNjb3BlJywnJGxvY2F0aW9uJ107IiwiZXhwb3J0IGNsYXNzIEZpbHRlcnNTZXJ2aWNlIHtcclxuICAgIGNvbnN0cnVjdG9yKCRyb290U2NvcGUsICR0aW1lb3V0LCAkbG9jYXRpb24sIHJlYWx0eVR5cGVzU2VydmljZSkge1xyXG4gICAgICAgIHRoaXMuJHJvb3RTY29wZSAgICAgPSAkcm9vdFNjb3BlO1xyXG4gICAgICAgIHRoaXMuJHRpbWVvdXQgICAgICAgPSAkdGltZW91dDtcclxuICAgICAgICB0aGlzLiRsb2NhdGlvbiAgICAgID0gJGxvY2F0aW9uO1xyXG4gICAgICAgIHRoaXMucmVhbHR5VHlwZXNTZXJ2aWNlID0gcmVhbHR5VHlwZXNTZXJ2aWNlO1xyXG5cclxuICAgICAgICB0aGlzLl9maWx0ZXJzX2Zvcl9sb2FkX21hcmtlcnMgPSB7XHJcbiAgICAgICAgICAgIHpvb206IG51bGwsXHJcbiAgICAgICAgICAgIHZpZXdwb3J0OiBudWxsLFxyXG4gICAgICAgICAgICBmaWx0ZXJzOiBbXVxyXG4gICAgICAgIH07XHJcbiAgICAgICAgdGhpcy5fZmlsdGVycyA9IHtcclxuICAgICAgICAgICAgbWFwOiB7XHJcbiAgICAgICAgICAgICAgICBjOiBudWxsLCAgICAvLyBjaXR5XHJcbiAgICAgICAgICAgICAgICBsOiBcIjQ4LjQ1NTkzNSwzNC40MTI4NVwiLCAgICAvLyBsYXRfbG5nXHJcbiAgICAgICAgICAgICAgICB2OiBudWxsLCAgICAvLyB2aWV3cG9ydFxyXG4gICAgICAgICAgICAgICAgejogNiAgICAgLy8gem9vbVxyXG4gICAgICAgICAgICB9LFxyXG4gICAgICAgICAgICBwYW5lbHM6IHtcclxuICAgICAgICAgICAgICAgIHJlZDoge1xyXG4gICAgICAgICAgICAgICAgICAgIHJfdF9zaWQ6IG51bGxcclxuICAgICAgICAgICAgICAgIH0sXHJcbiAgICAgICAgICAgICAgICBibHVlOiB7XHJcbiAgICAgICAgICAgICAgICAgICAgYl90X3NpZDogbnVsbFxyXG4gICAgICAgICAgICAgICAgfSxcclxuICAgICAgICAgICAgICAgIGdyZWVuOiB7XHJcbiAgICAgICAgICAgICAgICAgICAgZ190X3NpZDogbnVsbFxyXG4gICAgICAgICAgICAgICAgfSxcclxuICAgICAgICAgICAgICAgIHllbGxvdzoge1xyXG4gICAgICAgICAgICAgICAgICAgIHlfdF9zaWQ6IG51bGxcclxuICAgICAgICAgICAgICAgIH1cclxuICAgICAgICAgICAgfSxcclxuICAgICAgICAgICAgYmFzZToge1xyXG4gICAgICAgICAgICAgICAgLy8g0JfQsNCz0LDQu9GM0L3RllxyXG4gICAgICAgICAgICAgICAgb3Bfc2lkOiAgICAgMCwgIC8vIG9wZXJhdGlvbl9zaWRcclxuXHJcbiAgICAgICAgICAgICAgICAvLyDQlNGA0L7Qv9C00LDRg9C90LhcclxuICAgICAgICAgICAgICAgIGN1X3NpZDogICAgIDAsICAvLyBjdXJyZW5jeV9zaWRcclxuICAgICAgICAgICAgICAgIGhfdF9zaWQ6ICAgIDAsICAvLyBoZWF0aW5nX3R5cGVfc2lkXHJcbiAgICAgICAgICAgICAgICBwcl9zaWQ6ICAgICAwLCAgLy8gcGVyaW9kX3NpZFxyXG4gICAgICAgICAgICAgICAgcGxfc2lkOiAgICAgMCwgIC8vIHBsYW5pbmdfc2lkXHJcbiAgICAgICAgICAgICAgICBiX3Rfc2lkOiAgICAwLCAgLy8gYnVpbGRpbmdfdHlwZV9zaWRcclxuXHJcbiAgICAgICAgICAgICAgICAvLyDQn9C+0LvRjyDQstCy0L7QtNGDXHJcbiAgICAgICAgICAgICAgICBwX21pbjogICAgICBudWxsLCAgIC8vIHByaWNlX21pblxyXG4gICAgICAgICAgICAgICAgcF9tYXg6ICAgICAgbnVsbCwgICAvLyBwcmljZV9tYXhcclxuICAgICAgICAgICAgICAgIHJfY19taW46ICAgIG51bGwsICAgLy8gcm9vbXNfY291bnRfbWluXHJcbiAgICAgICAgICAgICAgICByX2NfbWF4OiAgICBudWxsLCAgIC8vIHJvb21zX2NvdW50X21heFxyXG4gICAgICAgICAgICAgICAgZl9jX21pbjogICAgbnVsbCwgICAvLyBmbG9vcnNfY291bnRfbWluXHJcbiAgICAgICAgICAgICAgICBmX2NfbWF4OiAgICBudWxsLCAgIC8vIGZsb29yc19jb3VudF9tYXhcclxuICAgICAgICAgICAgICAgIHBfY19taW46ICAgIG51bGwsICAgLy8gcGVyc29uc19jb3VudF9taW5cclxuICAgICAgICAgICAgICAgIHBfY19tYXg6ICAgIG51bGwsICAgLy8gcGVyc29uc19jb3VudF9tYXhcclxuICAgICAgICAgICAgICAgIHRfYV9taW46ICAgIG51bGwsICAgLy8gdG90YWxfYXJlYV9taW5cclxuICAgICAgICAgICAgICAgIHRfYV9tYXg6ICAgIG51bGwsICAgLy8gdG90YWxfYXJlYV9tYXhcclxuICAgICAgICAgICAgICAgIGZfbWluOiAgICAgIG51bGwsICAgLy8gZmxvb3JfbWluXHJcbiAgICAgICAgICAgICAgICBmX21heDogICAgICBudWxsLCAgIC8vIGZsb29yX21heFxyXG4gICAgICAgICAgICAgICAgaF9hX21pbjogICAgbnVsbCwgICAvLyBoYWxsc19hcmVhX21pblxyXG4gICAgICAgICAgICAgICAgaF9hX21heDogICAgbnVsbCwgICAvLyBoYWxsc19hcmVhX21heFxyXG4gICAgICAgICAgICAgICAgY19jX21pbjogICAgbnVsbCwgICAvLyBjYWJpbmV0c19jb3VudF9taW5cclxuICAgICAgICAgICAgICAgIGNfY19tYXg6ICAgIG51bGwsICAgLy8gY2FiaW5ldHNfY291bnRfbWF4XHJcbiAgICAgICAgICAgICAgICBoX2NfbWluOiAgICBudWxsLCAgIC8vIGhhbGxzX2NvdW50X21pblxyXG4gICAgICAgICAgICAgICAgaF9jX21heDogICAgbnVsbCwgICAvLyBoYWxsc19jb3VudF9tYXhcclxuICAgICAgICAgICAgICAgIGNfaF9taW46ICAgIG51bGwsICAgLy8gY2VpbGluZ19oZWlnaHRfbWluXHJcbiAgICAgICAgICAgICAgICBjX2hfbWF4OiAgICBudWxsLCAgIC8vIGNlaWxpbmdfaGVpZ2h0X21heFxyXG4gICAgICAgICAgICAgICAgYV9taW46ICAgICAgbnVsbCwgICAvLyBhcmVhX21pblxyXG4gICAgICAgICAgICAgICAgYV9tYXg6ICAgICAgbnVsbCwgICAvLyBhcmVhX21heFxyXG5cclxuICAgICAgICAgICAgICAgIC8vINCn0LXQutCx0L7QutGB0LhcclxuICAgICAgICAgICAgICAgIG5fYjogICAgdHJ1ZSwgICAvLyBuZXdfYnVpbGRpbmdzXHJcbiAgICAgICAgICAgICAgICBzX206ICAgIHRydWUsICAgLy8gc2Vjb25kYXJ5X21hcmtldFxyXG4gICAgICAgICAgICAgICAgZm1sOiAgICBmYWxzZSwgIC8vIGZhbWlseVxyXG4gICAgICAgICAgICAgICAgZnJnOiAgICBmYWxzZSwgIC8vIGZvcmVpZ25lcnNcclxuICAgICAgICAgICAgICAgIGVsdDogICAgZmFsc2UsICAvLyBlbGVjdHJpY2l0eVxyXG4gICAgICAgICAgICAgICAgZ2FzOiAgICBmYWxzZSwgIC8vIGdhc1xyXG4gICAgICAgICAgICAgICAgaF93OiAgICBmYWxzZSwgIC8vIGhvdF93YXRlclxyXG4gICAgICAgICAgICAgICAgY193OiAgICBmYWxzZSwgIC8vIGNvbGRfd2F0ZXJcclxuICAgICAgICAgICAgICAgIHN3ZzogICAgZmFsc2UsICAvLyBzZXdlcmFnZVxyXG4gICAgICAgICAgICAgICAgbGZ0OiAgICBmYWxzZSwgIC8vIGxpZnRcclxuICAgICAgICAgICAgICAgIHNjdDogICAgZmFsc2UsICAvLyBzZWN1cml0eVxyXG4gICAgICAgICAgICAgICAga3RuOiAgICBmYWxzZSwgIC8vIGtpdGNoZW5cclxuICAgICAgICAgICAgICAgIHNfYTogICAgZmFsc2UsICAvLyBzZWN1cml0eV9hbGFybVxyXG4gICAgICAgICAgICAgICAgZl9hOiAgICBmYWxzZSwgIC8vIGZpcmVfYWxhcm1cclxuICAgICAgICAgICAgICAgIHBpdDogICAgZmFsc2UsICAvLyBwaXRcclxuICAgICAgICAgICAgICAgIHd0cjogICAgZmFsc2UsICAvLyB3YXRlclxyXG4gICAgICAgICAgICAgICAgbXNkOiAgICB0cnVlLCAgIC8vIG1hbnNhcmRcclxuICAgICAgICAgICAgICAgIGdyZDogICAgdHJ1ZSAgICAvLyBncm91bmRcclxuICAgICAgICAgICAgfVxyXG4gICAgICAgIH07XHJcbiAgICAgICAgdGhpcy51cGRhdGVGaWx0ZXJzRnJvbVVybCgpO1xyXG4gICAgfVxyXG5cclxuXHJcblxyXG4gICAgdXBkYXRlKGZpbHRlcl9vYmplY3RfbmFtZSwgZmlsdGVyc19vYmplY3QpIHtcclxuICAgICAgICBmb3IgKHZhciBmaWx0ZXIgaW4gZmlsdGVyc19vYmplY3QpIHtcclxuICAgICAgICAgICAgaWYgKGZpbHRlcnNfb2JqZWN0Lmhhc093blByb3BlcnR5KGZpbHRlcikpIHtcclxuICAgICAgICAgICAgICAgIHRoaXMuX2ZpbHRlcnNbZmlsdGVyX29iamVjdF9uYW1lXVtmaWx0ZXJdID0gZmlsdGVyc19vYmplY3RbZmlsdGVyXTtcclxuICAgICAgICAgICAgfVxyXG4gICAgICAgIH1cclxuXHJcbiAgICAgICAgdGhpcy51cGRhdGVVcmxGcm9tRmlsdGVycygpO1xyXG4gICAgICAgIHRoaXMuY3JlYXRlRm9ybWF0dGVkT2JqZWN0Rm9yTG9hZE1hcmtlcnMoKTtcclxuXHJcbiAgICAgICAgdGhpcy4kdGltZW91dCgoKSA9PiB0aGlzLiRyb290U2NvcGUuJGJyb2FkY2FzdCgncGFnZXMubWFwLkZpbHRlcnNTZXJ2aWNlLkZpbHRlcnNVcGRhdGVkJywgdGhpcy5fZmlsdGVycykpO1xyXG4gICAgfVxyXG5cclxuXHJcbiAgICBnZXQgZmlsdGVycygpIHtcclxuICAgICAgICByZXR1cm4gdGhpcy5fZmlsdGVycztcclxuICAgIH1cclxuXHJcblxyXG5cclxuICAgIGNyZWF0ZUZpbHRlcnNGb3JQYW5lbChwYW5lbF9jb2xvcikge1xyXG4gICAgICAgIHZhciBzZWxmID0gdGhpcyxcclxuICAgICAgICAgICAgcGFuZWxfcHJlZml4ICAgICAgICA9IHBhbmVsX2NvbG9yLnRvU3RyaW5nKCkuc3Vic3RyaW5nKDAsIDEpICsgXCJfXCIsXHJcbiAgICAgICAgICAgIHR5cGVfc2lkICAgICAgICAgICAgPSB0aGlzLl9maWx0ZXJzLnBhbmVsc1twYW5lbF9jb2xvcl1bcGFuZWxfcHJlZml4ICsgJ3Rfc2lkJ10sXHJcbiAgICAgICAgICAgIGxvY2F0aW9uX3NlYXJjaCAgICAgPSB0aGlzLiRsb2NhdGlvbi5zZWFyY2goKTtcclxuXHJcblxyXG4gICAgICAgIGlmIChfLmlzTnVsbCh0eXBlX3NpZCkpIHtcclxuICAgICAgICAgICAgLy8g0J7Rh9C40YnQsNGU0LzQviDQvtCx0ZTQutGCINC3INGE0ZbQu9GM0YLRgNCw0LzQuFxyXG4gICAgICAgICAgICB0aGlzLl9maWx0ZXJzLnBhbmVsc1twYW5lbF9jb2xvcl0gPSB7fTtcclxuXHJcbiAgICAgICAgICAgIC8vINCh0YLQstC+0YDRjtGU0LzQviDQv9Cw0YDQsNC80LXRgtGAINC3INGC0LjQv9C+0Lwg0L7Qs9C+0LvQvtGI0LXQvdC90Y8g0LIg0L7QsdGU0LrRgtGWINC3INGE0ZbQu9GM0YLRgNCw0LzQuFxyXG4gICAgICAgICAgICB0aGlzLl9maWx0ZXJzLnBhbmVsc1twYW5lbF9jb2xvcl1bcGFuZWxfcHJlZml4ICsgXCJ0X3NpZFwiXSA9IHR5cGVfc2lkO1xyXG5cclxuICAgICAgICAgICAgLy8g0JLQuNC00LDQu9GP0ZTQvNC+INGE0ZbQu9GM0YLRgNC4INC3INGD0YDQu9CwXHJcbiAgICAgICAgICAgIGZvciAodmFyIHNfa2V5IGluIGxvY2F0aW9uX3NlYXJjaCkge1xyXG4gICAgICAgICAgICAgICAgaWYgKGxvY2F0aW9uX3NlYXJjaC5oYXNPd25Qcm9wZXJ0eShzX2tleSkpIHtcclxuICAgICAgICAgICAgICAgICAgICBpZiAoc19rZXkubWF0Y2gobmV3IFJlZ0V4cCgnXicgKyBwYW5lbF9wcmVmaXgsICdtJykpKSB7XHJcbiAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMuJGxvY2F0aW9uLnNlYXJjaChzX2tleSwgbnVsbCk7XHJcbiAgICAgICAgICAgICAgICAgICAgfVxyXG4gICAgICAgICAgICAgICAgfVxyXG4gICAgICAgICAgICB9XHJcbiAgICAgICAgfVxyXG5cclxuXHJcbiAgICAgICAgLy8g0KHRgtCy0L7RgNGO0ZTQvNC+INC90LDQsdGW0YAg0YTRltC70YzRgtGA0ZbQsiDQtNC70Y8g0L/QsNC90LXQu9GWINC30LAg0L3QsNCx0L7RgNC+0LxcclxuICAgICAgICBpZiAoIV8uaXNOdWxsKHR5cGVfc2lkKSkge1xyXG4gICAgICAgICAgICB2YXIgcmVhbHR5X3R5cGVfZmlsdGVycyA9IF8ud2hlcmUoc2VsZi5yZWFsdHlUeXBlc1NlcnZpY2UucmVhbHR5X3R5cGVzLCB7ICdpZCc6IHR5cGVfc2lkIH0pWzBdLmZpbHRlcnM7XHJcblxyXG4gICAgICAgICAgICBmb3IgKHZhciBpID0gMCwgbGVuID0gcmVhbHR5X3R5cGVfZmlsdGVycy5sZW5ndGg7IGkgPCBsZW47IGkrKykge1xyXG4gICAgICAgICAgICAgICAgdmFyIGZpbHRlcl9uYW1lID0gcGFuZWxfcHJlZml4ICsgcmVhbHR5X3R5cGVfZmlsdGVyc1tpXTtcclxuXHJcbiAgICAgICAgICAgICAgICBpZiAoXy5pc1VuZGVmaW5lZCh0aGlzLl9maWx0ZXJzLnBhbmVsc1twYW5lbF9jb2xvcl1bZmlsdGVyX25hbWVdKSkge1xyXG4gICAgICAgICAgICAgICAgICAgIHRoaXMuX2ZpbHRlcnMucGFuZWxzW3BhbmVsX2NvbG9yXVtmaWx0ZXJfbmFtZV0gPSB0aGlzLl9maWx0ZXJzLmJhc2VbcmVhbHR5X3R5cGVfZmlsdGVyc1tpXV07XHJcbiAgICAgICAgICAgICAgICB9XHJcbiAgICAgICAgICAgIH1cclxuICAgICAgICB9XHJcblxyXG4gICAgICAgIHRoaXMuJHRpbWVvdXQoKCkgPT4gdGhpcy4kcm9vdFNjb3BlLiRicm9hZGNhc3QoJ3BhZ2VzLm1hcC5GaWx0ZXJzU2VydmljZS5GaWx0ZXJzVXBkYXRlZCcsIHRoaXMuX2ZpbHRlcnMpKTtcclxuICAgIH1cclxuXHJcblxyXG5cclxuICAgIHVwZGF0ZUZpbHRlcnNGcm9tVXJsKCkge1xyXG4gICAgICAgIHZhciBsb2NhdGlvbl9zZWFyY2ggPSB0aGlzLiRsb2NhdGlvbi5zZWFyY2goKSxcclxuICAgICAgICAgICAgZmlsdGVyc19wYW5lbHMgPSB0aGlzLl9maWx0ZXJzLnBhbmVscztcclxuXHJcbiAgICAgICAgZm9yICh2YXIga2V5IGluIGxvY2F0aW9uX3NlYXJjaCkge1xyXG4gICAgICAgICAgICBpZiAobG9jYXRpb25fc2VhcmNoLmhhc093blByb3BlcnR5KGtleSkpIHtcclxuXHJcbiAgICAgICAgICAgICAgICBpZiAoa2V5LnRvU3RyaW5nKCkgPT09IFwidG9rZW5cIikge1xyXG4gICAgICAgICAgICAgICAgICAgIGNvbnRpbnVlO1xyXG4gICAgICAgICAgICAgICAgfVxyXG4gICAgICAgICAgICAgICAgaWYgKGxvY2F0aW9uX3NlYXJjaFtrZXldID09PSAndHJ1ZScpIHtcclxuICAgICAgICAgICAgICAgICAgICBsb2NhdGlvbl9zZWFyY2hba2V5XSA9IHRydWU7XHJcbiAgICAgICAgICAgICAgICB9XHJcbiAgICAgICAgICAgICAgICBpZiAobG9jYXRpb25fc2VhcmNoW2tleV0gPT09ICdmYWxzZScpIHtcclxuICAgICAgICAgICAgICAgICAgICBsb2NhdGlvbl9zZWFyY2hba2V5XSA9IGZhbHNlO1xyXG4gICAgICAgICAgICAgICAgfVxyXG4gICAgICAgICAgICAgICAgaWYgKGtleS50b1N0cmluZygpLmluZGV4T2YoXCJfc2lkXCIpICE9PSAtMSkge1xyXG4gICAgICAgICAgICAgICAgICAgIGxvY2F0aW9uX3NlYXJjaFtrZXldID0gcGFyc2VJbnQobG9jYXRpb25fc2VhcmNoW2tleV0pO1xyXG4gICAgICAgICAgICAgICAgfVxyXG4gICAgICAgICAgICAgICAgaWYgKC9ecl8vLnRlc3Qoa2V5LnRvU3RyaW5nKCkpKSB7XHJcbiAgICAgICAgICAgICAgICAgICAgZmlsdGVyc19wYW5lbHNbJ3JlZCddW2tleV0gPSBsb2NhdGlvbl9zZWFyY2hba2V5XTtcclxuICAgICAgICAgICAgICAgIH1cclxuICAgICAgICAgICAgICAgIGlmICgvXmJfLy50ZXN0KGtleS50b1N0cmluZygpKSkge1xyXG4gICAgICAgICAgICAgICAgICAgIGZpbHRlcnNfcGFuZWxzWydibHVlJ11ba2V5XSA9IGxvY2F0aW9uX3NlYXJjaFtrZXldO1xyXG4gICAgICAgICAgICAgICAgfVxyXG4gICAgICAgICAgICAgICAgaWYgKC9eZ18vLnRlc3Qoa2V5LnRvU3RyaW5nKCkpKSB7XHJcbiAgICAgICAgICAgICAgICAgICAgZmlsdGVyc19wYW5lbHNbJ2dyZWVuJ11ba2V5XSA9IGxvY2F0aW9uX3NlYXJjaFtrZXldO1xyXG4gICAgICAgICAgICAgICAgfVxyXG4gICAgICAgICAgICAgICAgaWYgKC9eeV8vLnRlc3Qoa2V5LnRvU3RyaW5nKCkpKSB7XHJcbiAgICAgICAgICAgICAgICAgICAgZmlsdGVyc19wYW5lbHNbJ3llbGxvdyddW2tleV0gPSBsb2NhdGlvbl9zZWFyY2hba2V5XTtcclxuICAgICAgICAgICAgICAgIH1cclxuICAgICAgICAgICAgICAgIGlmIChfLmluY2x1ZGUoWydjJywgJ2wnLCAneiddLCBrZXkpKSB7XHJcbiAgICAgICAgICAgICAgICAgICAgdGhpcy5fZmlsdGVyc1snbWFwJ11ba2V5XSA9IGxvY2F0aW9uX3NlYXJjaFtrZXldO1xyXG4gICAgICAgICAgICAgICAgfVxyXG4gICAgICAgICAgICB9XHJcbiAgICAgICAgfVxyXG5cclxuICAgICAgICBpZiAoXy5pc1VuZGVmaW5lZChsb2NhdGlvbl9zZWFyY2hbJ3JfdF9zaWQnXSkgJiYgXy5pc1VuZGVmaW5lZChsb2NhdGlvbl9zZWFyY2hbJ2JfdF9zaWQnXSkgJiZcclxuICAgICAgICAgICAgXy5pc1VuZGVmaW5lZChsb2NhdGlvbl9zZWFyY2hbJ2dfdF9zaWQnXSkgJiYgXy5pc1VuZGVmaW5lZChsb2NhdGlvbl9zZWFyY2hbJ3lfdF9zaWQnXSkpIHtcclxuICAgICAgICAgICAgLy8gLVxyXG4gICAgICAgICAgICBmaWx0ZXJzX3BhbmVsc1sncmVkJ11bJ3JfdF9zaWQnXSA9IDA7XHJcbiAgICAgICAgICAgIHRoaXMuY3JlYXRlRmlsdGVyc0ZvclBhbmVsKFwicmVkXCIpO1xyXG4gICAgICAgIH1cclxuICAgICAgICBpZiAoIV8uaXNVbmRlZmluZWQobG9jYXRpb25fc2VhcmNoWydyX3Rfc2lkJ10pKSB7XHJcbiAgICAgICAgICAgIHRoaXMuY3JlYXRlRmlsdGVyc0ZvclBhbmVsKFwicmVkXCIpO1xyXG4gICAgICAgIH1cclxuICAgICAgICBpZiAoIV8uaXNVbmRlZmluZWQobG9jYXRpb25fc2VhcmNoWydiX3Rfc2lkJ10pKSB7XHJcbiAgICAgICAgICAgIHRoaXMuY3JlYXRlRmlsdGVyc0ZvclBhbmVsKFwiYmx1ZVwiKTtcclxuICAgICAgICB9XHJcbiAgICAgICAgaWYgKCFfLmlzVW5kZWZpbmVkKGxvY2F0aW9uX3NlYXJjaFsnZ190X3NpZCddKSkge1xyXG4gICAgICAgICAgICB0aGlzLmNyZWF0ZUZpbHRlcnNGb3JQYW5lbChcImdyZWVuXCIpO1xyXG4gICAgICAgIH1cclxuICAgICAgICBpZiAoIV8uaXNVbmRlZmluZWQobG9jYXRpb25fc2VhcmNoWyd5X3Rfc2lkJ10pKSB7XHJcbiAgICAgICAgICAgIHRoaXMuY3JlYXRlRmlsdGVyc0ZvclBhbmVsKFwieWVsbG93XCIpO1xyXG4gICAgICAgIH1cclxuXHJcbiAgICAgICAgdGhpcy4kdGltZW91dCgoKSA9PiB0aGlzLiRyb290U2NvcGUuJGJyb2FkY2FzdCgncGFnZXMubWFwLkZpbHRlcnNTZXJ2aWNlLlVwZGF0ZWRGcm9tVXJsJywgdGhpcy5fZmlsdGVycykpO1xyXG4gICAgfVxyXG5cclxuXHJcblxyXG4gICAgdXBkYXRlVXJsRnJvbUZpbHRlcnMoKSB7XHJcbiAgICAgICAgdmFyIGxvY2F0aW9uX3NlYXJjaCA9ICcnLFxyXG4gICAgICAgICAgICBtYXBfZmlsdGVycyAgICAgPSB0aGlzLl9maWx0ZXJzWydtYXAnXSxcclxuICAgICAgICAgICAgcGFuZWxzX2ZpbHRlcnMgID0gdGhpcy5fZmlsdGVyc1sncGFuZWxzJ10sXHJcbiAgICAgICAgICAgIF9mb3JtYXR0ZWRQYW5lbEZpbHRlcnMgPSB7fTtcclxuXHJcblxyXG4gICAgICAgIC8vIHJlc2V0IHRvIGVtcHR5IG9iamVjdFxyXG4gICAgICAgIHRoaXMuX2ZpbHRlcnNfZm9yX2xvYWRfbWFya2VycyA9IHtcclxuICAgICAgICAgICAgem9vbTogbnVsbCxcclxuICAgICAgICAgICAgdmlld3BvcnQ6IG51bGwsXHJcbiAgICAgICAgICAgIGZpbHRlcnM6IFtdXHJcbiAgICAgICAgfTtcclxuXHJcblxyXG4gICAgICAgIC8vIGNyZWF0ZSBsb2NhdGlvbiBzZWFyY2ggZnJvbSBtYXAgZmlsdGVyc1xyXG4gICAgICAgIGZvciAodmFyIG1hcF9maWx0ZXIgaW4gbWFwX2ZpbHRlcnMpIHtcclxuICAgICAgICAgICAgaWYgKG1hcF9maWx0ZXJzLmhhc093blByb3BlcnR5KG1hcF9maWx0ZXIpICYmICFfLmluY2x1ZGUoWyd2J10sIG1hcF9maWx0ZXIpKSB7XHJcbiAgICAgICAgICAgICAgICBpZiAoIW1hcF9maWx0ZXJzW21hcF9maWx0ZXJdKSB7XHJcbiAgICAgICAgICAgICAgICAgICAgY29udGludWU7XHJcbiAgICAgICAgICAgICAgICB9XHJcbiAgICAgICAgICAgICAgICBpZiAoIV8uaW5jbHVkZShbJycsIG51bGxdLCBtYXBfZmlsdGVyc1ttYXBfZmlsdGVyXSkpIHtcclxuICAgICAgICAgICAgICAgICAgICBsb2NhdGlvbl9zZWFyY2ggKz0gKGxvY2F0aW9uX3NlYXJjaC5sZW5ndGggIT09IDAgPyAnJicgOiAnJykgKyBtYXBfZmlsdGVyICsgJz0nICsgbWFwX2ZpbHRlcnNbbWFwX2ZpbHRlcl07XHJcbiAgICAgICAgICAgICAgICB9XHJcbiAgICAgICAgICAgIH1cclxuICAgICAgICB9XHJcblxyXG4gICAgICAgIC8vIGNyZWF0ZSBsb2NhdGlvbiBzZWFyY2ggZnJvbSBwYW5lbHMgZmlsdGVyc1xyXG4gICAgICAgIGZvciAodmFyIHBhbmVsIGluIHBhbmVsc19maWx0ZXJzKSB7XHJcbiAgICAgICAgICAgIGlmIChwYW5lbHNfZmlsdGVycy5oYXNPd25Qcm9wZXJ0eShwYW5lbCkpIHtcclxuICAgICAgICAgICAgICAgIF9mb3JtYXR0ZWRQYW5lbEZpbHRlcnMgPSB7XHJcbiAgICAgICAgICAgICAgICAgICAgcGFuZWw6IHBhbmVsXHJcbiAgICAgICAgICAgICAgICB9O1xyXG5cclxuICAgICAgICAgICAgICAgIGZvciAodmFyIHBhbmVsX2ZpbHRlciBpbiBwYW5lbHNfZmlsdGVyc1twYW5lbF0pIHtcclxuICAgICAgICAgICAgICAgICAgICBpZiAocGFuZWxzX2ZpbHRlcnNbcGFuZWxdLmhhc093blByb3BlcnR5KHBhbmVsX2ZpbHRlcikpIHtcclxuXHJcbiAgICAgICAgICAgICAgICAgICAgICAgIGlmIChwYW5lbF9maWx0ZXIuaW5kZXhPZihcInRfc2lkXCIpICE9PSAtMSAmJiBfLmlzTnVsbChwYW5lbHNfZmlsdGVyc1twYW5lbF1bcGFuZWxfZmlsdGVyXSkpIHtcclxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIF9mb3JtYXR0ZWRQYW5lbEZpbHRlcnMgPSBudWxsO1xyXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgY29udGludWU7XHJcbiAgICAgICAgICAgICAgICAgICAgICAgIH1cclxuXHJcbiAgICAgICAgICAgICAgICAgICAgICAgIGlmIChfLmluY2x1ZGUoWycnLCBudWxsXSwgcGFuZWxzX2ZpbHRlcnNbcGFuZWxdW3BhbmVsX2ZpbHRlcl0pKSB7XHJcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBjb250aW51ZTtcclxuICAgICAgICAgICAgICAgICAgICAgICAgfVxyXG5cclxuXHJcbiAgICAgICAgICAgICAgICAgICAgICAgIF9mb3JtYXR0ZWRQYW5lbEZpbHRlcnNbcGFuZWxfZmlsdGVyLnN1YnN0cigyLCBwYW5lbF9maWx0ZXIubGVuZ3RoKV0gPSBwYW5lbHNfZmlsdGVyc1twYW5lbF1bcGFuZWxfZmlsdGVyXTtcclxuXHJcblxyXG4gICAgICAgICAgICAgICAgICAgICAgICBpZiAocGFuZWxzX2ZpbHRlcnNbcGFuZWxdW3BhbmVsX2ZpbHRlcl0gPT09IHRoaXMuX2ZpbHRlcnNbJ2Jhc2UnXVtwYW5lbF9maWx0ZXIuc3Vic3RyKDIsIHBhbmVsX2ZpbHRlci5sZW5ndGgpXSkge1xyXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgY29udGludWU7XHJcbiAgICAgICAgICAgICAgICAgICAgICAgIH1cclxuXHJcblxyXG4gICAgICAgICAgICAgICAgICAgICAgICAvLyBpIGxvdmUganNcclxuICAgICAgICAgICAgICAgICAgICAgICAgLy9pZiAoXy5pbmNsdWRlKFsnMCcsICcxJywgJzInLCAnMycsICc0JywgJzUnLCAnNicsICc3JywgJzgnLCAnOSddLCBmaWx0ZXJzX3BhbmVsc1twYW5lbF1bZmlsdGVyXSkpIHtcclxuICAgICAgICAgICAgICAgICAgICAgICAgLy8gICAgZmlsdGVyc19wYW5lbHNbcGFuZWxdW2ZpbHRlcl0gPSBwYXJzZUludChmaWx0ZXJzX3BhbmVsc1twYW5lbF1bZmlsdGVyXSk7XHJcbiAgICAgICAgICAgICAgICAgICAgICAgIC8vfVxyXG5cclxuICAgICAgICAgICAgICAgICAgICAgICAgbG9jYXRpb25fc2VhcmNoICs9IChsb2NhdGlvbl9zZWFyY2gubGVuZ3RoICE9PSAwID8gJyYnIDogJycpICsgcGFuZWxfZmlsdGVyICsgJz0nICsgcGFuZWxzX2ZpbHRlcnNbcGFuZWxdW3BhbmVsX2ZpbHRlcl07XHJcbiAgICAgICAgICAgICAgICAgICAgfVxyXG4gICAgICAgICAgICAgICAgfVxyXG5cclxuICAgICAgICAgICAgICAgIGlmICghXy5pc051bGwoX2Zvcm1hdHRlZFBhbmVsRmlsdGVycykpXHJcbiAgICAgICAgICAgICAgICAgICAgdGhpcy5fZmlsdGVyc19mb3JfbG9hZF9tYXJrZXJzWydmaWx0ZXJzJ10ucHVzaChfZm9ybWF0dGVkUGFuZWxGaWx0ZXJzKTtcclxuXHJcblxyXG4gICAgICAgICAgICB9XHJcbiAgICAgICAgfVxyXG5cclxuICAgICAgICBjb25zb2xlLmluZm8oJ3VwZGF0ZVVybEZyb21QYW5lbHNGaWx0ZXJzIG1ldGhvZDogcGFuZWxzIGZpbHRlcnMgdXBkYXRlZCcpO1xyXG5cclxuICAgICAgICB0aGlzLiRsb2NhdGlvbi5zZWFyY2gobG9jYXRpb25fc2VhcmNoKTtcclxuXHJcbiAgICAgICAgaWYgKCF0aGlzLiRyb290U2NvcGUuJCRwaGFzZSlcclxuICAgICAgICAgICAgdGhpcy4kcm9vdFNjb3BlLiRhcHBseSgpO1xyXG4gICAgfVxyXG5cclxuXHJcblxyXG4gICAgY3JlYXRlRm9ybWF0dGVkT2JqZWN0Rm9yTG9hZE1hcmtlcnMoKSB7XHJcbiAgICAgICAgdGhpcy5fZmlsdGVyc19mb3JfbG9hZF9tYXJrZXJzLnpvb20gPSB0aGlzLl9maWx0ZXJzLm1hcC56O1xyXG4gICAgICAgIHRoaXMuY3JlYXRlRm9ybWF0dGVkVmlld3BvcnRGb3JMb2FkTWFya2VycygpO1xyXG5cclxuICAgICAgICB0aGlzLiR0aW1lb3V0KCgpID0+IHRoaXMuJHJvb3RTY29wZS4kYnJvYWRjYXN0KCdwYWdlcy5tYXAuRmlsdGVyc1NlcnZpY2UuQ3JlYXRlZEZvcm1hdHRlZEZpbHRlcnMnLCB0aGlzLl9maWx0ZXJzX2Zvcl9sb2FkX21hcmtlcnMpKTtcclxuICAgIH1cclxuXHJcblxyXG5cclxuICAgIGNyZWF0ZUZvcm1hdHRlZFZpZXdwb3J0Rm9yTG9hZE1hcmtlcnMoKSB7XHJcbiAgICAgICAgdmFyIGZpbHRlcnNfbWFwID0gdGhpcy5fZmlsdGVycy5tYXA7XHJcblxyXG4gICAgICAgIHZhciBzbmVMYXQgPSBmaWx0ZXJzX21hcC52LmdldE5vcnRoRWFzdCgpLmxhdCgpLnRvU3RyaW5nKCksXHJcbiAgICAgICAgICAgIHNuZUxuZyA9IGZpbHRlcnNfbWFwLnYuZ2V0Tm9ydGhFYXN0KCkubG5nKCkudG9TdHJpbmcoKSxcclxuICAgICAgICAgICAgc3N3TGF0ID0gZmlsdGVyc19tYXAudi5nZXRTb3V0aFdlc3QoKS5sYXQoKS50b1N0cmluZygpLFxyXG4gICAgICAgICAgICBzc3dMbmcgPSBmaWx0ZXJzX21hcC52LmdldFNvdXRoV2VzdCgpLmxuZygpLnRvU3RyaW5nKCk7XHJcblxyXG4gICAgICAgIHZhciBuZUxhdCA9IHNuZUxhdC5yZXBsYWNlKHNuZUxhdC5zdWJzdHJpbmcoc25lTGF0LmluZGV4T2YoXCIuXCIpICsgMywgc25lTGF0Lmxlbmd0aCksIFwiXCIpLFxyXG4gICAgICAgICAgICBuZUxuZyA9IHNuZUxuZy5yZXBsYWNlKHNuZUxuZy5zdWJzdHJpbmcoc25lTG5nLmluZGV4T2YoXCIuXCIpICsgMywgc25lTG5nLmxlbmd0aCksIFwiXCIpLFxyXG4gICAgICAgICAgICBzd0xhdCA9IHNzd0xhdC5yZXBsYWNlKHNzd0xhdC5zdWJzdHJpbmcoc3N3TGF0LmluZGV4T2YoXCIuXCIpICsgMywgc3N3TGF0Lmxlbmd0aCksIFwiXCIpLFxyXG4gICAgICAgICAgICBzd0xuZyA9IHNzd0xuZy5yZXBsYWNlKHNzd0xuZy5zdWJzdHJpbmcoc3N3TG5nLmluZGV4T2YoXCIuXCIpICsgMywgc3N3TG5nLmxlbmd0aCksIFwiXCIpO1xyXG5cclxuICAgICAgICB0aGlzLl9maWx0ZXJzX2Zvcl9sb2FkX21hcmtlcnMudmlld3BvcnQgPSB7XHJcbiAgICAgICAgICAgICduZV9sYXQnOiBuZUxhdCxcclxuICAgICAgICAgICAgJ25lX2xuZyc6IG5lTG5nLFxyXG4gICAgICAgICAgICAnc3dfbGF0Jzogc3dMYXQsXHJcbiAgICAgICAgICAgICdzd19sbmcnOiBzd0xuZ1xyXG4gICAgICAgIH07XHJcblxyXG4gICAgICAgIGNvbnNvbGUubG9nKHRoaXMuX2ZpbHRlcnNfZm9yX2xvYWRfbWFya2Vycyk7XHJcbiAgICB9XHJcbn1cclxuXHJcbkZpbHRlcnNTZXJ2aWNlLiRpbmplY3QgPSBbJyRyb290U2NvcGUnLCAnJHRpbWVvdXQnLCAnJGxvY2F0aW9uJywgJ1JlYWx0eVR5cGVzU2VydmljZSddOyIsImV4cG9ydCBjbGFzcyBNYXJrZXJzU2VydmljZSB7XHJcblxyXG4gICAgY29uc3RydWN0b3IoJHJvb3RTY29wZSwgJGh0dHAsICR0aW1lb3V0KSB7XHJcbiAgICAgICAgdmFyIHNlbGYgPSB0aGlzO1xyXG5cclxuICAgICAgICB0aGlzLiRyb290U2NvcGUgPSAkcm9vdFNjb3BlO1xyXG4gICAgICAgIHRoaXMuJGh0dHAgPSAkaHR0cDtcclxuICAgICAgICB0aGlzLiR0aW1lb3V0ID0gJHRpbWVvdXQ7XHJcblxyXG5cclxuICAgICAgICB0aGlzLl9maWx0ZXJzX2Zvcl9sb2FkX21hcmtlcnMgPSBudWxsO1xyXG4gICAgICAgIHRoaXMuX3Jlc3BvbnNlX21hcmtlcnMgPSB7XHJcbiAgICAgICAgICAgIHJlZDogICAge30sXHJcbiAgICAgICAgICAgIGJsdWU6ICAge30sXHJcbiAgICAgICAgICAgIGdyZWVuOiAge31cclxuICAgICAgICB9O1xyXG4gICAgICAgIHRoaXMuIF9tYXJrZXJzID0ge1xyXG4gICAgICAgICAgICByZWQ6ICAgIHt9LFxyXG4gICAgICAgICAgICBibHVlOiAgIHt9LFxyXG4gICAgICAgICAgICBncmVlbjogIHt9XHJcbiAgICAgICAgfTtcclxuXHJcbiAgICAgICAgJHJvb3RTY29wZS4kb24oJ3BhZ2VzLm1hcC5GaWx0ZXJzU2VydmljZS5DcmVhdGVkRm9ybWF0dGVkRmlsdGVycycsIGZ1bmN0aW9uKGV2ZW50LCBmb3JtYXR0ZWRfZmlsdGVycykge1xyXG4gICAgICAgICAgICBzZWxmLl9maWx0ZXJzX2Zvcl9sb2FkX21hcmtlcnMgPSBmb3JtYXR0ZWRfZmlsdGVycztcclxuXHJcbiAgICAgICAgICAgIHNlbGYubG9hZCgpO1xyXG4gICAgICAgIH0pO1xyXG4gICAgfVxyXG5cclxuXHJcblxyXG4gICAgbG9hZCgpIHtcclxuICAgICAgICB2YXIgc2VsZiA9IHRoaXM7XHJcblxyXG4gICAgICAgIHRoaXMuJGh0dHAuZ2V0KCcvYWpheC9hcGkvbWFya2Vycy8/cD0nICsgSlNPTi5zdHJpbmdpZnkodGhpcy5fZmlsdGVyc19mb3JfbG9hZF9tYXJrZXJzKSkuc3VjY2VzcyhmdW5jdGlvbihyZXNwb25zZSkge1xyXG4gICAgICAgICAgICBzZWxmLmNsZWFyUmVzcG9uc2VNYXJrZXJzT2JqZWN0KCk7XHJcblxyXG4gICAgICAgICAgICBzZWxmLl9yZXNwb25zZV9tYXJrZXJzID0gcmVzcG9uc2U7XHJcbiAgICAgICAgICAgIHNlbGYuJHRpbWVvdXQoKCkgPT4gc2VsZi4kcm9vdFNjb3BlLiRicm9hZGNhc3QoJ3BhZ2VzLm1hcC5NYXJrZXJzU2VydmljZS5NYXJrZXJzSXNMb2FkZWQnKSk7XHJcbiAgICAgICAgfSk7XHJcbiAgICB9XHJcblxyXG5cclxuXHJcbiAgICBwbGFjZShtYXApIHtcclxuICAgICAgICAvLyDQstC40LTQsNC70Y/RlNC80L4g0LzQsNGA0LrQtdGA0Lgg0Lcg0LrQsNGA0YLQuCDRj9C60LjRhSDQvdC10LzQsCDQsiDQstGW0LTQv9C+0LLRltC00ZYg0Lcg0YHQtdGA0LLQtdGA0LBcclxuICAgICAgICBmb3IgKHZhciBwYW5lbCBpbiB0aGlzLl9tYXJrZXJzKSB7XHJcbiAgICAgICAgICAgIGlmICh0aGlzLl9tYXJrZXJzLmhhc093blByb3BlcnR5KHBhbmVsKSkge1xyXG4gICAgICAgICAgICAgICAgZm9yICh2YXIgbWFya2VyIGluIHRoaXMuX21hcmtlcnNbcGFuZWxdKSB7XHJcbiAgICAgICAgICAgICAgICAgICAgaWYgKHRoaXMuX21hcmtlcnNbcGFuZWxdLmhhc093blByb3BlcnR5KG1hcmtlcikpIHtcclxuICAgICAgICAgICAgICAgICAgICAgICAgaWYgKCF0aGlzLl9yZXNwb25zZV9tYXJrZXJzW3BhbmVsXVttYXJrZXJdKSB7XHJcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aGlzLl9tYXJrZXJzW3BhbmVsXVttYXJrZXJdLnNldE1hcChudWxsKTtcclxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGNvbnNvbGUubG9nKCdkZWxldGVkOiAnICsgdGhpcy5fbWFya2Vyc1twYW5lbF1bbWFya2VyXSk7XHJcblxyXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgZGVsZXRlIHRoaXMuX21hcmtlcnNbcGFuZWxdW21hcmtlcl07XHJcbiAgICAgICAgICAgICAgICAgICAgICAgIH1cclxuICAgICAgICAgICAgICAgICAgICAgICAgY29uc29sZS5sb2codGhpcy5fbWFya2VycylcclxuICAgICAgICAgICAgICAgICAgICB9XHJcbiAgICAgICAgICAgICAgICB9XHJcbiAgICAgICAgICAgIH1cclxuICAgICAgICB9XHJcblxyXG5cclxuICAgICAgICAvLyDQtNC+0LTQsNGU0LzQviDQvdC+0LLQstGWINC80LDRgNC60LXRgNC4INC90LAg0LrQsNGA0YLRg1xyXG4gICAgICAgIGZvciAodmFyIHBhbmVsIGluIHRoaXMuX3Jlc3BvbnNlX21hcmtlcnMpIHtcclxuICAgICAgICAgICAgaWYgKHRoaXMuX3Jlc3BvbnNlX21hcmtlcnMuaGFzT3duUHJvcGVydHkocGFuZWwpKSB7XHJcbiAgICAgICAgICAgICAgICBmb3IgKHZhciBtYXJrZXIgaW4gdGhpcy5fcmVzcG9uc2VfbWFya2Vyc1twYW5lbF0pIHtcclxuICAgICAgICAgICAgICAgICAgICBpZiAodGhpcy5fcmVzcG9uc2VfbWFya2Vyc1twYW5lbF0uaGFzT3duUHJvcGVydHkobWFya2VyKSkge1xyXG5cclxuICAgICAgICAgICAgICAgICAgICAgICAgaWYgKCF0aGlzLl9tYXJrZXJzW3BhbmVsXVttYXJrZXJdKSB7XHJcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aGlzLl9tYXJrZXJzW3BhbmVsXVttYXJrZXJdID0gbmV3IGdvb2dsZS5tYXBzLk1hcmtlcih7XHJcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgcG9zaXRpb246IG5ldyBnb29nbGUubWFwcy5MYXRMbmcobWFya2VyLnNwbGl0KCc6JylbMF0sIG1hcmtlci5zcGxpdCgnOicpWzFdKSxcclxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBtYXA6IG1hcCxcclxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aXRsZTogJ0hlbGxvIFdvcmxkISdcclxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIH0pO1xyXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5fbWFya2Vyc1twYW5lbF1bbWFya2VyXS5zZXRNYXAobWFwKTtcclxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGNvbnNvbGUubG9nKCdhZGRlZDogJyArIHRoaXMuX21hcmtlcnNbcGFuZWxdW21hcmtlcl0pXHJcbiAgICAgICAgICAgICAgICAgICAgICAgIH1cclxuXHJcbiAgICAgICAgICAgICAgICAgICAgICAgIGNvbnNvbGUubG9nKHRoaXMuX21hcmtlcnMpXHJcbiAgICAgICAgICAgICAgICAgICAgfVxyXG4gICAgICAgICAgICAgICAgfVxyXG4gICAgICAgICAgICB9XHJcbiAgICAgICAgfVxyXG5cclxuICAgICAgICB0aGlzLiR0aW1lb3V0KCgpID0+IHRoaXMuJHJvb3RTY29wZS4kYnJvYWRjYXN0KCdwYWdlcy5tYXAuTWFya2Vyc1NlcnZpY2UuTWFya2Vyc1BsYWNlZCcpKTtcclxuICAgIH1cclxuXHJcblxyXG5cclxuICAgIGNsZWFyUmVzcG9uc2VNYXJrZXJzT2JqZWN0KCkge1xyXG4gICAgICAgIHRoaXMuX3Jlc3BvbnNlX21hcmtlcnMgPSB7XHJcbiAgICAgICAgICAgIHJlZDogICAge30sXHJcbiAgICAgICAgICAgIGJsdWU6ICAge30sXHJcbiAgICAgICAgICAgIGdyZWVuOiAge31cclxuICAgICAgICB9O1xyXG4gICAgfVxyXG59XHJcblxyXG5NYXJrZXJzU2VydmljZS4kaW5qZWN0ID0gW1xyXG4gICAgJyRyb290U2NvcGUnLFxyXG4gICAgJyRodHRwJyxcclxuICAgICckdGltZW91dCdcclxuXTsiXX0=
