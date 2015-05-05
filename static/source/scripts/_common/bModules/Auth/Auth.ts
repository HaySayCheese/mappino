/// <reference path='_references.ts' />


module binno.auth {
    'use strict';

    var bAuth: angular.IModule = angular.module('binno.auth', ['ngCookies']);

    bAuth.factory('AuthService', AuthService);
}
