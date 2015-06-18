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


    /** Module services */
    app.service('DropPanelsHandler', bModules.Panels.DropPanelsHandler);
    app.service('SlidePanelsHandler', bModules.Panels.SlidingPanelsHandler);

    app.service('RealtyTypesService', bModules.Types.RealtyTypesService);


    app.service('FiltersService', FiltersService);
    app.service('MarkersService', MarkersService);


    /** Module controllers */
    app.controller('AppController', AppController);
    app.controller('TabsNavigationController', TabsNavigationController);
    app.controller('FiltersPanelController', FiltersPanelController);
    app.controller('MapController', MapController);
    app.controller('PlaceAutocompleteController', PlaceAutocompleteController);
}
