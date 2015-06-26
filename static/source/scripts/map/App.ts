/// <reference path='_references.ts' />

module pages.map {
    'use strict';

    var app: angular.IModule = angular.module('mappino.pages.map', [
        'ngMaterial',
        'ngCookies',
        'ngResource',
        'ui.router',

        'bModules.Types'
    ]);





    /** Providers configuration create */
    new ProvidersConfigs(app);

    /** Routers configuration create */
    new RoutersConfigs(app);

    /** Material configuration create */
    new MaterialFrameworkConfigs(app);

    /** Application configuration create */
    new ApplicationConfigs(app);


    /** Services */
    app.service('FiltersService', FiltersService);
    app.service('MarkersService', MarkersService);


    /** Handlers */
    app.service('PanelsHandler', PanelsHandler);


    /** Directives */
    app.directive('tabBodyCollapsible', TabBodyCollapsibleDirective);
    app.directive('tabBodySectionCollapsible', TabBodySectionCollapsibleDirective);


    /** Controllers */
    app.controller('AppController', AppController);
    app.controller('FiltersPanelController', FiltersPanelController);
    app.controller('MapController', MapController);
    app.controller('PlaceAutocompleteController', PlaceAutocompleteController);
}