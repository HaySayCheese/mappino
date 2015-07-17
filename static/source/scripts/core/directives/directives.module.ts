/// <reference path='_all.ts' />


module mappino.core.directives {
    var core: angular.IModule = angular.module('mappino.core.directives', []);

    core.directive('includeReplace', includeReplace);
    core.directive('onlyNumber', onlyNumber);
    core.directive('onlyNumberWithDots', onlyNumberWithDots);
    core.directive('onErrorSrc', onErrorSrc);
}