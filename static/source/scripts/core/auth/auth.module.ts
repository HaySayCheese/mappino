/// <reference path='_all.ts' />


module mappino.core.auth {
    'use strict';

    var auth: angular.IModule = angular.module('mappino.core.auth', [
        'ngCookies'
    ]);

    auth.service('AuthService', AuthService);
}