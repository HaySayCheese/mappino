namespace Mappino.Landing {
    'use strict';

    var app: ng.IModule = angular.module('mappino.landing', [
        'ngMaterial',

        'Mappino.Core.Constants',
        'Mappino.Core.Directives'
    ]);



    /** Providers configuration create */
    new ProvidersConfigs(app);

    /** Material configuration create */
    new MaterialFrameworkConfigs(app);

    /** Application configuration create */
    new ApplicationConfigs(app);


    /** Module directives */
    app.directive('headerMedia', HeaderMediaDirective);


    /** Module controllers */
    app.controller('LandingController', LandingController);
}