/// <reference path='_all.ts' />

module mappino.cabinet {
    'use strict';

    var app: angular.IModule = angular.module('mappino.cabinet', [
        'ngMaterial',
        'ngCookies',
        'ngMessages',
        'ngFileUpload',

        'ui.router',

        'mappino.core',
    ]);



    /** Providers configuration create */
    new ProvidersConfigs(app);

    /** Routers configuration create */
    new RouterConfigs(app);

    /** Material configuration create */
    new MaterialConfigs(app);

    /** Application configuration create */
    new ApplicationConfigs(app);


    app.service('PublicationsService', PublicationsService);
    app.service('TicketsService', TicketsService);


    /** Module controllers */
    app.controller('CabinetController', CabinetController);
    app.controller('BriefsController', BriefsController);
    app.controller('PublicationController', PublicationController);
    app.controller('UnpublishedPublicationController', UnpublishedPublicationController);
    app.controller('SettingsController', SettingsController);
    app.controller('SupportController', SupportController);
    app.controller('TicketController', TicketController);
}