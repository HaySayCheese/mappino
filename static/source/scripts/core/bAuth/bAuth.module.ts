/// <reference path='_all.ts' />


namespace Mappino.Core.BAuth {
    'use strict';

    var auth: angular.IModule = angular.module('Mappino.Core.bAuth', [
        'ngCookies',
        'ngMaterial'
    ]);

    auth.service('BAuthService', BAuthService);

    auth.directive('bAuthToolbarButton', BAuthToolbarButtonDirective);
    auth.directive('bAuthUserAvatar', BAuthUserAvatarDirective);
}