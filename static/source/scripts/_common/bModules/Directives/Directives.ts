/// <reference path='_references.ts' />


module bModules.Directives {
    'use strict';

    var bDirectives: angular.IModule = angular.module('bModules.Directives', []);

    bDirectives.directive('onlyNumber', OnlyNumber);
}
