namespace Mappino.Landing {
    'use strict';

    var app: ng.IModule = angular.module('mappino.landing', [
        'ngMaterial'
    ]);



    /** Providers configuration create */
    new ProvidersConfigs(app);

    /** Application configuration create */
    new ApplicationConfigs(app);

    /** Material configuration create */
    new MaterialFrameworkConfigs(app);


    /** Module services */
    //app.service('RealtyTypesService', bModules.Types.RealtyTypesService);


    /** Module directives */
    app.directive('headerMedia', HeaderMediaDirective);


    /** Module controllers */
    app.controller('LandingController', LandingController);
}