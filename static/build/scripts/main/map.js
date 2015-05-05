/// <reference path='../_references.ts' />
var mappino;
(function (mappino) {
    var main;
    (function (main) {
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
        })(map = main.map || (main.map = {}));
    })(main = mappino.main || (mappino.main = {}));
})(mappino || (mappino = {}));
/// <reference path='../_references.ts' />
var mappino;
(function (mappino) {
    var main;
    (function (main) {
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
        })(map = main.map || (main.map = {}));
    })(main = mappino.main || (mappino.main = {}));
})(mappino || (mappino = {}));
/// <reference path='../_references.ts' />
var mappino;
(function (mappino) {
    var main;
    (function (main) {
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
        })(map = main.map || (main.map = {}));
    })(main = mappino.main || (mappino.main = {}));
})(mappino || (mappino = {}));
/// <reference path='../_references.ts' />
var mappino;
(function (mappino) {
    var main;
    (function (main) {
        var map;
        (function (map) {
            var Panel = (function () {
                function Panel(el, name, state) {
                    this.el = el;
                    this.name = name;
                    this.state = state;
                    this.config = {
                        openedClass: 'opened',
                        closedClass: 'closed',
                        closingClass: 'closing'
                    };
                    // -
                }
                Object.defineProperty(Panel.prototype, "_name", {
                    get: function () {
                        return this.name;
                    },
                    enumerable: true,
                    configurable: true
                });
                Object.defineProperty(Panel.prototype, "_state", {
                    get: function () {
                        return this.state;
                    },
                    set: function (_state) {
                        this.state = _state;
                        _state === 0 ? this.hide() : this.show();
                    },
                    enumerable: true,
                    configurable: true
                });
                Panel.prototype.show = function () {
                    this.el
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
                    if (this.el.hasClass(this.config['openedClass'])) {
                        this.el
                            .removeClass(this.config['openedClass'])
                            .addClass(this.config['closingClass'])
                            .delay(500)
                            .queue(function () {
                            self.el
                                .removeClass(self.config['closingClass'])
                                .addClass(self.config['closedClass'])
                                .dequeue();
                        });
                    }
                    else {
                        this.el.addClass(this.config['closedClass']);
                    }
                };
                return Panel;
            })();
            map.Panel = Panel;
        })(map = main.map || (main.map = {}));
    })(main = mappino.main || (mappino.main = {}));
})(mappino || (mappino = {}));
/// <reference path='../_references.ts' />
/// <reference path='../_references.ts' />
var mappino;
(function (mappino) {
    var main;
    (function (main) {
        var map;
        (function (map) {
            'use strict';
            var PanelsHandler = (function () {
                function PanelsHandler($rootScope, $state) {
                    var _this = this;
                    this.$rootScope = $rootScope;
                    this.$state = $state;
                    this.panels = [];
                    this.closedStateId = 0;
                    this.panels.push(new map.Panel(angular.element('.filters-panel'), 'filters', 0));
                    this.panels.push(new map.Panel(angular.element('.favorites-panel'), 'favorites', 0));
                    this.$rootScope.$on('$stateChangeSuccess', function () { return _this.synchronize(); });
                }
                PanelsHandler.prototype.synchronize = function () {
                    // Якщо в урлі для панелі фільтрів та оголошення параметри стану !== 0
                    // значить хочуть бути відкрти обидві панелі і у нас конфлікт.
                    // Тоді закриваємо панель фільтрів, віддаючи приоритет панелі з оголошенням
                    if (parseInt(this.$state.params['filters']) !== this.closedStateId &&
                        parseInt(this.$state.params['favorites']) !== this.closedStateId) {
                        // -
                        this.$state.go('base', { favorites: 0 });
                        return;
                    }
                    this.toggleState('filters', parseInt(this.$state.params['filters']));
                    this.toggleState('favorites', parseInt(this.$state.params['favorites']));
                };
                PanelsHandler.prototype.toggleState = function (panel_name, state) {
                    var panels = this.panels;
                    for (var i = 0, len = panels.length; i < len; i++) {
                        if (panel_name === panels[i]._name) {
                            panels[i]._state = state;
                        }
                    }
                };
                PanelsHandler.prototype.isOpened = function (panel_name) {
                    var panels = this.panels;
                    for (var i = 0, len = panels.length; i < len; i++) {
                        if (panel_name === panels[i]._name)
                            return panels[i]._state !== this.closedStateId;
                    }
                };
                PanelsHandler.prototype.open = function (panel_name) {
                    var self = this;
                    switch (panel_name) {
                        case 'filters':
                            self.$state.go('base', { favorites: self.closedStateId, filters: 1 });
                            break;
                        case 'favorites':
                            self.$state.go('base', { filters: self.closedStateId, favorites: 1 });
                            break;
                    }
                };
                PanelsHandler.prototype.close = function (panel_name) {
                    var self = this;
                    switch (panel_name) {
                        case 'filters':
                            self.$state.go('base', { filters: self.closedStateId });
                            break;
                        case 'favorites':
                            self.$state.go('base', { favorites: self.closedStateId });
                            break;
                    }
                };
                PanelsHandler.$inject = [
                    '$rootScope',
                    '$state'
                ];
                return PanelsHandler;
            })();
            map.PanelsHandler = PanelsHandler;
        })(map = main.map || (main.map = {}));
    })(main = mappino.main || (mappino.main = {}));
})(mappino || (mappino = {}));
/**
 * Created by Sergei on 03.05.2015.
 */
