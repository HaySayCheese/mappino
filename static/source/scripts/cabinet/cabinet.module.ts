/// <reference path='_all.ts' />

module Mappino.Cabinet {
    'use strict';

    var app: angular.IModule = angular.module('Mappino.Cabinet', [
        'ngMaterial',
        'ngCookies',
        'ngMessages',
        'ngFileUpload',

        'ui.router',

        'Mappino.Core',
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


    app.directive('publicationControls', publicationControls);


    /** Module controllers */
    app.controller('CabinetController', CabinetController);
    app.controller('BriefsController', BriefsController);
    app.controller('PublicationController', PublicationController);
    app.controller('SettingsController', SettingsController);
    app.controller('SupportController', SupportController);
    app.controller('TicketController', TicketController);
}