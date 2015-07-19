/// <reference path='_all.ts' />


module Mappino.Core.Directives {
    var core: angular.IModule = angular.module('Mappino.Core.Directives', []);

    core.directive('includeReplace', includeReplace);
    core.directive('onlyNumber', onlyNumber);
    core.directive('onlyNumberWithDots', onlyNumberWithDots);
    core.directive('onErrorSrc', onErrorSrc);
}