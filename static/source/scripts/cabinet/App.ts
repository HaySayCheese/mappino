/// <reference path='_references.ts' />

module pages.cabinet {
    'use strict';

    var app: angular.IModule = angular.module('mappino.pages.cabinet', [
        'ngCookies',
        'ui.router'
    ]);



    /** Providers configuration create */
    new ProvidersConfigs(app);

    /** Routers configuration create */
    new RoutersConfigs(app);

    /** Application configuration create */
    new ApplicationConfigs(app);


    /** Module services */
    app.service('RealtyTypesService', bModules.Types.RealtyTypesService);

    app.service('AdminAuthService', AdminAuthService);


    /** Module controllers */
    app.controller('LoginController', LoginController);
    app.controller('CabinetController', CabinetController);
    app.controller('BriefsController', BriefsController);
}