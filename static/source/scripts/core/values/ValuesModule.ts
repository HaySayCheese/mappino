/// <reference path='_all.ts' />


namespace Mappino.Core.Values {
    var values: ng.IModule = angular.module('Mappino.Core.Values', []);

    values.value('TXT', {
        'DIALOGS':  DialogsValues.Default,
        'TOASTS':   ToastsValues.Default
    });

    values.value('CLAIM', {
        'REASONS':  ClaimReasonsValues.Default,
    });


    values.run(['$rootScope', 'CLAIM', 'TXT', ($rootScope, CLAIM, TXT) => {
        $rootScope.CLAIM    = CLAIM;
        $rootScope.TXT      = TXT;
    }]);
}