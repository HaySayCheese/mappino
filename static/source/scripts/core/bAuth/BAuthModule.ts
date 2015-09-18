/// <reference path='_all.ts' />


namespace Mappino.Core.BAuth {
    'use strict';

    var bAuth: angular.IModule = angular.module('Mappino.Core.bAuth', [
        'ngCookies',
        'ngMaterial',
        'ngFileUpload'
    ]);

    bAuth.service('BAuthService', BAuthService);

    bAuth.directive('bAuthToolbarButton', BAuthToolbarButtonDirective);
    bAuth.directive('bAuthUserAvatar', BAuthUserAvatarDirective);


    bAuth.run(['BAuthService', (bAuthService: BAuthService) => {
        bAuthService.tryLogin();
    }]);
}