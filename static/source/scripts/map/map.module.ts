/// <reference path='_all.ts' />

module Mappino.Map {
    'use strict';

    var app: angular.IModule = angular.module('Mappino.Map', [
        'ngAnimate',
        'ngMaterial',
        'ngCookies',
        'ngResource',
        'ngMessages',

        'ngFileUpload',

        'ui.router',

        'Mappino.Core'

        //'ngTinyScrollbar',
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
    app.service('TabsHandler', TabsHandler);
    app.service('PublicationHandler', PublicationHandler);


    /** Directives */
    app.directive('navbarLeft', NavbarLeftDirective);
    app.directive('navbarRight', NavbarRightDirective);
    app.directive('publicationView', PublcationViewDirective);
    app.directive('tabSectionCollapsible', TabBodyCollapsibleDirective);
    //app.directive('tabBodySectionCollapsible', TabBodySectionCollapsibleDirective);




    /** Controllers */
    app.controller('AppController', AppController);

    // left navbar controllers
    app.controller('NavbarLeftController', NavbarLeftController);
    app.controller('FiltersTabController', FiltersTabController);
    // account tab controllers
    app.controller('AccountTabController', AccountTabController);

    // right navbar controllers
    app.controller('NavbarRightController', NavbarRightController);
    app.controller('FavoritesTabController', FavoritesTabController);

    // publication controllers
    app.controller('PublicationController', PublicationController);


    app.controller('MapController', MapController);
    app.controller('PlaceAutocompleteController', PlaceAutocompleteController);
}