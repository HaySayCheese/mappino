namespace Mappino.Cabinet.Managers {
    'use strict';

    var app: ng.IModule = angular.module('mappino.cabinet.managers', [
        'ngMaterial',
        'ngCookies',
        'ngMessages',
        'ngFileUpload',

        'ui.router',

        'angular-carousel',


        'Mappino.Core.Values',
        'Mappino.Core.Constants',
        'Mappino.Core.Directives',

        'Mappino.Core.BAuth',
        'Mappino.Core.PublicationPreview'
    ]);




    /** Providers configuration create */
    new ProvidersConfigs(app);

    /** Routers configuration create */
    new RouterConfigs(app);

    /** Material configuration create */
    new MaterialConfigs(app);

    /** Application configuration create */
    new ApplicationConfigs(app);

    app.service('ManagingService', ManagingService);
    app.service('PublicationsService', PublicationsService);

    app.directive('publicationControls', publicationControls);


    /** Module controllers */
    app.controller('BriefsController', BriefsController);
    app.controller('CabinetController', CabinetController);
    app.controller('SettingsController', SettingsController);
    app.controller('ManagingController', ManagingController);
    app.controller('PublicationController', PublicationController);
    app.controller('StatisticsController', StatisticsController);
}