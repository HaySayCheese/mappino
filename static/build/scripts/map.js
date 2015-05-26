var bModules;
(function (bModules) {
    var Panels;
    (function (Panels) {
        var Panel = (function () {
            function Panel(_el, _panel_name, _state) {
                if (_state === void 0) { _state = 0; }
                this._el = _el;
                this._panel_name = _panel_name;
                this._state = _state;
                this.config = {
                    openedClass: 'opened',
                    closedClass: 'closed',
                    closingClass: 'closing'
                };
                // -
            }
            Object.defineProperty(Panel.prototype, "panel_name", {
                get: function () {
                    return this._panel_name;
                },
                enumerable: true,
                configurable: true
            });
            Object.defineProperty(Panel.prototype, "state", {
                get: function () {
                    return this._state;
                },
                set: function (state) {
                    if (this._state !== state) {
                        this._state = state;
                        state === 0 ? this.hide() : this.show();
                    }
                },
                enumerable: true,
                configurable: true
            });
            Panel.prototype.show = function () {
                this._el
                    .dequeue()
                    .removeClass(this.config['closedClass'])
                    .removeClass(this.config['closingClass'])
                    .addClass(this.config['openedClass']);
            };
            Panel.prototype.hide = function () {
                var self = this;
                // Якщо панель має клас 'this.config['openedClass']' (відкрита)
                // то закриваємо її
                // ця провірка потрібна що б не смикати панель спочатку у відкритий стан а потім закривати
                if (this._el.hasClass(this.config['openedClass'])) {
                    this._el
                        .removeClass(this.config['openedClass'])
                        .addClass(this.config['closingClass'])
                        .delay(500)
                        .queue(function () {
                        self._el
                            .removeClass(self.config['closingClass'])
                            .addClass(self.config['closedClass'])
                            .dequeue();
                    });
                }
                else {
                    this._el.addClass(this.config['closedClass']);
                }
            };
            return Panel;
        })();
        Panels.Panel = Panel;
    })(Panels = bModules.Panels || (bModules.Panels = {}));
})(bModules || (bModules = {}));
/// <reference path='_references.ts' />
var __extends = this.__extends || function (d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
    function __() { this.constructor = d; }
    __.prototype = b.prototype;
    d.prototype = new __();
};
var bModules;
(function (bModules) {
    var Panels;
    (function (Panels) {
        var DropPanel = (function (_super) {
            __extends(DropPanel, _super);
            function DropPanel(_el, _panel_name, _state) {
                if (_state === void 0) { _state = 0; }
                _super.call(this, _el, _panel_name, _state);
                this._el = _el;
                this._panel_name = _panel_name;
                this._state = _state;
            }
            return DropPanel;
        })(Panels.Panel);
        Panels.DropPanel = DropPanel;
    })(Panels = bModules.Panels || (bModules.Panels = {}));
})(bModules || (bModules = {}));
/// <reference path='_references.ts' />
/// <reference path='_references.ts' />
var bModules;
(function (bModules) {
    var Panels;
    (function (Panels) {
        'use strict';
        var DropPanelsHandler = (function () {
            function DropPanelsHandler($rootScope, $state) {
                this.$rootScope = $rootScope;
                this.$state = $state;
                this.panels = [];
                this.close_state_sid = 0;
                this.open_state_sid = 1;
                this.panels.push(new Panels.DropPanel(angular.element('.user-panel'), 'user'));
                this.panels.push(new Panels.DropPanel(angular.element('.menu-panel'), 'menu'));
            }
            DropPanelsHandler.prototype.isOpened = function (panel_name) {
                var panels = this.panels;
                for (var i = 0, len = panels.length; i < len; i++) {
                    if (panel_name === panels[i].panel_name)
                        return panels[i].state !== this.close_state_sid;
                }
            };
            DropPanelsHandler.prototype.open = function (panel_name, state) {
                if (state === void 0) { state = this.open_state_sid; }
                var panels = this.panels;
                for (var i = 0, len = panels.length; i < len; i++) {
                    if (panel_name === panels[i].panel_name) {
                        panels[i].state = state;
                        this.$rootScope.$broadcast('bModules.Panels.DropPanels.PanelOpened', {
                            panel_name: panel_name,
                            state: state,
                            is_opened: state !== this.close_state_sid
                        });
                    }
                }
            };
            DropPanelsHandler.prototype.close = function (panel_name) {
                var panels = this.panels;
                for (var i = 0, len = panels.length; i < len; i++) {
                    if (panel_name === panels[i].panel_name) {
                        panels[i].state = this.close_state_sid;
                        this.$rootScope.$broadcast('bModules.Panels.DropPanels.PanelClosed', {
                            panel_name: panel_name,
                            state: this.close_state_sid,
                            is_opened: false
                        });
                    }
                }
            };
            DropPanelsHandler.$inject = [
                '$rootScope',
                '$state'
            ];
            return DropPanelsHandler;
        })();
        Panels.DropPanelsHandler = DropPanelsHandler;
    })(Panels = bModules.Panels || (bModules.Panels = {}));
})(bModules || (bModules = {}));
/// <reference path='DropPanel.ts' />
/// <reference path='IDropPanelsHandler.ts' />
/// <reference path='DropPanelsHandler.ts' /> 
/// <reference path='_references.ts' />
var bModules;
(function (bModules) {
    var Panels;
    (function (Panels) {
        var SlidingPanel = (function (_super) {
            __extends(SlidingPanel, _super);
            function SlidingPanel(_el, _panel_name, _state) {
                if (_state === void 0) { _state = 0; }
                _super.call(this, _el, _panel_name, _state);
                this._el = _el;
                this._panel_name = _panel_name;
                this._state = _state;
            }
            return SlidingPanel;
        })(Panels.Panel);
        Panels.SlidingPanel = SlidingPanel;
    })(Panels = bModules.Panels || (bModules.Panels = {}));
})(bModules || (bModules = {}));
/// <reference path='_references.ts' />
/// <reference path='_references.ts' />
var bModules;
(function (bModules) {
    var Panels;
    (function (Panels) {
        'use strict';
        var SlidingPanelsHandler = (function () {
            function SlidingPanelsHandler($rootScope, $state) {
                var _this = this;
                this.$rootScope = $rootScope;
                this.$state = $state;
                this.panels = [];
                this.close_state_sid = 0;
                this.open_state_sid = 1;
                this.panels.push(new Panels.SlidingPanel(angular.element('.filters-panel'), 'filters'));
                this.panels.push(new Panels.SlidingPanel(angular.element('.favorites-panel'), 'favorites'));
                this.panels.push(new Panels.SlidingPanel(angular.element('.auth-panel'), 'auth'));
                this.$rootScope.$on('$stateChangeSuccess', function () { return _this.synchronize(); });
            }
            SlidingPanelsHandler.prototype.synchronize = function () {
                // Приоритет панелей якщо в урлі для декількох панелей задано значення відкритої
                // -
                if (parseInt(this.$state.params['filters']) !== this.close_state_sid &&
                    parseInt(this.$state.params['favorites']) !== this.close_state_sid) {
                    // -
                    this.$state.go('base', { favorites: this.close_state_sid });
                    return;
                }
                if (parseInt(this.$state.params['filters']) !== this.close_state_sid &&
                    parseInt(this.$state.params['auth']) !== this.close_state_sid) {
                    // -
                    this.$state.go('base', { auth: this.close_state_sid });
                    return;
                }
                if (parseInt(this.$state.params['favorites']) !== this.close_state_sid &&
                    parseInt(this.$state.params['auth']) !== this.close_state_sid) {
                    // -
                    this.$state.go('base', { auth: this.close_state_sid });
                    return;
                }
                this.switchState('filters', parseInt(this.$state.params['filters']));
                this.switchState('favorites', parseInt(this.$state.params['favorites']));
                this.switchState('auth', parseInt(this.$state.params['auth']));
            };
            SlidingPanelsHandler.prototype.switchState = function (panel_name, state) {
                var panels = this.panels;
                for (var i = 0, len = panels.length; i < len; i++) {
                    if (panel_name === panels[i].panel_name) {
                        panels[i].state = state;
                        this.$rootScope.$broadcast('bModules.Panels.SlidingPanels.PanelSwitchState', {
                            panel_name: panel_name,
                            state: state,
                            is_opened: state !== this.close_state_sid
                        });
                    }
                }
            };
            SlidingPanelsHandler.prototype.isOpened = function (panel_name) {
                var panels = this.panels;
                for (var i = 0, len = panels.length; i < len; i++) {
                    if (panel_name === panels[i].panel_name)
                        return panels[i].state !== this.close_state_sid;
                }
            };
            SlidingPanelsHandler.prototype.open = function (panel_name, state) {
                if (state === void 0) { state = this.open_state_sid; }
                switch (panel_name) {
                    case 'filters':
                        this.$state.go('base', { filters: state, favorites: this.close_state_sid, auth: this.close_state_sid });
                        break;
                    case 'favorites':
                        this.$state.go('base', { filters: this.close_state_sid, favorites: state, auth: this.close_state_sid });
                        break;
                    case 'auth':
                        this.$state.go('base', { filters: this.close_state_sid, favorites: this.close_state_sid, auth: state });
                        break;
                }
                this.$rootScope.$broadcast('bModules.Panels.SlidingPanels.PanelOpened', {
                    panel_name: panel_name,
                    state: state,
                    is_opened: state !== this.close_state_sid
                });
            };
            SlidingPanelsHandler.prototype.close = function (panel_name) {
                switch (panel_name) {
                    case 'filters':
                        this.$state.go('base', { filters: this.close_state_sid });
                        break;
                    case 'favorites':
                        this.$state.go('base', { favorites: this.close_state_sid });
                        break;
                    case 'auth':
                        this.$state.go('base', { auth: this.close_state_sid });
                        break;
                }
                this.$rootScope.$broadcast('bModules.Panels.SlidingPanels.PanelClosed', {
                    panel_name: panel_name,
                    state: this.close_state_sid,
                    is_opened: false
                });
            };
            SlidingPanelsHandler.$inject = [
                '$rootScope',
                '$state'
            ];
            return SlidingPanelsHandler;
        })();
        Panels.SlidingPanelsHandler = SlidingPanelsHandler;
    })(Panels = bModules.Panels || (bModules.Panels = {}));
})(bModules || (bModules = {}));
/// <reference path='SlidingPanel.ts' />
/// <reference path='ISlidingPanelsHandler.ts' />
/// <reference path='SlidingPanelsHandler.ts' /> 
/// <reference path='../../definitions/angular.d.ts' />
/// <reference path='Panel/Panel.ts' />
/// <reference path='DropPanels/_references.ts' />
/// <reference path='SlidingPanels/_references.ts' /> 
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
    var map;
    (function (map) {
        'use strict';
        var ProvidersConfigs = (function () {
            function ProvidersConfigs(app) {
                this.app = app;
                app.config(['$interpolateProvider', '$resourceProvider', '$locationProvider',
                    function ($interpolateProvider, $resourceProvider, $locationProvider) {
                        $interpolateProvider.startSymbol('[[');
                        $interpolateProvider.endSymbol(']]');
                        $resourceProvider.defaults.stripTrailingSlashes = false;
                    }
                ]);
            }
            return ProvidersConfigs;
        })();
        map.ProvidersConfigs = ProvidersConfigs;
    })(map = pages.map || (pages.map = {}));
})(pages || (pages = {}));
/// <reference path='../_references.ts' />
var pages;
(function (pages) {
    var map;
    (function (map) {
        'use strict';
        var RoutersConfigs = (function () {
            function RoutersConfigs(app) {
                this.app = app;
                app.config(['$stateProvider', '$urlRouterProvider', '$locationProvider', function ($stateProvider, $urlRouterProvider, $locationProvider) {
                        //
                        // For any unmatched url, redirect to /state1
                        $urlRouterProvider.otherwise("/0/1/0/gdsg/");
                        //
                        // Now set up the states
                        $stateProvider
                            .state('base', {
                            url: "/:auth/:filters/:favorites/:publication/"
                        });
                        $locationProvider.hashPrefix('!');
                    }]);
            }
            return RoutersConfigs;
        })();
        map.RoutersConfigs = RoutersConfigs;
    })(map = pages.map || (pages.map = {}));
})(pages || (pages = {}));
/// <reference path='../_references.ts' />
var pages;
(function (pages) {
    var map;
    (function (map) {
        'use strict';
        var ApplicationConfigs = (function () {
            function ApplicationConfigs(app) {
                this.app = app;
                app.run(['$http', '$cookies', function ($http, $cookies) {
                        return $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
                    }
                ]);
            }
            return ApplicationConfigs;
        })();
        map.ApplicationConfigs = ApplicationConfigs;
    })(map = pages.map || (pages.map = {}));
})(pages || (pages = {}));
/// <reference path='../_references.ts' />
var pages;
(function (pages) {
    var map;
    (function (map) {
        'use strict';
        var FiltersService = (function () {
            function FiltersService($rootScope, $timeout, $location, realtyTypesService) {
                this.$rootScope = $rootScope;
                this.$timeout = $timeout;
                this.$location = $location;
                this.realtyTypesService = realtyTypesService;
                this._filters = {
                    map: {
                        c: null,
                        l: "48.455935,34.41285",
                        v: null,
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
                        op_sid: 0,
                        // Дропдауни
                        cu_sid: 0,
                        h_t_sid: 0,
                        pr_sid: 0,
                        pl_sid: 0,
                        b_t_sid: 0,
                        // Поля вводу
                        p_min: null,
                        p_max: null,
                        r_c_min: null,
                        r_c_max: null,
                        f_c_min: null,
                        f_c_max: null,
                        p_c_min: null,
                        p_c_max: null,
                        t_a_min: null,
                        t_a_max: null,
                        f_min: null,
                        f_max: null,
                        h_a_min: null,
                        h_a_max: null,
                        c_c_min: null,
                        c_c_max: null,
                        h_c_min: null,
                        h_c_max: null,
                        c_h_min: null,
                        c_h_max: null,
                        a_min: null,
                        a_max: null,
                        // Чекбокси
                        n_b: true,
                        s_m: true,
                        fml: false,
                        frg: false,
                        elt: false,
                        gas: false,
                        h_w: false,
                        c_w: false,
                        swg: false,
                        lft: false,
                        sct: false,
                        ktn: false,
                        s_a: false,
                        f_a: false,
                        pit: false,
                        wtr: false,
                        msd: true,
                        grd: true // ground
                    }
                };
                this._filters_for_load_markers = {
                    zoom: null,
                    viewport: null,
                    filters: []
                };
                // -
                this.updateFiltersFromUrl();
                this.updateUrlFromPanelsFilters();
            }
            FiltersService.prototype.update = function (filter_object, filter_name, filter_value) {
                var _this = this;
                this._filters[filter_object][filter_name] = filter_value;
                if (filter_object === 'map') {
                    this.updateUrlFromMapFilters();
                }
                else {
                    this.updateUrlFromPanelsFilters();
                }
                this.createFormattedObjectForLoadMarkers(filter_name, filter_value);
                this.$timeout(function () { return _this.$rootScope.$broadcast('pages.map.FiltersService.FiltersUpdated', _this._filters); });
            };
            Object.defineProperty(FiltersService.prototype, "filters", {
                get: function () {
                    return this._filters;
                },
                enumerable: true,
                configurable: true
            });
            //public createStringFromFilters() {
            //    var location_search = {},
            //        filters_panels = this._filters['panels'];
            //
            //    for (var key in filters_panels) {
            //        if (filters_panels.hasOwnProperty(key)) {
            //
            //            if (filters[key] !== false && filters[key] !== "false" && filters[key] !== "" && filters[key] !== null) {
            //                var param = key.toString().substring(2),
            //                    value = filters[key];
            //
            //                location_search[param] = value;
            //            }
            //        }
            //    }
            //    location_search['panel'] = panel;
            //
            //    jsonFilters.filters.push(location_search);
            //}
            FiltersService.prototype.createFiltersForPanel = function (panel_color) {
                var _this = this;
                var self = this, panel_prefix = panel_color.toString().substring(0, 1) + "_", type_sid = this._filters['panels'][panel_color][panel_prefix + 't_sid'], location_search = this.$location.search();
                if (_.isNull(type_sid)) {
                    // Очищаємо обєкт з фільтрами
                    this._filters['panels'][panel_color] = {};
                    // Створюємо параметр з типом оголошення в обєкті з фільтрами
                    this._filters['panels'][panel_color][panel_prefix + "t_sid"] = type_sid;
                    // Видаляємо фільтри з урла
                    for (var s_key in location_search) {
                        if (location_search.hasOwnProperty(s_key)) {
                            if (s_key.match(new RegExp('^' + panel_prefix, 'm'))) {
                                this.$location.search(s_key, null);
                            }
                        }
                    }
                }
                // Створюємо набір фільтрів для панелі за набором
                if (!_.isNull(type_sid)) {
                    var realty_type_filters = _.where(self.realtyTypesService.realty_types, { 'id': type_sid })[0]['filters'];
                    for (var i = 0, len = realty_type_filters.length; i < len; i++) {
                        var filter_name = panel_prefix + realty_type_filters[i];
                        if (_.isUndefined(this._filters['panels'][panel_color][filter_name])) {
                            this._filters['panels'][panel_color][filter_name] = this._filters['base'][realty_type_filters[i]];
                        }
                    }
                }
                this.$timeout(function () { return _this.$rootScope.$broadcast('pages.map.FiltersService.FiltersUpdated', _this._filters); });
            };
            FiltersService.prototype.updateFiltersFromUrl = function () {
                var _this = this;
                var location_search = this.$location.search(), filters_panels = this._filters['panels'];
                for (var key in location_search) {
                    if (location_search.hasOwnProperty(key)) {
                        if (key.toString() === "token") {
                            continue;
                        }
                        if (location_search[key] === 'true') {
                            location_search[key] = true;
                        }
                        if (location_search[key] === 'false') {
                            location_search[key] = false;
                        }
                        if (key.toString().indexOf("_sid") !== -1) {
                            location_search[key] = parseInt(location_search[key]);
                        }
                        if (/^r_/.test(key.toString())) {
                            filters_panels['red'][key] = location_search[key];
                        }
                        if (/^b_/.test(key.toString())) {
                            filters_panels['blue'][key] = location_search[key];
                        }
                        if (/^g_/.test(key.toString())) {
                            filters_panels['green'][key] = location_search[key];
                        }
                        if (/^y_/.test(key.toString())) {
                            filters_panels['yellow'][key] = location_search[key];
                        }
                        if (_.include(['c', 'l', 'z'], key)) {
                            this._filters['map'][key] = location_search[key];
                        }
                    }
                }
                if (_.isUndefined(location_search['r_t_sid']) && _.isUndefined(location_search['b_t_sid']) &&
                    _.isUndefined(location_search['g_t_sid']) && _.isUndefined(location_search['y_t_sid'])) {
                    // -
                    filters_panels['red']['r_t_sid'] = 0;
                    this.createFiltersForPanel("red");
                }
                if (!_.isUndefined(location_search['r_t_sid'])) {
                    this.createFiltersForPanel("red");
                }
                if (!_.isUndefined(location_search['b_t_sid'])) {
                    this.createFiltersForPanel("blue");
                }
                if (!_.isUndefined(location_search['g_t_sid'])) {
                    this.createFiltersForPanel("green");
                }
                if (!_.isUndefined(location_search['y_t_sid'])) {
                    this.createFiltersForPanel("yellow");
                }
                this.$timeout(function () { return _this.$rootScope.$broadcast('pages.map.FiltersService.UpdatedFromUrl', _this._filters); });
            };
            FiltersService.prototype.updateUrlFromMapFilters = function () {
                var filters_map = this._filters['map'];
                for (var filter in filters_map) {
                    if (filters_map.hasOwnProperty(filter) && !_.include(['v'], filter)) {
                        this.$location.search(filter, filters_map[filter]);
                        if (!this.$rootScope.$$phase)
                            this.$rootScope.$apply();
                    }
                }
                //this._filters_for_load_markers['zoom'] = filters_map['z'];
                //this._filters_for_load_markers['viewport'] = filters_map['v'];
                console.info('updateUrlFromMapFilters method: map filters updated');
            };
            FiltersService.prototype.updateUrlFromPanelsFilters = function () {
                var location_search = '', filters_panels = this._filters['panels'], _formattedPanelFilters = {};
                for (var panel in filters_panels) {
                    if (filters_panels.hasOwnProperty(panel)) {
                        _formattedPanelFilters = {
                            panel: panel
                        };
                        for (var filter in filters_panels[panel]) {
                            if (filters_panels[panel].hasOwnProperty(filter)) {
                                if (filter.indexOf("t_sid") !== -1 && _.isNull(filters_panels[panel][filter])) {
                                    _formattedPanelFilters = null;
                                    continue;
                                }
                                if (_.include(['', null], filters_panels[panel][filter])) {
                                    continue;
                                }
                                _formattedPanelFilters[filter.substr(2, filter.length)] = filters_panels[panel][filter];
                                if (filters_panels[panel][filter] === this._filters['base'][filter.substr(2, filter.length)]) {
                                    continue;
                                }
                                // i love js
                                //if (_.include(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], filters_panels[panel][filter])) {
                                //    filters_panels[panel][filter] = parseInt(filters_panels[panel][filter]);
                                //}
                                location_search += (location_search.length !== 0 ? '&' : '') + filter + '=' + filters_panels[panel][filter];
                            }
                        }
                        if (!_.isNull(_formattedPanelFilters))
                            this._filters_for_load_markers['filters'].push(_formattedPanelFilters);
                    }
                }
                console.info('updateUrlFromPanelsFilters method: panels filters updated');
                this.$location.search(location_search);
                if (!this.$rootScope.$$phase)
                    this.$rootScope.$apply();
                //$rootScope.searchUrlPart = base64.urlencode(location_search);
                //$location.search(base64.urlencode(location_search));
            };
            FiltersService.prototype.createFormattedObjectForLoadMarkers = function (filter_name, filter_value) {
                var _this = this;
                switch (filter_name) {
                    case 'z':
                        this._filters_for_load_markers['zoom'] = filter_value;
                        break;
                    case 'v':
                        this.createFormattedViewportForLoadMarkers();
                }
                this.$timeout(function () { return _this.$rootScope.$broadcast('pages.map.FiltersService.CreatedFormattedFilters', _this._filters_for_load_markers); });
            };
            FiltersService.prototype.createFormattedViewportForLoadMarkers = function () {
                var filters_map = this._filters['map'];
                var sneLat = filters_map['v'].getNorthEast().lat().toString(), sneLng = filters_map['v'].getNorthEast().lng().toString(), sswLat = filters_map['v'].getSouthWest().lat().toString(), sswLng = filters_map['v'].getSouthWest().lng().toString();
                var neLat = sneLat.replace(sneLat.substring(sneLat.indexOf(".") + 3, sneLat.length), ""), neLng = sneLng.replace(sneLng.substring(sneLng.indexOf(".") + 3, sneLng.length), ""), swLat = sswLat.replace(sswLat.substring(sswLat.indexOf(".") + 3, sswLat.length), ""), swLng = sswLng.replace(sswLng.substring(sswLng.indexOf(".") + 3, sswLng.length), "");
                this._filters_for_load_markers['viewport'] = {
                    'ne_lat': neLat,
                    'ne_lng': neLng,
                    'sw_lat': swLat,
                    'sw_lng': swLng
                };
                console.log(this._filters_for_load_markers);
            };
            FiltersService.$inject = [
                '$rootScope',
                '$timeout',
                '$location',
                'RealtyTypesService'
            ];
            return FiltersService;
        })();
        map.FiltersService = FiltersService;
    })(map = pages.map || (pages.map = {}));
})(pages || (pages = {}));
/// <reference path='../_references.ts' />
var pages;
(function (pages) {
    var map;
    (function (map_1) {
        'use strict';
        var MarkersService = (function () {
            function MarkersService($rootScope, $http, $q, $timeout) {
                this.$rootScope = $rootScope;
                this.$http = $http;
                this.$q = $q;
                this.$timeout = $timeout;
                this._response_markers = {
                    red: {
                        '47.8125:25.87522': 1
                    }
                };
                this._markers_to_remove = {
                    red: {}
                };
                this._markers_to_place = {
                    red: {}
                };
                // -
                var self = this;
                $rootScope.$on('pages.map.FiltersService.CreatedFormattedFilters', function (event, formatted_filters) {
                    self._filters_for_load_markers = formatted_filters;
                    console.log(JSON.stringify(self._filters_for_load_markers));
                    self.load();
                });
            }
            MarkersService.prototype.load = function () {
                var self = this;
                if (this._load_markers_canceler)
                    this._load_markers_canceler.resolve();
                this._load_markers_canceler = this.$q.defer();
                this.$http.get('/ajax/api/markers/?p=' + JSON.stringify(this._filters_for_load_markers), {
                    timeout: this._load_markers_canceler.promise
                }).success(function (response) {
                    self._response_markers = response;
                    self.intersection(response);
                });
            };
            MarkersService.prototype.intersection = function (_new_response_markers) {
                var _this = this;
                var self = this;
                self._markers_to_place['red'] = {};
                self._response_markers['red']['47.8125111:25.87522'] = 1;
                console.log(self._response_markers);
                console.log(_new_response_markers);
                // find unique
                for (var panel in _new_response_markers) {
                    if (_new_response_markers.hasOwnProperty(panel)) {
                        for (var marker in _new_response_markers[panel]) {
                            if (_new_response_markers[panel].hasOwnProperty(marker)) {
                                if (_.isUndefined(self._response_markers[panel][marker])) {
                                    self._markers_to_place[panel][marker] = _new_response_markers[panel][marker];
                                    //self._response_markers[panel][marker] = _new_response_markers[panel][marker];
                                    console.log(self._markers_to_place);
                                }
                            }
                        }
                    }
                }
                // find old
                for (var panel in self._response_markers) {
                    if (self._response_markers.hasOwnProperty(panel)) {
                        for (var marker in self._response_markers[panel]) {
                            if (self._response_markers[panel].hasOwnProperty(marker)) {
                                if (_.isUndefined(_new_response_markers[panel][marker])) {
                                    self._markers_to_remove[panel][marker] = self._response_markers[panel][marker];
                                    console.log(self._markers_to_remove);
                                }
                            }
                        }
                    }
                }
                this.$timeout(function () { return _this.$rootScope.$broadcast('pages.map.MarkersService.MarkersDone'); });
            };
            MarkersService.prototype.place = function (map) {
                for (var panel in this._markers_to_place) {
                    if (this._markers_to_place.hasOwnProperty(panel)) {
                        for (var marker in this._markers_to_place[panel]) {
                            if (this._markers_to_place[panel].hasOwnProperty(marker)) {
                                var _marker = new google.maps.Marker({
                                    position: new google.maps.LatLng(marker.split(':')[0], marker.split(':')[1]),
                                    map: map,
                                    title: 'Hello World!'
                                });
                                console.log('place');
                            }
                        }
                    }
                }
            };
            MarkersService.$inject = [
                '$rootScope',
                '$http',
                '$q',
                '$timeout'
            ];
            return MarkersService;
        })();
        map_1.MarkersService = MarkersService;
    })(map = pages.map || (pages.map = {}));
})(pages || (pages = {}));
/// <reference path='../_references.ts' />
var pages;
(function (pages) {
    var map;
    (function (map) {
        'use strict';
        var AppController = (function () {
            function AppController($rootScope, $location, dropPanelsHandler, slidingPanelsHandler) {
                this.$rootScope = $rootScope;
                this.$location = $location;
                this.dropPanelsHandler = dropPanelsHandler;
                this.slidingPanelsHandler = slidingPanelsHandler;
                // -
                var self = this;
                /**
                 * Відновлюємо фільтри в урлі після зміни панелі
                 **/
                $rootScope.$on('$stateChangeStart', function () {
                    if (!_.isNull($location.search()))
                        self._location_search = $location.search();
                });
                $rootScope.$on('$stateChangeSuccess', function () {
                    if (!_.isNull(self._location_search))
                        $location.search(self._location_search);
                });
            }
            AppController.$inject = [
                '$rootScope',
                '$location',
                'DropPanelsHandler',
                'SlidePanelsHandler'
            ];
            return AppController;
        })();
        map.AppController = AppController;
    })(map = pages.map || (pages.map = {}));
})(pages || (pages = {}));
/// <reference path='../_references.ts' />
var pages;
(function (pages) {
    var map;
    (function (map) {
        'use strict';
        var TabsNavigationController = (function () {
            function TabsNavigationController($scope, $timeout) {
                // -
                this.$scope = $scope;
                this.$timeout = $timeout;
                // Materialize: init .tabs()
                $timeout(function () { return $('.tabs').tabs(); });
            }
            TabsNavigationController.$inject = [
                '$scope',
                '$timeout',
                'SlidePanelsHandler'
            ];
            return TabsNavigationController;
        })();
        map.TabsNavigationController = TabsNavigationController;
    })(map = pages.map || (pages.map = {}));
})(pages || (pages = {}));
/// <reference path='../_references.ts' />
var pages;
(function (pages) {
    var map;
    (function (map) {
        'use strict';
        var FiltersPanelController = (function () {
            function FiltersPanelController($scope, $timeout, filtersService, realtyTypesService) {
                this.$scope = $scope;
                this.$timeout = $timeout;
                this.filtersService = filtersService;
                this.realtyTypesService = realtyTypesService;
                // -
                $timeout(function () { return $('select').material_select(); });
                $scope.realtyTypes = realtyTypesService.realty_types;
                this.filters = $scope.filters = filtersService.filters['panels'];
            }
            FiltersPanelController.$inject = [
                '$scope',
                '$timeout',
                'FiltersService',
                'RealtyTypesService'
            ];
            return FiltersPanelController;
        })();
        map.FiltersPanelController = FiltersPanelController;
    })(map = pages.map || (pages.map = {}));
})(pages || (pages = {}));
/// <reference path='../_references.ts' />
var pages;
(function (pages) {
    var map;
    (function (map) {
        'use strict';
        var MapController = (function () {
            function MapController($scope, filtersService, markersService) {
                var _this = this;
                this.$scope = $scope;
                this.filtersService = filtersService;
                this.markersService = markersService;
                // -
                var self = this;
                google.maps.event.addDomListener(window, "load", function () { return _this.initMap(_this); });
                $scope.$on('pages.map.MarkersService.MarkersDone', function () {
                    markersService.place(self._map);
                });
                $scope.$on('pages.map.PlaceAutocompleteController.PlaceChanged', function (event, place) {
                    self.positioningMap(place);
                });
            }
            MapController.prototype.initMap = function (self) {
                self._map = new google.maps.Map(document.getElementById("map"), {
                    center: new google.maps.LatLng(this.filtersService.filters['map']['l'].split(',')[0], this.filtersService.filters['map']['l'].split(',')[1]),
                    zoom: parseInt(this.filtersService.filters['map']['z']),
                    mapTypeId: google.maps.MapTypeId.ROADMAP,
                    disableDefaultUI: true
                });
                google.maps.event.addListener(self._map, 'idle', function () {
                    self.filtersService.update('map', 'z', self._map.getZoom());
                    self.filtersService.update('map', 'v', self._map.getBounds());
                    self.filtersService.update('map', 'l', self._map.getCenter().toUrlValue());
                });
            };
            MapController.prototype.positioningMap = function (place) {
                if (!place.geometry)
                    return;
                if (place.geometry.viewport) {
                    this._map.fitBounds(place.geometry.viewport);
                }
                else {
                    this._map.setCenter(place.geometry.location);
                    this._map.setZoom(17);
                }
            };
            MapController.$inject = [
                '$scope',
                'FiltersService',
                'MarkersService'
            ];
            return MapController;
        })();
        map.MapController = MapController;
    })(map = pages.map || (pages.map = {}));
})(pages || (pages = {}));
/// <reference path='../_references.ts' />
var pages;
(function (pages) {
    var map;
    (function (map) {
        'use strict';
        var PlaceAutocompleteController = (function () {
            function PlaceAutocompleteController($scope, $rootScope, filtersService) {
                var _this = this;
                this.$scope = $scope;
                this.$rootScope = $rootScope;
                this.filtersService = filtersService;
                // -
                this._autocompleteInput = document.getElementById("place-autocomplete");
                /** Listen events */
                google.maps.event.addDomListener(window, "load", function () { return _this.initAutocomplete(_this); });
                $scope.$on('pages.map.FiltersService.UpdatedFromUrl', function (event, filters) {
                    _this._autocompleteInput.value = filters['map']['c'];
                });
            }
            PlaceAutocompleteController.prototype.initAutocomplete = function (self) {
                self._autocomplete = new google.maps.places.Autocomplete(this._autocompleteInput, {
                    componentRestrictions: {
                        country: "ua"
                    }
                });
                google.maps.event.addListener(self._autocomplete, 'place_changed', function () {
                    self.filtersService.update('map', 'c', self._autocomplete.getPlace().formatted_address);
                    self.$rootScope.$broadcast('pages.map.PlaceAutocompleteController.PlaceChanged', self._autocomplete.getPlace());
                });
            };
            PlaceAutocompleteController.$inject = [
                '$scope',
                '$rootScope',
                'FiltersService'
            ];
            return PlaceAutocompleteController;
        })();
        map.PlaceAutocompleteController = PlaceAutocompleteController;
    })(map = pages.map || (pages.map = {}));
})(pages || (pages = {}));
/// <reference path='_references.ts' />
var pages;
(function (pages) {
    var map;
    (function (map) {
        'use strict';
        var app = angular.module('mappino.pages.map', [
            //'ngRoute',
            'ngCookies',
            //'ngAnimate',
            'ngResource',
            //
            //'ui.mask',
            'ui.router',
        ]);
        /** Providers configuration create */
        new map.ProvidersConfigs(app);
        /** Routers configuration create */
        new map.RoutersConfigs(app);
        /** Application configuration create */
        new map.ApplicationConfigs(app);
        /** Module services */
        app.service('DropPanelsHandler', bModules.Panels.DropPanelsHandler);
        app.service('SlidePanelsHandler', bModules.Panels.SlidingPanelsHandler);
        app.service('RealtyTypesService', bModules.Types.RealtyTypesService);
        app.service('FiltersService', map.FiltersService);
        app.service('MarkersService', map.MarkersService);
        /** Module controllers */
        app.controller('AppController', map.AppController);
        app.controller('TabsNavigationController', map.TabsNavigationController);
        app.controller('FiltersPanelController', map.FiltersPanelController);
        app.controller('MapController', map.MapController);
        app.controller('PlaceAutocompleteController', map.PlaceAutocompleteController);
    })(map = pages.map || (pages.map = {}));
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
/// <reference path='interfaces/IFiltersService.ts' />
// ####################
// _modules import
// ####################
/// <reference path='../_common/bModules/Panels/_references.ts' />
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
/// <reference path='services/FiltersService.ts' />
/// <reference path='services/MarkersService.ts' />
// ####################
// Controllers import
// ####################
/// <reference path='controllers/AppController.ts' />
/// <reference path='controllers/TabsNavigationController.ts' />
/// <reference path='controllers/FiltersPanelController.ts' />
/// <reference path='controllers/MapController.ts' />
/// <reference path='controllers/PlaceAutocompleteController.ts' />
// ####################
// App init
// ####################
/// <reference path='App.ts' />
