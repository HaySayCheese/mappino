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
var bModules;
(function (bModules) {
    var Auth;
    (function (Auth) {
        var AuthService = (function () {
            function AuthService($http, $cookies) {
                this.$http = $http;
                this.$cookies = $cookies;
                // -
                this.getUserByCookie();
            }
            AuthService.prototype.login = function (user, callback) {
                var self = this;
                this.$http.post('/ajax/api/accounts/login/', user)
                    .then(function (response) {
                    if (response.data['code'] === 0) {
                        self.updateUserData(response.data['user']);
                        callback(response);
                    }
                    else {
                        self.removeFromStorages();
                        callback(response);
                    }
                }, function () {
                    // - error
                });
            };
            AuthService.prototype.getUserByCookie = function () {
                var self = this;
                this.$http.get('/ajax/api/accounts/on-login-info/')
                    .then(function (response) {
                    if (response.data['code'] === 0) {
                        self.updateUserData(response.data['user']);
                    }
                    else {
                        self.removeFromStorages();
                    }
                }, function () {
                    // - error
                });
            };
            AuthService.prototype.updateUserData = function (user) {
                this._user = user;
                this._user['full_name'] = user['name'] + ' ' + user['surname'];
                this.saveToStorages(user);
            };
            AuthService.prototype.saveToStorages = function (user) {
                console.log(user);
                if (localStorage) {
                    localStorage['user'] = JSON.stringify(user);
                }
            };
            AuthService.prototype.removeFromStorages = function () {
                if (localStorage && localStorage['user']) {
                    delete localStorage['user'];
                }
            };
            Object.defineProperty(AuthService.prototype, "user", {
                //private getFromStorages() {
                //    if (localStorage && localStorage['user']) {
                //        this._user = JSON.parse(localStorage['user']);
                //    }
                //}
                get: function () {
                    return this._user;
                },
                set: function (user) {
                    for (var key in user) {
                        this._user[key] = user[key];
                    }
                },
                enumerable: true,
                configurable: true
            });
            // $inject annotation.
            AuthService.$inject = [
                '$http',
                '$cookieStore'
            ];
            return AuthService;
        })();
        Auth.AuthService = AuthService;
    })(Auth = bModules.Auth || (bModules.Auth = {}));
})(bModules || (bModules = {}));
/// <reference path='_references.ts' />
var bModules;
(function (bModules) {
    var Auth;
    (function (Auth) {
        'use strict';
        var bAuth = angular.module('bModules.Auth', ['ngCookies']);
        bAuth.service('AuthService', Auth.AuthService);
    })(Auth = bModules.Auth || (bModules.Auth = {}));
})(bModules || (bModules = {}));
/// <reference path='../../definitions/jquery.d.ts' />
/// <reference path='../../definitions/angular.d.ts' />
/// <reference path='../../definitions/angular-cookies.d.ts' />
/// <reference path='services/AuthService.ts' />
/// <reference path='Auth.ts' />
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
        var PublicationsService = (function () {
            function PublicationsService($http, $state) {
                this.$http = $http;
                this.$state = $state;
                // -
            }
            PublicationsService.prototype.create = function (publication, callback) {
                var self = this;
                this.$http.post('/ajax/api/cabinet/publications/', publication)
                    .then(function (response) {
                    self.$state.go('publication_edit', { id: publication['tid'] + ":" + response.data['data']['id'] });
                    callback(response);
                }, function () {
                    // error
                });
            };
            PublicationsService.prototype.loadPublicationData = function (publication, callback) {
                var self = this;
                this.$http.get('/ajax/api/cabinet/publications/' + publication['tid'] + ':' + publication['hid'] + '/')
                    .then(function (response) {
                    console.log(response);
                    callback(response);
                }, function () {
                    // -
                });
            };
            PublicationsService.$inject = [
                '$http',
                '$state'
            ];
            return PublicationsService;
        })();
        cabinet.PublicationsService = PublicationsService;
    })(cabinet = pages.cabinet || (pages.cabinet = {}));
})(pages || (pages = {}));
/// <reference path='../_references.ts' />
var pages;
(function (pages) {
    var cabinet;
    (function (cabinet) {
        var LoginController = (function () {
            function LoginController($scope, authService) {
                this.$scope = $scope;
                this.authService = authService;
                // -
                $scope.user = {
                    username: '',
                    password: '',
                    invalid: false
                };
            }
            LoginController.prototype.login = function () {
                var self = this;
                if (!this.$scope.user.username || !this.$scope.user.password) {
                    return;
                }
                this.authService.login(this.$scope.user, function (response) {
                    if (response.data.code !== 0) {
                        self.$scope.user.invalid = true;
                    }
                    else {
                        window.location.pathname = '/cabinet/';
                    }
                });
            };
            LoginController.$inject = [
                '$scope',
                'AuthService'
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
            function CabinetController($timeout, authService) {
                this.$timeout = $timeout;
                this.authService = authService;
                // -
                var self = this;
                //$timeout(() => {
                //    self.authService.user = { full_name: 'fsafaf' };
                //    console.log(self.authService.user)
                //}, 4000);
                $(".button-collapse").sideNav();
            }
            CabinetController.$inject = [
                '$timeout',
                'AuthService'
            ];
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
            function BriefsController($scope, $timeout, realtyTypesService, publicationsService) {
                this.$scope = $scope;
                this.$timeout = $timeout;
                this.realtyTypesService = realtyTypesService;
                this.publicationsService = publicationsService;
                // -
                $scope.new_publication = {
                    tid: 0,
                    for_sale: true,
                    for_rent: false
                };
                $scope.realtyTypes = realtyTypesService.realty_types;
                $timeout(function () { return $('select').material_select(); });
            }
            BriefsController.prototype.createPublication = function () {
                this.publicationsService.create(this.$scope.new_publication, function () {
                    // - create callback
                });
            };
            BriefsController.$inject = [
                '$scope',
                '$timeout',
                'RealtyTypesService',
                'PublicationsService'
            ];
            return BriefsController;
        })();
        cabinet.BriefsController = BriefsController;
    })(cabinet = pages.cabinet || (pages.cabinet = {}));
})(pages || (pages = {}));
/// <reference path='../_references.ts' />
var pages;
(function (pages) {
    var cabinet;
    (function (cabinet) {
        var PublicationController = (function () {
            function PublicationController($scope, $timeout, $state, publicationsService) {
                // -
                this.$scope = $scope;
                this.$timeout = $timeout;
                this.$state = $state;
                this.publicationsService = publicationsService;
                this._publication = {};
                this._publication['tid'] = $state.params['id'].split(':')[0];
                this._publication['hid'] = $state.params['id'].split(':')[1];
                $scope.showPublication = true;
                $scope.publicationLoaded = true;
                $scope.publication = {};
                $scope.publicationTemplateUrl = '/ajax/template/cabinet/publications/unpublished/' + this._publication['tid'] + '/';
                this.loadPublicationData();
            }
            PublicationController.prototype.loadPublicationData = function () {
                var _this = this;
                this.$scope.publicationLoaded = false;
                this.publicationsService.loadPublicationData(this._publication, function (response) {
                    _this.$scope.publicationLoaded = true;
                    _this.$scope.publication = response.data;
                });
                this.$timeout(function () { return $('select').material_select(); }, 3000);
            };
            PublicationController.$inject = [
                '$scope',
                '$timeout',
                '$state',
                'PublicationsService'
            ];
            return PublicationController;
        })();
        cabinet.PublicationController = PublicationController;
    })(cabinet = pages.cabinet || (pages.cabinet = {}));
})(pages || (pages = {}));
/// <reference path='../_references.ts' />
var pages;
(function (pages) {
    var cabinet;
    (function (cabinet) {
        var SettingsController = (function () {
            function SettingsController($timeout) {
                this.$timeout = $timeout;
                // -
                $timeout(function () { return $('select').material_select(); });
            }
            SettingsController.$inject = [
                '$timeout',
            ];
            return SettingsController;
        })();
        cabinet.SettingsController = SettingsController;
    })(cabinet = pages.cabinet || (pages.cabinet = {}));
})(pages || (pages = {}));
/// <reference path='../_references.ts' />
var pages;
(function (pages) {
    var cabinet;
    (function (cabinet) {
        var SupportController = (function () {
            function SupportController($timeout) {
                this.$timeout = $timeout;
                // -
            }
            SupportController.$inject = [
                '$timeout',
            ];
            return SupportController;
        })();
        cabinet.SupportController = SupportController;
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
            'ui.router',
            'bModules.Types',
            'bModules.Auth'
        ]);
        /** Providers configuration create */
        new cabinet.ProvidersConfigs(app);
        /** Routers configuration create */
        new cabinet.RoutersConfigs(app);
        /** Application configuration create */
        new cabinet.ApplicationConfigs(app);
        /** Module services */
        // -
        app.service('PublicationsService', cabinet.PublicationsService);
        /** Module controllers */
        app.controller('LoginController', cabinet.LoginController);
        app.controller('CabinetController', cabinet.CabinetController);
        app.controller('BriefsController', cabinet.BriefsController);
        app.controller('PublicationController', cabinet.PublicationController);
        app.controller('SettingsController', cabinet.SettingsController);
        app.controller('SupportController', cabinet.SupportController);
    })(cabinet = pages.cabinet || (pages.cabinet = {}));
})(pages || (pages = {}));
// ####################
// Declarations import
// ####################
/// <reference path='../_common/definitions/_references.ts' />
// ####################
// Interfaces import
// ####################
// ####################
// _modules import
// ####################
/// <reference path='../_common/bModules/Types/_references.ts' />
/// <reference path='../_common/bModules/Auth/_references.ts' />
// ####################
// Configs import
// ####################
/// <reference path='configs/ProvidersConfigs.ts' />
/// <reference path='configs/RoutersConfigs.ts' />
/// <reference path='configs/ApplicationConfigs.ts' />
// ####################
// Services import
// ####################
/// <reference path='services/PublicationsService.ts' />
// ####################
// Controllers import
// ####################
/// <reference path='controllers/LoginController.ts' />
/// <reference path='controllers/CabinetController.ts' />
/// <reference path='controllers/BriefsController.ts' />
/// <reference path='controllers/PublicationController.ts' />
/// <reference path='controllers/SettingsController.ts' />
/// <reference path='controllers/SupportController.ts' />
// ####################
// App init
// ####################
/// <reference path='App.ts' />
//# sourceMappingURL=cabinet.js.map