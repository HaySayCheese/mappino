/// <reference path='../_references.ts' />


module pages.cabinet {
    export class BriefsController {

        public static $inject = [
            '$scope',
            '$timeout',
            'RealtyTypesService'
        ];

        constructor(
            private $scope: any,
            private $timeout: angular.ITimeoutService,
            private realtyTypesService: bModules.Types.RealtyTypesService) {
            // -
            $scope.realtyTypes = realtyTypesService.realty_types;
            $timeout(() => $('select').material_select());
        }

    }
}