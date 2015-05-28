/// <reference path='angular.d.ts' />
/// <reference path='angular-cookies.d.ts' />
/// <reference path='angular-ui-router.d.ts' />
/// <reference path='custom.d.ts' />
/// <reference path='google.maps.d.ts' />
/// <reference path='jquery.d.ts' />
/// <reference path='underscore.d.ts' />
/// <reference path='../_references.ts' />
var bModules;
(function (bModules) {
    var Types;
    (function (Types) {
        var RealtyTypesService = (function () {
            function RealtyTypesService() {
                this._realty_types = [
                    {
                        id: 0,
                        name: "flat",
                        title: "Квартиры",
                        filters: [
                            "op_sid", "pr_sid", "p_min", "p_max", "cu_sid", "p_c_min", "p_c_max", "n_b",
                            "s_m", "fml", "frg", "r_c_min", "r_c_max", "t_a_min", "t_a_max", "f_min", "f_max",
                            "msd", "grd", "pl_sid", "lft", "elt", "h_w", "c_w", "gas", "h_t_sid"
                        ]
                    }, {
                        id: 1,
                        name: "house",
                        title: "Дома",
                        filters: [
                            "op_sid", "pr_sid", "p_min", "p_max", "cu_sid", "p_c_min", "p_c_max", "n_b",
                            "s_m", "fml", "frg", "r_c_min", "r_c_max", "f_c_min", "f_c_max", "elt", "h_w",
                            "gas", "c_w", "swg", "h_t_sid"
                        ]
                    }, {
                        id: 2,
                        name: "room",
                        title: "Комнаты",
                        filters: [
                            "op_sid", "pr_sid", "p_min", "p_max", "cu_sid", "p_c_min", "p_c_max", "n_b",
                            "s_m", "fml", "frg", "r_c_min", "r_c_max", "t_a_min", "t_a_max", "f_min", "f_max",
                            "msd", "grd", "lft", "elt", "h_w", "c_w", "gas", "h_t_sid"
                        ]
                    }, {
                        id: 3,
                        name: "land",
                        title: "Земельные участки",
                        filters: [
                            "op_sid", "p_min", "p_max", "cu_sid", "a_min", "a_max", "gas", "elt", "wtr", "swg"
                        ]
                    }, {
                        id: 4,
                        name: "garage",
                        title: "Гаражи",
                        filters: [
                            "op_sid", "p_min", "p_max", "cu_sid", "t_a_min", "t_a_max"
                        ]
                    }, {
                        id: 5,
                        name: "office",
                        title: "Офисы",
                        filters: [
                            "op_sid", "p_min", "p_max", "cu_sid", "n_b", "s_m", "t_a_min", "t_a_max",
                            "c_c_min", "c_c_max", "sct", "ktn", "h_w", "c_w"
                        ]
                    }, {
                        id: 6,
                        name: "trade",
                        title: "Торговые помещения",
                        filters: [
                            "op_sid", "p_min", "p_max", "cu_sid", "n_b", "s_m", "h_a_min", "h_a_max",
                            "t_a_min", "t_a_max", "b_t_sid", "gas", "elt", "h_w", "c_w", "swg"
                        ]
                    }, {
                        id: 7,
                        name: "warehouse",
                        title: "Склады",
                        filters: [
                            "op_sid", "p_min", "p_max", "cu_sid", "n_b", "s_m", "h_a_min", "h_a_max",
                            "gas", "elt", "h_w", "c_w", "s_a", "f_a"
                        ]
                    }, {
                        id: 8,
                        name: "business",
                        title: "Готовый бизнес",
                        filters: [
                            "op_sid", "p_min", "p_max", "cu_sid"
                        ]
                    }];
            }
            Object.defineProperty(RealtyTypesService.prototype, "realty_types", {
                get: function () {
                    return this._realty_types;
                },
                enumerable: true,
                configurable: true
            });
            return RealtyTypesService;
        })();
        Types.RealtyTypesService = RealtyTypesService;
    })(Types = bModules.Types || (bModules.Types = {}));
})(bModules || (bModules = {}));
/// <reference path='_references.ts' />
var bModules;
(function (bModules) {
    var Types;
    (function (Types) {
        'use strict';
        var bTypes = angular.module('bModules.Types', []);
        bTypes.service('RealtyTypesService', Types.RealtyTypesService);
    })(Types = bModules.Types || (bModules.Types = {}));
})(bModules || (bModules = {}));
/// <reference path='../../definitions/_references.ts' />
/// <reference path='services/RealtyTypesService.ts' />
/// <reference path='Types.ts' /> 
/// <reference path='../_references.ts' />
var pages;
(function (pages) {
    var home;
    (function (home) {
        'use strict';
        var ProvidersConfigs = (function () {
            function ProvidersConfigs(app) {
                this.app = app;
                app.config(['$interpolateProvider', '$locationProvider',
                    function ($interpolateProvider, $locationProvider) {
                        $interpolateProvider.startSymbol('[[');
                        $interpolateProvider.endSymbol(']]');
                    }
                ]);
            }
            return ProvidersConfigs;
        })();
        home.ProvidersConfigs = ProvidersConfigs;
    })(home = pages.home || (pages.home = {}));
})(pages || (pages = {}));
/// <reference path='../_references.ts' />
var pages;
(function (pages) {
    var home;
    (function (home) {
        'use strict';
        var ApplicationConfigs = (function () {
            function ApplicationConfigs(app) {
                this.app = app;
            }
            return ApplicationConfigs;
        })();
        home.ApplicationConfigs = ApplicationConfigs;
    })(home = pages.home || (pages.home = {}));
})(pages || (pages = {}));
/// <reference path='../_references.ts' />
var pages;
(function (pages) {
    var home;
    (function (home) {
        var HomeController = (function () {
            function HomeController($scope, $timeout) {
                this.$scope = $scope;
                this.$timeout = $timeout;
                // -
                $timeout(function () { return $('.parallax').parallax(); });
                this.setParalaxHeight();
            }
            HomeController.prototype.setParalaxHeight = function () {
                $(window).on('resize', function () {
                    if ($(window).height() > 300) {
                        $('.parallax-container:first-child').css('height', $(window).height() + 'px');
                    }
                }).resize();
            };
            HomeController.scrollTo = function (to) {
                $("html, body").animate({
                    scrollTop: to === 'top' ? 0 : $(window).height()
                }, '500');
                event.preventDefault();
            };
            HomeController.$inject = [
                '$scope',
                '$timeout'
            ];
            return HomeController;
        })();
        home.HomeController = HomeController;
    })(home = pages.home || (pages.home = {}));
})(pages || (pages = {}));
/// <reference path='_references.ts' />
var pages;
(function (pages) {
    var home;
    (function (home) {
        'use strict';
        var app = angular.module('mappino.pages.home', [
            'ngCookies'
        ]);
        /** Providers configuration create */
        new home.ProvidersConfigs(app);
        /** Application configuration create */
        new home.ApplicationConfigs(app);
        /** Module services */
        app.service('RealtyTypesService', bModules.Types.RealtyTypesService);
        /** Module controllers */
        app.controller('HomeController', home.HomeController);
    })(home = pages.home || (pages.home = {}));
})(pages || (pages = {}));
// ####################
// Declarations import
// ####################
/// <reference path='../_common/definitions/underscore.d.ts' />
/// <reference path='../_common/definitions/google.maps.d.ts' />
/// <reference path='../_common/definitions/jquery.d.ts' />
/// <reference path='../_common/definitions/angular.d.ts' />
/// <reference path='../_common/definitions/angular-cookies.d.ts' />
/// <reference path='../_common/definitions/angular-ui-router.d.ts' />
/// <reference path='../_common/definitions/custom.d.ts' />
// ####################
// Interfaces import
// ####################
// ####################
// _modules import
// ####################
/// <reference path='../_common/bModules/Types/_references.ts' />
// ####################
// Configs import
// ####################
/// <reference path='configs/ProvidersConfigs.ts' />
/// <reference path='configs/ApplicationConfigs.ts' />
// ####################
// Services import
// ####################
// ####################
// Controllers import
// ####################
/// <reference path='controllers/HomeController.ts' />
// ####################
// App init
// ####################
/// <reference path='App.ts' />
//# sourceMappingURL=landing.js.map