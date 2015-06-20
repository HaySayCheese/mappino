import { RealtyTypesService } from "../_common/bModules/Types/services/realty-types.service.js";

import { AppController } from "./controllers/app.controller.js";
import { MapController } from "./controllers/map.controller.js";
import { FiltersPanelController } from "./controllers/filters-panel.controller.js";
import { PlaceAutocompleteController } from "./controllers/place-autocomplete.controller.js";

import { PanelsHandler } from "./handlers/panels.hendler.js";

import { FiltersService } from "./services/filters.service.js";
import { MarkersService } from "./services/markers.service.js";
import { tabBodyCollapsible, tabBodySectionCollapsible } from "./directives/tabs-panel.directive.js";



var app = angular.module('mappino.pages.map', [
    'ngMaterial',
    'ngCookies',
    'ngResource',
    'ui.router'
]);


app.config(['$stateProvider', '$urlRouterProvider', '$locationProvider', ($stateProvider, $urlRouterProvider, $locationProvider) => {
    $urlRouterProvider.otherwise("/0/0/");

    $stateProvider
        .state('base', {
            url: "/:left_panel_index/:right_panel_index/"
        });

    $locationProvider.hashPrefix('!');
}]);



app.config(['$interpolateProvider', '$resourceProvider', ($interpolateProvider, $resourceProvider) => {
        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');

        $resourceProvider.defaults.stripTrailingSlashes = false;
    }
]);



app.config(['$mdThemingProvider', '$mdIconProvider', ($mdThemingProvider, $mdIconProvider) => {
    $mdThemingProvider.setDefaultTheme('default');

    $mdThemingProvider.theme('default')
        .primaryPalette('blue');
}]);



app.run(['$http', '$cookies', ($http, $cookies) => {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
}]);



/** Handlers */
app.service('PanelsHandler', PanelsHandler);


/** bModule services */
app.service('RealtyTypesService', RealtyTypesService);


/** Services */
app.service('FiltersService', FiltersService);
app.service('MarkersService', MarkersService);



/** Directives */
app.directive('tabBodyCollapsible', tabBodyCollapsible);
app.directive('tabBodySectionCollapsible', tabBodySectionCollapsible);


/** Controllers */
app.controller('AppController', AppController);
app.controller('FiltersPanelController', FiltersPanelController);
app.controller('MapController', MapController);
app.controller('PlaceAutocompleteController', PlaceAutocompleteController);