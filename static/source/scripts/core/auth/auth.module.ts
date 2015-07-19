/// <reference path='_all.ts' />


module Mappino.Core.Auth {
    'use strict';

    var auth: angular.IModule = angular.module('Mappino.Core.Auth', [
        'ngCookies'
    ]);

    auth.service('AuthService', AuthService);
}