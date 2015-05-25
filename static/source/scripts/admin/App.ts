/// <reference path='_references.ts' />

module pages.admin {
    'use strict';

    var app: angular.IModule = angular.module('mappino.pages.home', [
        'ngCookies'
    ]);



    /** Providers configuration create */
    new ProvidersConfigs(app);

    /** Application configuration create */
    new ApplicationConfigs(app);


    /** Module services */
    app.service('AdminAuthService', AdminAuthService);


    /** Module controllers */
    app.controller('LoginController', LoginController);
    app.controller('AdminController', AdminController);
}