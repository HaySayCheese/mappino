namespace Mappino.Help {

    'use strict';

    var app: ng.IModule = angular.module('mappino.help', [
        'ngMaterial'
    ]);



    /** Providers configuration create */
    new ProvidersConfigs(app);

    /** Application configuration create */
    new ApplicationConfigs(app);

    /** Material configuration create */
    new MaterialFrameworkConfigs(app);



    /** Module directives */


    /** Module controllers */
    app.controller('HelpController', HelpController);
}