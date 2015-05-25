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
    var admin;
    (function (admin) {
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
        admin.ProvidersConfigs = ProvidersConfigs;
    })(admin = pages.admin || (pages.admin = {}));
})(pages || (pages = {}));
/// <reference path='../_references.ts' />
var pages;
(function (pages) {
    var admin;
    (function (admin) {
        'use strict';
        var ApplicationConfigs = (function () {
            function ApplicationConfigs(app) {
                this.app = app;
            }
            return ApplicationConfigs;
        })();
        admin.ApplicationConfigs = ApplicationConfigs;
    })(admin = pages.admin || (pages.admin = {}));
})(pages || (pages = {}));
/// <reference path='../_references.ts' />
var pages;
(function (pages) {
    var admin;
    (function (admin_1) {
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
        admin_1.AdminAuthService = AdminAuthService;
    })(admin = pages.admin || (pages.admin = {}));
})(pages || (pages = {}));
/// <reference path='../_references.ts' />
var pages;
(function (pages) {
    var admin;
    (function (admin) {
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
        admin.LoginController = LoginController;
    })(admin = pages.admin || (pages.admin = {}));
})(pages || (pages = {}));
/// <reference path='../_references.ts' />
var pages;
(function (pages) {
    var admin;
    (function (admin) {
        var AdminController = (function () {
            function AdminController() {
            }
            return AdminController;
        })();
        admin.AdminController = AdminController;
    })(admin = pages.admin || (pages.admin = {}));
})(pages || (pages = {}));
/// <reference path='_references.ts' />
var pages;
(function (pages) {
    var admin;
    (function (admin) {
        'use strict';
        var app = angular.module('mappino.pages.home', [
            'ngCookies'
        ]);
        /** Providers configuration create */
        new admin.ProvidersConfigs(app);
        /** Application configuration create */
        new admin.ApplicationConfigs(app);
        /** Module services */
        app.service('AdminAuthService', admin.AdminAuthService);
        /** Module controllers */
        app.controller('LoginController', admin.LoginController);
        app.controller('AdminController', admin.AdminController);
    })(admin = pages.admin || (pages.admin = {}));
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
/// <reference path='services/AdminAuthService.ts' />
// ####################
// Controllers import
// ####################
/// <reference path='controllers/LoginController.ts' />
/// <reference path='controllers/AdminController.ts' />
// ####################
// App init
// ####################
/// <reference path='App.ts' />
