/// <reference path='_references.ts' />

module pages.cabinet {
    'use strict';

    var app: angular.IModule = angular.module('mappino.pages.cabinet', [
        'ngCookies',
        'ui.router',
        'ui.mask',
        'angularFileUpload',
        'bModules.Types',
        'bModules.Auth'
    ]);



    /** Providers configuration create */
    new ProvidersConfigs(app);

    /** Routers configuration create */
    new RoutersConfigs(app);

    /** Application configuration create */
    new ApplicationConfigs(app);


    /** Module services */
    // -

    app.service('PublicationsService', PublicationsService);


    /** Module controllers */
    app.controller('LoginController', LoginController);
    app.controller('CabinetController', CabinetController);
    app.controller('BriefsController', BriefsController);
    app.controller('PublicationController', PublicationController);
    app.controller('SettingsController', SettingsController);
    app.controller('SupportController', SupportController);
}