/// <reference path='_references.ts' />

module pages.map {
    'use strict';

    var app: angular.IModule = angular.module('mappino.pages.map', [
        'ngMaterial',
        'ngCookies',
        'ngResource',
        'ui.router',

        //'bModules.bSidebarPanel'
    ]);




    /** Providers configuration create */
    new ProvidersConfigs(app);

    /** Routers configuration create */
    new RoutersConfigs(app);

    /** Material configuration create */
    new MaterialFrameworkConfigs(app);

    /** Application configuration create */
    new ApplicationConfigs(app);


    /** Handlers */
    app.service('PanelsHandler', PanelsHandler);


    /** bModule services */
    //app.service('DropPanelsHandler', bModules.Panels.DropPanelsHandler);
    //app.service('SlidePanelsHandler', bModules.Panels.SlidingPanelsHandler);
    app.service('RealtyTypesService', bModules.Types.RealtyTypesService);


    /** Services */
    app.service('FiltersService', FiltersService);
    app.service('MarkersService', MarkersService);



    /** Directives */
    app.directive('tabBodyCollapsible', tabBodyCollapsible);
    app.directive('tabBodySectionCollapsible', tabBodySectionCollapsible);


    /** Controllers */
    app.controller('AppController', AppController);
    app.controller('BNavbarController', BNavbarController);
    app.controller('FiltersPanelController', FiltersPanelController);
    app.controller('MapController', MapController);
    app.controller('PlaceAutocompleteController', PlaceAutocompleteController);
}
