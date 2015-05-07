/// <reference path='_references.ts' />

module pages.map {
    'use strict';

    var app: angular.IModule = angular.module('mappino.pages.map', [
        //'ngRoute',
        'ngCookies',
        //'ngAnimate',
        'ngResource',
        //
        //'ui.mask',
        'ui.router',
        //'lrNotifier',
        //'ab-base64',
    ]);


    /** Providers configuration create */
    new ProvidersConfigs(app);

    /** Routers configuration create */
    new RoutersConfigs(app);

    /** Application configuration create */
    new ApplicationConfigs(app);


    /** Module services */
    app.service('DropPanelsHandler', bModules.Panels.DropPanelsHandler);
    app.service('SlidePanelsHandler', bModules.Panels.SlidingPanelsHandler);

    app.service('RealtyTypesService', bModules.Types.RealtyTypesService);


    app.service('FiltersService', FiltersService);


    /** Module controllers */
    app.controller('AppController', AppController);
    app.controller('TabsNavigationController', TabsNavigationController);
    app.controller('FiltersPanelController', FiltersPanelController);
    app.controller('MapController', MapController);
    app.controller('PlaceAutocompleteController', PlaceAutocompleteController);
}
