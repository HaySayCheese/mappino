/// <reference path='_all.ts' />


module Mappino.Core.Constants {
    var constants: angular.IModule = angular.module('Mappino.Core.Constants', []);

    constants.constant('MAP', {
        'STYLES':  MapStyleConstant.Default,
    });


    constants.run(['$rootScope', 'MAP', ($rootScope, MAP) => {
        $rootScope.MAP = MAP;
    }]);
}