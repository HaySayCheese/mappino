namespace Mappino.Cabinet.Users {
    import IModule = angular.IModule;

    'use strict';

    var app: IModule = angular.module('mappino.cabinet.users', [
        'ngAnimate',
        'ngMaterial',
        'ngCookies',
        'ngResource',
        'ngMessages',
        'ngSanitize',
        'ngFileUpload',

        'ui.router',

        'angular-carousel',


        'Mappino.Core.Values',
        'Mappino.Core.Constants',
        'Mappino.Core.Directives',

        'Mappino.Core.BAuth',
        'Mappino.Core.RentCalendar',
        'Mappino.Core.PublicationPreview',
        'Mappino.Core.RentCalendar'
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
    app.controller('PublishedPublicationController', PublishedPublicationController);
    app.controller('UnpublishedPublicationController', UnpublishedPublicationController);
    app.controller('SettingsController', SettingsController);
    app.controller('SupportController', SupportController);
    app.controller('TicketController', TicketController);
}