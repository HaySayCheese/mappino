namespace Mappino.Core.BAuth {

    import IModule = angular.IModule;

    'use strict';


    var bAuth: IModule = angular.module('Mappino.Core.BAuth', [
        'ngCookies',
        'ngMaterial',
        'ngFileUpload',

        'Mappino.Core.Directives'
    ]);


    bAuth.service('BAuthService', BAuthService);

    bAuth.directive('bAuthToolbarButton', BAuthToolbarButtonDirective);
    bAuth.directive('bAuthUserAvatar', BAuthUserAvatarDirective);


    bAuth.run(['BAuthService', (bAuthService: BAuthService) => {
        bAuthService.tryLogin();
    }]);
}