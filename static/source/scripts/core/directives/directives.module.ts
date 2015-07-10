/// <reference path='_all.ts' />


module mappino.core.directives {
    var core: angular.IModule = angular.module('mappino.core.directives', []);

    core.directive('onlyNumber', onlyNumber);
}