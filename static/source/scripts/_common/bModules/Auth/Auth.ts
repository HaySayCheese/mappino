/// <reference path='_references.ts' />


module bModules.Auth {
    'use strict';

    var bAuth: angular.IModule = angular.module('bModules.Auth', ['ngCookies']);

    bAuth.service('AuthService', AuthService);
}