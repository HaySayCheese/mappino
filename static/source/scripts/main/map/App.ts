/// <reference path='_references.ts' />

module mappino.main.map {
    'use strict';

    var app: angular.IModule = angular.module('mappino.main.map', [
        //'ngRoute',
        'ngCookies',
        //'ngAnimate',
        'ngResource',
        //
        //'ui.mask',
        'ui.router',
        //'lrNotifier',
        //'ab-base64',
        //
        //'underscore',
        //
        //'_modules.bTypes',
        //'_modules.bAuth',
        //'_modules.bDirectives'
    ]);


    /** Providers configuration create */
    new ProvidersConfigs(app);

    /** Routers configuration create */
    new RoutersConfigs(app);

    /** Application configuration create */
    new ApplicationConfigs(app);


    /** Module services */
    app.service('PanelsHandler', PanelsHandler);

    /** Module controllers */
    app.controller('AppController', AppController);
    app.controller('TabsNavigationController', TabsNavigationController);
    app.controller('MapController', MapController);
}
