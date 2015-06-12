/// <reference path='_references.ts' />

module pages.cabinet {
    'use strict';

    var app: angular.IModule = angular.module('mappino.pages.cabinet', [
        'ngMaterial',
        'ngCookies',
        'ngMessages',
        'ui.router',
        'ngFileUpload',

        'bModules.Types',
        'bModules.Auth',
        'bModules.Directives'
    ]);



    /** Providers configuration create */
    new ProvidersConfigs(app);

    /** Routers configuration create */
    new RoutersConfigs(app);

    /** Material configuration create */
    new MaterialFrameworkConfigs(app);

    /** Application configuration create */
    new ApplicationConfigs(app);


    /** Module services */
    // -

    app.service('PublicationsService', PublicationsService);
    app.service('TicketsService', TicketsService);


    /** Module controllers */
    app.controller('LoginController', LoginController);
    app.controller('CabinetController', CabinetController);
    app.controller('BriefsController', BriefsController);
    app.controller('PublicationController', PublicationController);
    app.controller('SettingsController', SettingsController);
    app.controller('SupportController', SupportController);
    app.controller('TicketController', TicketController);
}