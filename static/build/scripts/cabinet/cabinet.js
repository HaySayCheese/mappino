/// <reference path='angular.d.ts' />
/// <reference path='angular-cookies.d.ts' />
/// <reference path='angular-ui-router.d.ts' />
/// <reference path='custom.d.ts' />
/// <reference path='google.maps.d.ts' />
/// <reference path='jquery.d.ts' />
/// <reference path='underscore.d.ts' />
/// <reference path='../_references.ts' />
/// <reference path='../_references.ts' />
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
/// <reference path='../_references.ts' />
var bModules;
(function (bModules) {
    var Types;
    (function (Types) {
        var CurrencyTypesService = (function () {
            function CurrencyTypesService() {
                this._currency_types = [{
                        id: '0',
                        name: 'USD',
                        title: 'Дол.'
                    }, {
                        id: '1',
                        name: 'EUR',
                        title: 'Евро'
                    }, {
                        id: '2',
                        name: 'UAH',
                        title: 'Грн.'
                    }];
            }
            Object.defineProperty(CurrencyTypesService.prototype, "currency_types", {
                get: function () {
                    return this._currency_types;
                },
                enumerable: true,
                configurable: true
            });
            return CurrencyTypesService;
        })();
        Types.CurrencyTypesService = CurrencyTypesService;
    })(Types = bModules.Types || (bModules.Types = {}));
})(bModules || (bModules = {}));
/// <reference path='../_references.ts' />
var bModules;
(function (bModules) {
    var Types;
    (function (Types) {
        var PeriodTypesService = (function () {
            function PeriodTypesService() {
                this._period_types = [{
                        id: '0',
                        name: 'daily',
                        title: 'Посуточно'
                    }, {
                        id: '1',
                        name: 'monthly',
                        title: 'Помесячно'
                    }, {
                        id: '2',
                        name: 'long_term',
                        title: 'Долгосрочная'
                    }];
            }
            Object.defineProperty(PeriodTypesService.prototype, "period_types", {
                get: function () {
                    return this._period_types;
                },
                enumerable: true,
                configurable: true
            });
            return PeriodTypesService;
        })();
        Types.PeriodTypesService = PeriodTypesService;
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
        bTypes.service('CurrencyTypesService', Types.CurrencyTypesService);
        bTypes.service('PeriodTypesService', Types.PeriodTypesService);
    })(Types = bModules.Types || (bModules.Types = {}));
})(bModules || (bModules = {}));
/// <reference path='../../definitions/_references.ts' />
/// <reference path='services/RealtyTypesService.ts' />
/// <reference path='services/CurrencyTypesService.ts' />
/// <reference path='services/PeriodTypesService.ts' />
/// <reference path='Types.ts' /> 
/// <reference path='../_references.ts' />
/// <reference path='../_references.ts' />
/// <reference path='../_references.ts' />
/// <reference path='../_references.ts' />
var bModules;
(function (bModules) {
    var Auth;
    (function (Auth) {
        var AuthService = (function () {
            function AuthService($http, settingsService) {
                this.$http = $http;
                this.settingsService = settingsService;
                // ---------------------------------------------------------------------------------------------------------
            }
            AuthService.prototype.login = function (user, success_callback, error_callback) {
                var self = this;
                this.$http.post('/ajax/api/accounts/login/', user)
                    .then(function (response) {
                    if (response.data['code'] === 0) {
                        self.settingsService.update(response.data['user']);
                        _.isFunction(success_callback) && success_callback(response.data);
                    }
                    else {
                        self.settingsService.clearDataByUser();
                        _.isFunction(error_callback) && error_callback(response.data);
                    }
                }, function (response) {
                    self.settingsService.clearDataByUser();
                    _.isFunction(error_callback) && error_callback(response.data);
                });
            };
            AuthService.prototype.getUserByCookie = function (success_callback, error_callback) {
                var self = this;
                this.$http.get('/ajax/api/accounts/on-login-info/')
                    .then(function (response) {
                    if (response.data['code'] === 0) {
                        self.settingsService.update(response.data['user']);
                        _.isFunction(success_callback) && success_callback(response.data);
                    }
                    else {
                        self.settingsService.clearDataByUser();
                        _.isFunction(error_callback) && error_callback(response.data);
                    }
                }, function (response) {
                    _.isFunction(error_callback) && error_callback(response.data);
                });
            };
            AuthService.$inject = [
                '$http',
                'SettingsService'
            ];
            return AuthService;
        })();
        Auth.AuthService = AuthService;
    })(Auth = bModules.Auth || (bModules.Auth = {}));
})(bModules || (bModules = {}));
/// <reference path='../_references.ts' />
var bModules;
(function (bModules) {
    var Auth;
    (function (Auth) {
        var SettingsService = (function () {
            function SettingsService($http, Upload) {
                this.$http = $http;
                this.Upload = Upload;
                this._user = {
                    account: {
                        name: null,
                        surname: null,
                        full_name: null,
                        avatar: null,
                        add_landline_phone: null,
                        add_mobile_phone: null,
                        email: null,
                        landline_phone: null,
                        mobile_phone: null,
                        skype: null,
                        work_email: null,
                    },
                    preferences: {
                        allow_call_requests: true,
                        allow_messaging: true,
                        hide_add_landline_phone_number: true,
                        hide_add_mobile_phone_number: true,
                        hide_email: true,
                        hide_landline_phone_number: true,
                        hide_mobile_phone_number: true,
                        hide_skype: true,
                        send_call_request_notifications_to_sid: 0,
                        send_message_notifications_to_sid: 0
                    }
                };
                // ---------------------------------------------------------------------------------------------------------
            }
            SettingsService.prototype.load = function (success_callback, error_callback) {
                var self = this;
                this.$http.get('/ajax/api/cabinet/account/')
                    .then(function (response) {
                    if (response.data['code'] === 0) {
                        self.update(response.data['data']['account']);
                        self.update(response.data['data']['preferences']);
                        _.isFunction(success_callback) && success_callback(self._user);
                    }
                    else {
                        _.isFunction(error_callback) && error_callback(response.data);
                    }
                }, function (response) {
                    _.isFunction(error_callback) && error_callback(response.data);
                });
            };
            SettingsService.prototype.check = function (field, success_callback, error_callback) {
                var self = this;
                this.$http.post('/ajax/api/cabinet/account/', field)
                    .then(function (response) {
                    if (response.data['code'] === 0) {
                        field['v'] = response.data['value'] ? response.data['value'] : field['v'];
                        var _field = {};
                        _field[field['f']] = field['v'];
                        self.update(_field);
                        _.isFunction(success_callback) && success_callback(field['v']);
                    }
                    else {
                        _.isFunction(error_callback) && error_callback(response.data);
                    }
                }, function (response) {
                    _.isFunction(error_callback) && error_callback(response.data);
                });
            };
            SettingsService.prototype.uploadAvatar = function (avatar, success_callback, error_callback) {
                var self = this;
                this.Upload.upload({
                    url: '/ajax/api/cabinet/account/photo/',
                    file: avatar
                }).success(function (response) {
                    if (response.code === 0) {
                        self.update({ avatar: response.data['url'] });
                        _.isFunction(success_callback) && success_callback(response);
                    }
                    else {
                        _.isFunction(error_callback) && error_callback(response);
                    }
                }).error(function (response) {
                    _.isFunction(error_callback) && error_callback(response);
                });
            };
            SettingsService.prototype.update = function (params) {
                for (var key in params) {
                    if (this._user.account[key] !== undefined) {
                        this._user.account[key] = params[key];
                        if (key === 'name' || key === 'surname') {
                            this._user.account.full_name = this._user.account.name + ' ' + this._user.account.surname;
                        }
                    }
                    if (this._user.preferences[key] != undefined) {
                        this._user.preferences[key] = params[key];
                    }
                }
                this.saveToStorages(this._user);
            };
            Object.defineProperty(SettingsService.prototype, "user", {
                get: function () {
                    return this._user;
                },
                enumerable: true,
                configurable: true
            });
            SettingsService.prototype.clearDataByUser = function () {
                if (localStorage && localStorage['user']) {
                    delete localStorage['user'];
                }
            };
            SettingsService.prototype.saveToStorages = function (user) {
                if (localStorage) {
                    localStorage['user'] = JSON.stringify(user);
                }
            };
            SettingsService.$inject = [
                '$http',
                'Upload'
            ];
            return SettingsService;
        })();
        Auth.SettingsService = SettingsService;
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
        bAuth.service('SettingsService', Auth.SettingsService);
    })(Auth = bModules.Auth || (bModules.Auth = {}));
})(bModules || (bModules = {}));
// ####################
// Declarations import
// ####################
/// <reference path='../../definitions/_references.ts' />
// ####################
// Interfaces import
// ####################
/// <reference path='interfaces/IUser.ts' />
/// <reference path='interfaces/IAuthService.ts' />
/// <reference path='interfaces/ISettingsService.ts' />
// ####################
// Services import
// ####################
/// <reference path='services/AuthService.ts' />
/// <reference path='services/SettingsService.ts' />
/// <reference path='Auth.ts' />
/// <reference path='../_references.ts' />
var bModules;
(function (bModules) {
    var Directives;
    (function (Directives) {
        function OnlyNumber() {
            return {
                restrict: 'A',
                require: 'ngModel',
                link: function (scope, element, attrs, modelCtrl) {
                    modelCtrl.$parsers.push(function (inputValue) {
                        // this next if is necessary for when using ng-required on your input.
                        // In such cases, when a letter is typed first, this parser will be called
                        // again, and the 2nd time, the value will be undefined
                        if (inputValue === undefined)
                            return '';
                        var transformedInput = inputValue.replace(/[^0-9]/g, '');
                        if (transformedInput !== inputValue) {
                            modelCtrl.$setViewValue(transformedInput);
                            modelCtrl.$render();
                        }
                        return transformedInput;
                    });
                }
            };
        }
        Directives.OnlyNumber = OnlyNumber;
    })(Directives = bModules.Directives || (bModules.Directives = {}));
})(bModules || (bModules = {}));
/// <reference path='_references.ts' />
var bModules;
(function (bModules) {
    var Directives;
    (function (Directives) {
        'use strict';
        var bDirectives = angular.module('bModules.Directives', []);
        bDirectives.directive('onlyNumber', Directives.OnlyNumber);
    })(Directives = bModules.Directives || (bModules.Directives = {}));
})(bModules || (bModules = {}));
/// <reference path='../../definitions/_references.ts' />
/// <reference path='directives/OnlyNumber.ts' />
/// <reference path='Directives.ts' /> 
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
                            .state('ticket_view', {
                            url: "/support/:ticket_id",
                            templateUrl: '/ajax/template/cabinet/support/ticket/'
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
                // ---------------------------------------------------------------------------------------------------------
            }
            PublicationsService.prototype.load = function (success_callback, error_callback) {
                var _this = this;
                this.$http.get('/ajax/api/cabinet/publications/briefs/all')
                    .then(function (response) {
                    if (response.data['code'] === 0) {
                        console.log(response.data['data']);
                        _this._publications = response.data['data'];
                        _.isFunction(success_callback) && success_callback(_this._publications);
                    }
                    else {
                        _.isFunction(error_callback) && error_callback(response.data);
                    }
                }, function (response) {
                    _.isFunction(error_callback) && error_callback(response.data);
                });
            };
            PublicationsService.prototype.create = function (publication, success_callback, error_callback) {
                var self = this;
                this.$http.post('/ajax/api/cabinet/publications/', publication)
                    .then(function (response) {
                    if (response.data['code'] === 0) {
                        self.$state.go('publication_edit', { id: publication['tid'] + ":" + response.data['data']['id'] });
                        _.isFunction(success_callback) && success_callback(response.data);
                    }
                    else {
                        _.isFunction(error_callback) && error_callback(response.data);
                    }
                }, function () {
                    _.isFunction(error_callback) && error_callback(response.data);
                });
            };
            PublicationsService.prototype.loadPublication = function (publication, success_callback, error_callback) {
                var _this = this;
                var self = this;
                this.$http.get('/ajax/api/cabinet/publications/' + publication['tid'] + ':' + publication['hid'] + '/')
                    .then(function (response) {
                    if (response.data['code'] === 0) {
                        console.log(response.data['data']);
                        _this._publication = response.data['data'];
                        _this.createDefaultTerms();
                        _.isFunction(success_callback) && success_callback(_this._publication);
                    }
                    else {
                        _.isFunction(error_callback) && error_callback(response.data);
                    }
                }, function (response) {
                    _.isFunction(error_callback) && error_callback(response.data);
                });
            };
            PublicationsService.prototype.createDefaultTerms = function () {
                if (_.isNull(this._publication['sale_terms'])) {
                    this._publication['sale_terms'] = {};
                    _.defaults(this._publication['sale_terms'], {
                        add_terms: null,
                        currency_sid: '0',
                        is_contract: false,
                        price: null,
                        sale_type_sid: '0',
                        transaction_sid: '0'
                    });
                }
                if (_.isNull(this._publication['rent_terms'])) {
                    this._publication['rent_terms'] = {};
                    _.defaults(this._publication['rent_terms'], {
                        add_terms: null,
                        currency_sid: '0',
                        is_contract: false,
                        period_sid: '1',
                        persons_count: null,
                        price: null,
                        rent_type_sid: '0'
                    });
                }
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
        var TicketsService = (function () {
            function TicketsService($http, $location) {
                this.$http = $http;
                this.$location = $location;
                // ---------------------------------------------------------------------------------------------------------
            }
            TicketsService.prototype.createTicket = function (success_callback, error_callback) {
                var self = this;
                this.$http.post('/ajax/api/cabinet/support/tickets/', null)
                    .then(function (response) {
                    if (response.data['code'] === 0) {
                        _.isFunction(success_callback) && success_callback(response.data['data']);
                    }
                    else {
                        _.isFunction(error_callback) && error_callback(response.data);
                    }
                }, function (response) {
                    _.isFunction(error_callback) && error_callback(response.data);
                });
            };
            TicketsService.prototype.loadTickets = function (success_callback, error_callback) {
                var self = this;
                this.$http.get('/ajax/api/cabinet/support/tickets/')
                    .then(function (response) {
                    if (response.data['code'] === 0) {
                        self._tickets = response.data['data'];
                        _.isFunction(success_callback) && success_callback(self._tickets);
                    }
                    else {
                        _.isFunction(error_callback) && error_callback(response.data);
                    }
                }, function (response) {
                    _.isFunction(error_callback) && error_callback(response.data);
                });
            };
            TicketsService.prototype.loadTicketMessages = function (ticket_id, success_callback, error_callback) {
                var self = this;
                this.$http.get('/ajax/api/cabinet/support/tickets/' + ticket_id + '/messages/')
                    .then(function (response) {
                    if (response.data['code'] === 0) {
                        _.isFunction(success_callback) && success_callback(response.data['data']);
                    }
                    else {
                        _.isFunction(error_callback) && error_callback(response.data);
                    }
                }, function (response) {
                    _.isFunction(error_callback) && error_callback(response.data);
                });
            };
            TicketsService.prototype.sendMessage = function (ticket_id, message, success_callback, error_callback) {
                var self = this;
                this.$http.post('/ajax/api/cabinet/support/tickets/' + ticket_id + '/messages/', message)
                    .then(function (response) {
                    if (response.data['code'] === 0) {
                        _.isFunction(success_callback) && success_callback(response.data);
                    }
                    else {
                        _.isFunction(error_callback) && error_callback(response.data);
                    }
                }, function (response) {
                    _.isFunction(error_callback) && error_callback(response.data);
                });
            };
            Object.defineProperty(TicketsService.prototype, "tickets", {
                get: function () {
                    return this._tickets;
                },
                enumerable: true,
                configurable: true
            });
            TicketsService.$inject = [
                '$http',
                '$location'
            ];
            return TicketsService;
        })();
        cabinet.TicketsService = TicketsService;
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
            function CabinetController($rootScope, authService, settingsService) {
                this.$rootScope = $rootScope;
                this.authService = authService;
                this.settingsService = settingsService;
                // -
                $(".button-collapse").sideNav();
                $rootScope.loaders = {
                    base: false,
                    avatar: false
                };
                authService.getUserByCookie();
            }
            CabinetController.$inject = [
                '$rootScope',
                'AuthService',
                'SettingsService'
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
                // ---------------------------------------------------------------------------------------------------------
                $scope.publications = [];
                $scope.new_publication = {
                    tid: 0,
                    for_sale: true,
                    for_rent: false
                };
                $scope.realtyTypes = realtyTypesService.realty_types;
                $timeout(function () { return $('select').material_select(); });
                this.loadPublications();
            }
            BriefsController.prototype.loadPublications = function () {
                var _this = this;
                this.publicationsService.load(function (response) {
                    _this.$scope.publications = response;
                });
            };
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
            function PublicationController($scope, $rootScope, $timeout, $state, currencyTypesService, periodTypesService, publicationsService) {
                // ---------------------------------------------------------------------------------------------------------
                this.$scope = $scope;
                this.$rootScope = $rootScope;
                this.$timeout = $timeout;
                this.$state = $state;
                this.currencyTypesService = currencyTypesService;
                this.periodTypesService = periodTypesService;
                this.publicationsService = publicationsService;
                this._publication = {};
                this._publication['tid'] = $state.params['id'].split(':')[0];
                this._publication['hid'] = $state.params['id'].split(':')[1];
                $scope.currencyTypes = currencyTypesService.currency_types;
                $scope.periodTypes = periodTypesService.period_types;
                $scope.publication = {};
                $scope.publicationTemplateUrl = '/ajax/template/cabinet/publications/unpublished/' + this._publication['tid'] + '/';
                this.loadPublicationData();
            }
            PublicationController.prototype.loadPublicationData = function () {
                var _this = this;
                this.$rootScope.loaders.base = true;
                this.publicationsService.loadPublication(this._publication, function (response) {
                    _this.$scope.publication = response;
                    _this.$rootScope.loaders.base = false;
                    _this.$timeout(function () { return $('select').material_select(); }, 0);
                });
            };
            PublicationController.$inject = [
                '$scope',
                '$rootScope',
                '$timeout',
                '$state',
                'CurrencyTypesService',
                'PeriodTypesService',
                'PublicationsService',
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
            function SettingsController($scope, $rootScope, $timeout, settingsService) {
                this.$scope = $scope;
                this.$rootScope = $rootScope;
                this.$timeout = $timeout;
                this.settingsService = settingsService;
                // ---------------------------------------------------------------------------------------------------------
                $rootScope.loaders.base = true;
                this.initInputsChange();
                settingsService.load(function (response) {
                    $scope.user = response;
                    $rootScope.loaders.base = false;
                    $timeout(function () {
                        angular.element(".settings-page input:not([type='file'], [type='checkbox'])").change();
                        $timeout(function () { return $('select').material_select(); });
                    });
                });
            }
            // used in scope, don't remove
            SettingsController.prototype.changePhoto = function (event) {
                event.preventDefault();
                angular.element('#photo-field').click();
            };
            SettingsController.prototype.initInputsChange = function () {
                var self = this;
                angular.element(".settings-page input[type='file']").bind('change', function (event) {
                    self.$rootScope.loaders.avatar = true;
                    self.settingsService.uploadAvatar(event.target['files'][0], function (response) {
                        self.$rootScope.loaders.avatar = false;
                        self.$scope.imageFatal = response.code === 1;
                        self.$scope.imageTooLarge = response.code === 2;
                        self.$scope.ImageTooSmall = response.code === 3;
                        self.$scope.ImageUndefined = response.code === 4;
                    });
                });
                angular.element(".settings-page input[type='text'], " +
                    ".settings-page input[type='tel'], " +
                    ".settings-page input[type='email']")
                    .bind("focusout", function (e) {
                    // -
                    var name = e.currentTarget['name'], value = e.currentTarget['value'].replace(/\s+/g, " ");
                    if (!self.$scope.form.user[name].$dirty) {
                        return;
                    }
                    if (name === "mobile_phone" && (value === "+38 (0__) __ - __ - ___" || value[22] === "_")) {
                        return;
                    }
                    self.settingsService.check({ f: name, v: value }, function (newValue) {
                        e.currentTarget['value'] = newValue;
                    }, function (response) {
                        self.$scope.form.user[name].$setValidity("incorrect", response.code !== 10);
                        self.$scope.form.user[name].$setValidity("duplicated", response.code !== 11);
                    });
                });
                angular.element(".settings-page input[type='checkbox']").bind("change", function (e) {
                    var name = e.currentTarget['name'], value = e.currentTarget['checked'];
                    self.settingsService.check({ f: name, v: value });
                });
                angular.element(".settings-page select").bind('change', function (e) {
                    var name = e.currentTarget['name'], value = e.currentTarget['value'];
                    self.settingsService.check({ f: name, v: value });
                });
            };
            SettingsController.$inject = [
                '$scope',
                '$rootScope',
                '$timeout',
                'SettingsService'
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
            function SupportController($scope, $rootScope, $state, ticketsService) {
                var _this = this;
                this.$scope = $scope;
                this.$rootScope = $rootScope;
                this.$state = $state;
                this.ticketsService = ticketsService;
                this._ticket = {
                    id: null,
                    created: null,
                    last_message: null,
                    state_sid: null,
                    subject: null,
                    messages: null
                };
                // ---------------------------------------------------------------------------------------------------------
                $scope.ticket = {};
                $scope.tickets = this._tickets = [];
                $rootScope.loaders.base = true;
                $scope.ticketFormIsVisible = false;
                ticketsService.loadTickets(function (response) {
                    _this._tickets = $scope.tickets = response;
                    $rootScope.loaders.base = false;
                });
            }
            SupportController.prototype.createTicket = function () {
                var _this = this;
                var self = this;
                this.ticketsService.createTicket(function (response) {
                    _this._ticket.id = self.$scope.ticket.id = response.id;
                    self.$scope.ticketFormIsVisible = true;
                    if (!self.$scope.$$phase) {
                        self.$scope.$apply();
                    }
                });
            };
            SupportController.prototype.sendMessage = function () {
                var _this = this;
                var self = this;
                this.ticketsService.sendMessage(this._ticket.id, this.$scope.ticket, function (response) {
                    self.$state.go('ticket_view', { ticket_id: _this._ticket.id });
                });
            };
            SupportController.$inject = [
                '$scope',
                '$rootScope',
                '$state',
                'TicketsService'
            ];
            return SupportController;
        })();
        cabinet.SupportController = SupportController;
    })(cabinet = pages.cabinet || (pages.cabinet = {}));
})(pages || (pages = {}));
/// <reference path='../_references.ts' />
var pages;
(function (pages) {
    var cabinet;
    (function (cabinet) {
        var TicketController = (function () {
            function TicketController($scope, $state, ticketsService, settingsService) {
                var _this = this;
                this.$scope = $scope;
                this.$state = $state;
                this.ticketsService = ticketsService;
                this.settingsService = settingsService;
                this._ticket = {
                    id: null,
                    created: null,
                    last_message: null,
                    state_sid: null,
                    subject: null,
                    messages: null
                };
                // ---------------------------------------------------------------------------------------------------------
                $scope.ticket = {};
                $scope.new_message = {};
                $scope.ticketIsLoaded = false;
                $scope.$on('$stateChangeSuccess', function (event, toState, toParams, fromState, fromParams) {
                    ticketsService.loadTicketMessages(toParams.ticket_id, function (response) {
                        _this._ticket.id = toParams.ticket_id;
                        _this._ticket.subject = response.subject;
                        _this._ticket.messages = response.messages;
                        $scope.ticket = _this._ticket;
                        $scope.ticketIsLoaded = true;
                    });
                });
            }
            TicketController.prototype.sendMessage = function () {
                var self = this;
                this.ticketsService.sendMessage(this._ticket.id, self.$scope.new_message, function (response) {
                    self.$scope.ticket.messages.unshift({
                        created: new Date().getTime(),
                        text: self.$scope.new_message.message,
                        type_sid: 0
                    });
                    if (self.$scope.new_message.subject) {
                        self.$scope.ticket.subject = self.$scope.new_message.subject;
                        self.$scope.new_message.subject = '';
                    }
                    self.$scope.new_message.message = '';
                });
            };
            TicketController.$inject = [
                '$scope',
                '$state',
                'TicketsService',
                'SettingsService'
            ];
            return TicketController;
        })();
        cabinet.TicketController = TicketController;
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
            'ui.mask',
            'ngFileUpload',
            'bModules.Types',
            'bModules.Auth',
            'bModules.Directives'
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
        app.service('TicketsService', cabinet.TicketsService);
        /** Module controllers */
        app.controller('LoginController', cabinet.LoginController);
        app.controller('CabinetController', cabinet.CabinetController);
        app.controller('BriefsController', cabinet.BriefsController);
        app.controller('PublicationController', cabinet.PublicationController);
        app.controller('SettingsController', cabinet.SettingsController);
        app.controller('SupportController', cabinet.SupportController);
        app.controller('TicketController', cabinet.TicketController);
    })(cabinet = pages.cabinet || (pages.cabinet = {}));
})(pages || (pages = {}));
// ####################
// Declarations import
// ####################
/// <reference path='../_common/definitions/_references.ts' />
// ####################
// Interfaces import
// ####################
/// <reference path='interfaces/ITicket.ts' />
/// <reference path='interfaces/ITicketsService.ts' />
// ####################
// _modules import
// ####################
/// <reference path='../_common/bModules/Types/_references.ts' />
/// <reference path='../_common/bModules/Auth/_references.ts' />
/// <reference path='../_common/bModules/Directives/_references.ts' />
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
/// <reference path='services/TicketsService.ts' />
// ####################
// Controllers import
// ####################
/// <reference path='controllers/LoginController.ts' />
/// <reference path='controllers/CabinetController.ts' />
/// <reference path='controllers/BriefsController.ts' />
/// <reference path='controllers/PublicationController.ts' />
/// <reference path='controllers/SettingsController.ts' />
/// <reference path='controllers/SupportController.ts' />
/// <reference path='controllers/TicketController.ts' />
// ####################
// App init
// ####################
/// <reference path='App.ts' />
//# sourceMappingURL=cabinet.js.map