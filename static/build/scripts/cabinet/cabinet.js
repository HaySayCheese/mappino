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
            function AuthService($http, settingsService) {
                this.$http = $http;
                this.settingsService = settingsService;
                // -
                this.getUserByCookie();
            }
            AuthService.prototype.login = function (user, callback) {
                var self = this;
                this.$http.post('/ajax/api/accounts/login/', user)
                    .then(function (response) {
                    if (response.data['code'] === 0) {
                        self.settingsService.update(response.data['user']);
                        callback(response);
                    }
                    else {
                        self.settingsService.clearDataByUser();
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
                        self.settingsService.update(response.data['user']);
                    }
                    else {
                        self.settingsService.clearDataByUser();
                    }
                }, function () {
                    // - error
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
                        name: '',
                        surname: '',
                        full_name: '',
                        avatar: '',
                        add_landline_phone: '',
                        add_mobile_phone: '',
                        email: '',
                        landline_phone: '',
                        mobile_phone: '',
                        skype: '',
                        work_email: '',
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
                // -
            }
            SettingsService.prototype.load = function (callback) {
                var self = this;
                this.$http.get('/ajax/api/cabinet/account/')
                    .then(function (response) {
                    if (response.data['code'] === 0) {
                        self.update(response.data['data']['account']);
                        self.update(response.data['data']['preferences']);
                        callback(self._user);
                    }
                    else {
                        callback(response);
                    }
                }, function () {
                    // - error
                });
            };
            SettingsService.prototype.check = function (field, callback) {
                var self = this;
                this.$http.post('/ajax/api/cabinet/account/', field)
                    .then(function (response) {
                    field['v'] = response.data['value'] ? response.data['value'] : field['v'];
                    var _field = {};
                    _field[field['f']] = field['v'];
                    self.update(_field);
                    callback(field['v'], response.data['code']);
                });
            };
            SettingsService.prototype.uploadAvatar = function (avatar, callback) {
                var self = this;
                this.Upload.upload({
                    url: '/ajax/api/cabinet/account/photo/',
                    file: avatar
                }).success(function (response) {
                    if (response.code === 0) {
                        callback(response);
                        console.log(response);
                        self.update({ avatar: response.data['url'] });
                    }
                    else {
                        callback(response);
                    }
                });
            };
            SettingsService.prototype.update = function (user) {
                for (var key in user) {
                    if (this._user['account'][key] != undefined) {
                        this._user['account'][key] = user[key];
                        if (key === 'name' || key === 'surname') {
                            this._user['account']['full_name'] = this._user['account']['name'] + ' ' + this._user['account']['surname'];
                        }
                    }
                    if (this._user['preferences'][key] != undefined) {
                        this._user['preferences'][key] = user[key];
                    }
                }
                this.saveToStorages(this._user);
                console.log(this._user);
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
/// <reference path='../../definitions/jquery.d.ts' />
/// <reference path='../../definitions/angular.d.ts' />
/// <reference path='../../definitions/angular-cookies.d.ts' />
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
            function CabinetController($timeout, settingsService) {
                this.$timeout = $timeout;
                this.settingsService = settingsService;
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
            function SettingsController($scope, $timeout, settingsService) {
                this.$scope = $scope;
                this.$timeout = $timeout;
                this.settingsService = settingsService;
                // -
                $scope.settingsIsLoaded = false;
                this.initInputsChange();
                settingsService.load(function (response) {
                    $scope.user = response;
                    $scope.settingsIsLoaded = true;
                    $timeout(function () {
                        angular.element(".settings-page input:not([type='file'], [type='checkbox'])").change();
                        $timeout(function () { return $('select').material_select(); });
                    });
                });
            }
            SettingsController.prototype.changePhoto = function (event) {
                event.preventDefault();
                angular.element('#photo-field').click();
            };
            SettingsController.prototype.initInputsChange = function () {
                var self = this;
                angular.element(".settings-page input[type='file']").bind('change', function (event) {
                    self.settingsService.uploadAvatar(event.target['files'][0], function (response) {
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
                    if (!self.$scope.form.user[name].$dirty)
                        return;
                    if (name === "mobile_phone" && (value === "+38 (0__) __ - __ - ___" || value[22] === "_"))
                        return;
                    self.settingsService.check({ f: name, v: value }, function (newValue, code) {
                        console.log(newValue);
                        console.log(code);
                        if (newValue)
                            e.currentTarget['value'] = newValue;
                        self.$scope.form.user[name].$setValidity("incorrect", code !== 10);
                        self.$scope.form.user[name].$setValidity("duplicated", code !== 11);
                    });
                });
                angular.element(".settings-page input[type='checkbox']").bind("change", function (e) {
                    var name = e.currentTarget['name'], value = e.currentTarget['checked'];
                    self.settingsService.check({ f: name, v: value }, null);
                });
                angular.element(".settings-page select").bind('change', function (e) {
                    var name = e.currentTarget['name'], value = e.currentTarget['value'];
                    self.settingsService.check({ f: name, v: value }, null);
                });
            };
            SettingsController.$inject = [
                '$scope',
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