/// <reference path='../_references.ts' />
var mappino;
(function (mappino) {
    var main;
    (function (main) {
        var map;
        (function (map) {
            'use strict';
            var AppController = (function () {
                function AppController($scope) {
                    this.$scope = $scope;
                }
                AppController.$inject = [
                    '$scope'
                ];
                return AppController;
            })();
            map.AppController = AppController;
        })(map = main.map || (main.map = {}));
    })(main = mappino.main || (mappino.main = {}));
})(mappino || (mappino = {}));
/// <reference path='../_references.ts' />
var mappino;
(function (mappino) {
    var main;
    (function (main) {
        var map;
        (function (map) {
            'use strict';
            var TabsNavigationController = (function () {
                function TabsNavigationController($scope, $timeout, panelsHandler) {
                    this.$scope = $scope;
                    this.$timeout = $timeout;
                    this.panelsHandler = panelsHandler;
                    var self = this;
                    this.$scope.$on('$stateChangeSuccess', function () {
                        $scope.filtersPanelIsOpened = self.panelsHandler.isOpened('filters');
                        $scope.favoritesPanelIsOpened = self.panelsHandler.isOpened('favorites');
                    });
                    // Materialize: init .tabs()
                    $timeout(function () { return $('.tabs').tabs(); });
                }
                TabsNavigationController.prototype.open = function (panel_name) {
                    this.panelsHandler.open(panel_name);
                };
                TabsNavigationController.$inject = [
                    '$scope',
                    '$timeout',
                    'PanelsHandler'
                ];
                return TabsNavigationController;
            })();
            map.TabsNavigationController = TabsNavigationController;
        })(map = main.map || (main.map = {}));
    })(main = mappino.main || (mappino.main = {}));
})(mappino || (mappino = {}));
/// <reference path='../_references.ts' />
var mappino;
(function (mappino) {
    var main;
    (function (main) {
        var map;
        (function (map) {
            'use strict';
            var MapController = (function () {
                function MapController($scope) {
                    this.$scope = $scope;
                    $scope.$on('$routeChangeSuccess', function (prevent, current) {
                        console.log(current.params);
                        //console.log(this.map);
                    });
                    google.maps.event.addDomListener(window, "load", this.initMap);
                }
                MapController.prototype.initMap = function () {
                    this.map = new google.maps.Map(document.getElementById("map"), {
                        center: new google.maps.LatLng(48.455935, 34.41285),
                        zoom: 6,
                        mapTypeId: google.maps.MapTypeId.ROADMAP,
                        disableDefaultUI: true
                    });
                };
                MapController.$inject = [
                    '$scope'
                ];
                return MapController;
            })();
            map.MapController = MapController;
        })(map = main.map || (main.map = {}));
    })(main = mappino.main || (mappino.main = {}));
})(mappino || (mappino = {}));
/// <reference path='_references.ts' />
var mappino;
(function (mappino) {
    var main;
    (function (main) {
        var map;
        (function (map) {
            'use strict';
            var app = angular.module('mappino.main.map', [
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
            app.service('PanelsHandler', map.PanelsHandler);
            /** Module controllers */
            app.controller('AppController', map.AppController);
            app.controller('TabsNavigationController', map.TabsNavigationController);
            app.controller('MapController', map.MapController);
        })(map = main.map || (main.map = {}));
    })(main = mappino.main || (mappino.main = {}));
})(mappino || (mappino = {}));
/// <reference path='../../_common/definitions/google.maps.d.ts' />
/// <reference path='../../_common/definitions/jquery.d.ts' />
/// <reference path='../../_common/definitions/angular.d.ts' />
/// <reference path='../../_common/definitions/angular-cookies.d.ts' />
/// <reference path='../../_common/definitions/angular-ui-router.d.ts' />
/// <reference path='../../_common/definitions/custom.d.ts' />
/// <reference path='configs/ProvidersConfigs.ts' />
/// <reference path='configs/RoutersConfigs.ts' />
/// <reference path='configs/ApplicationConfigs.ts' />
/// <reference path='models/Panel.ts' />
/// <reference path='interfaces/IPanelsHandler.ts' />
/// <reference path='handlers/PanelsHandler.ts' />
/// <reference path='services/FiltersService.ts' />
/// <reference path='controllers/AppController.ts' />
/// <reference path='controllers/TabsNavigationController.ts' />
/// <reference path='controllers/MapController.ts' />
/// <reference path='App.ts' />
//# sourceMappingURL=map.js.map