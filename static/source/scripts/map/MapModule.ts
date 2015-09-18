/// <reference path='_all.ts' />

namespace Mappino.Map {
    'use strict';

    var app: angular.IModule = angular.module('mappino.map', [
        'ngAnimate',
        'ngMaterial',
        'ngCookies',
        'ngResource',
        'ngMessages',

        'ui.router',

        'Mappino.Core',

        'ngFileUpload',

        'angular-carousel',
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
    app.service('BriefsService', BriefsService);
    app.service('FavoritesService', FavoritesService);
    app.service('FiltersService', FiltersService);
    app.service('MarkersService', MarkersService);
    app.service('PublicationService', PublicationService);


    /** Handlers */
    app.service('TabsHandler', TabsHandler);
    app.service('PublicationHandler', PublicationHandler);



    /** Directives */
    app.directive('googlePlaceAutocomplete', GooglePlaceAutocompleteDirective);
    app.directive('navbarLeft', NavbarLeftDirective);
    app.directive('navbarRight', NavbarRightDirective);
    app.directive('publicationContacts', PublicationContactsDirective);
    app.directive('publicationView', PublicationViewDirective);
    app.directive('tabSectionCollapsible', TabBodyCollapsibleDirective);
    app.directive('navbarLeftSectionScroll', NavbarLeftSectionScrollDirective);


    /** Controllers */
    app.controller('AppController', AppController);

    // left navbar controllers
    app.controller('NavbarLeftController', NavbarLeftController);
    app.controller('FiltersTabController', FiltersTabController);
    app.controller('AccountTabController', AccountTabController);

    // right navbar controllers
    app.controller('NavbarRightController', NavbarRightController);
    app.controller('FavoritesTabController', FavoritesTabController);
    app.controller('BriefsTabController', BriefsTabController);

    // publication controllers
    app.controller('PublicationController', PublicationController);
    app.controller('PublicationFullSliderController', PublicationFullSliderController);


    app.controller('MapController', MapController);
    app.controller('PlaceAutocompleteController', PlaceAutocompleteController);
}