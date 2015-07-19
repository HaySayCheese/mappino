/// <reference path='_all.ts' />


module Mappino.Core.Values {
    var constants: angular.IModule = angular.module('Mappino.Core.Values', []);

    constants.value('TXT', {
        'DIALOGS': DialogsValues.Default
    });


    constants.run(['$rootScope', 'TXT', ($rootScope, TXT) => {
        $rootScope.TXT = TXT;
    }]);
}