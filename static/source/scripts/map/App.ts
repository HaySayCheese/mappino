/// <reference path='_references.ts' />

module pages.map {
    'use strict';

    var app: angular.IModule = angular.module('mappino.pages.map', [
        'ngMaterial',
        'ngCookies',
        'ngResource',

        'ngTinyScrollbar',

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
    app.service('NavbarsHandler', NavbarsHandler);
    app.service('TabsHandler', TabsHandler);
    app.service('PublicationHandler', PublicationHandler);


    /** Directives */
    app.directive('tabBodyCollapsible', TabBodyCollapsibleDirective);
    app.directive('tabBodySectionCollapsible', TabBodySectionCollapsibleDirective);


    /** Controllers */
    app.controller('AppController', AppController);
    app.controller('NavbarLeftController', NavbarLeftController);
    app.controller('NavbarRightController', NavbarRightController);
    app.controller('PublicationController', PublicationController);
    app.controller('FavoritesController', FavoritesController);
    app.controller('FiltersController', FiltersController);
    app.controller('MapController', MapController);
    app.controller('PlaceAutocompleteController', PlaceAutocompleteController);
}