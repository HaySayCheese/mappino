/// <reference path='_all.ts' />


namespace Mappino.Core.Constants {
    var constants: angular.IModule = angular.module('Mappino.Core.Constants', []);

    constants.constant('MAP', {
        'STYLES':  MapStylesConstant.Default,
    });

    constants.constant('COUNTRY', {
        'CODES':  CountryCodesConstant.Default,
    });


    constants.run(['$rootScope', 'MAP', 'COUNTRY', ($rootScope, MAP, COUNTRY) => {
        $rootScope.MAP      = MAP;
        $rootScope.COUNTRY  = COUNTRY;
    }]);
}