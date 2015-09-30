namespace Mappino.Core.Directives {

    import IModule = angular.IModule;

    "use strict";


    var core: IModule = angular.module('Mappino.Core.Directives', []);

    core.directive('includeReplace', includeReplace);
    core.directive('mappinoLogo', mappinoLogoDirective);
    core.directive('onlyNumber', onlyNumber);
    core.directive('onlyNumberWithDots', onlyNumberWithDots);
    core.directive('onErrorSrc', onErrorSrc);
}