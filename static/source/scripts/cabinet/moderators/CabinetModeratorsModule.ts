namespace Mappino.Cabinet.Moderators {
    'use strict';

    var app: ng.IModule = angular.module('mappino.cabinet.moderators', [
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


    app.service('ModeratingService', ModeratingService);


    /** Module controllers */
    app.controller('CabinetController', CabinetController);
    app.controller('HeldController', HeldController);
    app.controller('SettingsController', SettingsController);
    app.controller('ModeratingController', ModeratingController);
}