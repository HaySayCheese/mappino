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
/// <reference path='RealtyTypesService.ts' /> 
/// <reference path='../_references.ts' />
var pages;
(function (pages) {
    var cabinet;
    (function (cabinet) {
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
        cabinet.ProvidersConfigs = ProvidersConfigs;
    })(cabinet = pages.cabinet || (pages.cabinet = {}));
})(pages || (pages = {}));
/// <reference path='../_references.ts' />
var pages;
(function (pages) {
    var cabinet;
    (function (cabinet) {
        'use strict';
        var RoutersConfigs = (function () {
            function RoutersConfigs(app) {
                this.app = app;
                app.config(['$stateProvider', '$urlRouterProvider', '$locationProvider', function ($stateProvider, $urlRouterProvider, $locationProvider) {
                        $urlRouterProvider.otherwise("/publications/");
                        $stateProvider
                            .state('publications', {
                            url: "/publications/",
                            templateUrl: '/ajax/template/cabinet/publications/briefs/'
                        })
                            .state('publication_view', {
                            url: "/publication/:id/view/",
                            templateUrl: '/ajax/template/cabinet/publications/publication/'
                        })
                            .state('publication_edit', {
                            url: "/publication/:id/edit/",
                            templateUrl: '/ajax/template/cabinet/publications/publication/'
                        })
                            .state('support', {
                            url: "/support/",
                            templateUrl: '/ajax/template/cabinet/support/'
                        })
                            .state('settings', {
                            url: "/settings/",
                            templateUrl: '/ajax/template/cabinet/settings/'
                        });
                        $locationProvider.hashPrefix('!');
                    }]);
            }
            return RoutersConfigs;
        })();
        cabinet.RoutersConfigs = RoutersConfigs;
    })(cabinet = pages.cabinet || (pages.cabinet = {}));
})(pages || (pages = {}));
/// <reference path='../_references.ts' />
var pages;
(function (pages) {
    var cabinet;
    (function (cabinet) {
        'use strict';
        var ApplicationConfigs = (function () {
            function ApplicationConfigs(app) {
                this.app = app;
            }
            return ApplicationConfigs;
        })();
        cabinet.ApplicationConfigs = ApplicationConfigs;
    })(cabinet = pages.cabinet || (pages.cabinet = {}));
})(pages || (pages = {}));
/// <reference path='../_references.ts' />
var pages;
(function (pages) {
    var cabinet;
    (function (cabinet) {
        var AdminAuthService = (function () {
            function AdminAuthService($http) {
                this.$http = $http;
                // -
            }
            AdminAuthService.prototype.login = function (admin, callback) {
                this.$http.post('/api/admin/login/', admin)
                    .then(function (response) {
                    callback(response);
                });
            };
            AdminAuthService.$inject = [
                '$http'
            ];
            return AdminAuthService;
        })();
        cabinet.AdminAuthService = AdminAuthService;
    })(cabinet = pages.cabinet || (pages.cabinet = {}));
})(pages || (pages = {}));
/// <reference path='../_references.ts' />
var pages;
(function (pages) {
    var cabinet;
    (function (cabinet) {
        var LoginController = (function () {
            function LoginController($scope, adminAuthService) {
                this.$scope = $scope;
                this.adminAuthService = adminAuthService;
                this.admin = {
                    username: '',
                    password: ''
                };
                // -
            }
            LoginController.prototype.login = function () {
                this.adminAuthService.login(this.admin, function (response) {
                    if (response.code !== 0) {
                        console.log('!ok');
                    }
                    else {
                        console.log('ok');
                    }
                });
            };
            LoginController.$inject = [
                '$scope',
                'AdminAuthService'
            ];
            return LoginController;
        })();
        cabinet.LoginController = LoginController;
    })(cabinet = pages.cabinet || (pages.cabinet = {}));
})(pages || (pages = {}));
/// <reference path='../_references.ts' />
var pages;
(function (pages) {
    var cabinet;
    (function (cabinet) {
        var CabinetController = (function () {
            function CabinetController($timeout) {
                this.$timeout = $timeout;
                this.$inject = [
                    '$timeout'
                ];
                $(".button-collapse").sideNav();
            }
            return CabinetController;
        })();
        cabinet.CabinetController = CabinetController;
    })(cabinet = pages.cabinet || (pages.cabinet = {}));
})(pages || (pages = {}));
/// <reference path='../_references.ts' />
var pages;
(function (pages) {
    var cabinet;
    (function (cabinet) {
        var BriefsController = (function () {
            function BriefsController($scope, $timeout, realtyTypesService) {
                this.$scope = $scope;
                this.$timeout = $timeout;
                this.realtyTypesService = realtyTypesService;
                // -
                $scope.realtyTypes = realtyTypesService.realty_types;
                $timeout(function () { return $('select').material_select(); });
            }
            BriefsController.$inject = [
                '$scope',
                '$timeout',
                'RealtyTypesService'
            ];
            return BriefsController;
        })();
        cabinet.BriefsController = BriefsController;
    })(cabinet = pages.cabinet || (pages.cabinet = {}));
})(pages || (pages = {}));
/// <reference path='_references.ts' />
var pages;
(function (pages) {
    var cabinet;
    (function (cabinet) {
        'use strict';
        var app = angular.module('mappino.pages.cabinet', [
            'ngCookies',
            'ui.router'
        ]);
        /** Providers configuration create */
        new cabinet.ProvidersConfigs(app);
        /** Routers configuration create */
        new cabinet.RoutersConfigs(app);
        /** Application configuration create */
        new cabinet.ApplicationConfigs(app);
        /** Module services */
        app.service('RealtyTypesService', bModules.Types.RealtyTypesService);
        app.service('AdminAuthService', cabinet.AdminAuthService);
        /** Module controllers */
        app.controller('LoginController', cabinet.LoginController);
        app.controller('CabinetController', cabinet.CabinetController);
        app.controller('BriefsController', cabinet.BriefsController);
    })(cabinet = pages.cabinet || (pages.cabinet = {}));
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
/// <reference path='configs/RoutersConfigs.ts' />
/// <reference path='configs/ApplicationConfigs.ts' />
// ####################
// Services import
// ####################
/// <reference path='services/AdminAuthService.ts' />
// ####################
// Controllers import
// ####################
/// <reference path='controllers/LoginController.ts' />
/// <reference path='controllers/CabinetController.ts' />
/// <reference path='controllers/BriefsController.ts' />
// ####################
// App init
// ####################
/// <reference path='App.ts' />
//# sourceMappingURL=cabinet.js.map