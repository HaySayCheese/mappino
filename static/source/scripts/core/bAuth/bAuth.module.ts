/// <reference path='_all.ts' />


module Mappino.Core.BAuth {
    'use strict';

    var auth: angular.IModule = angular.module('Mappino.Core.bAuth', [
        'ngCookies',
        'ngMaterial'
    ]);

    auth.service('AuthService', AuthService);

    auth.directive('bAuthToolbarButton', BAuthToolbarButtonDirective);
    auth.directive('bAuthUserAvatar', BAuthUserAvatarDirective);
}