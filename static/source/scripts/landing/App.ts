/// <reference path='_references.ts' />

namespace pages.home {
    'use strict';

    var app: angular.IModule = angular.namespace('mappino.pages.home', [
        'ngCookies'
    ]);



    /** Providers configuration create */
    new ProvidersConfigs(app);

    /** Application configuration create */
    new ApplicationConfigs(app);


    /** Module services */
    app.service('RealtyTypesService', bModules.Types.RealtyTypesService);


    /** Module controllers */
    app.controller('HomeController', HomeController);
}