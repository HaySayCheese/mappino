/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class AppController {
        private realtyTypes = [];

        public static $inject = [
            '$scope',
            'PanelsHandler',
            'RealtyTypesService'
        ];

        constructor(private $scope,
                    private panelsHandler,
                    private realtyTypesService) {
            // ---------------------------------------------------------------------------------------------------------
            this.realtyTypes = realtyTypesService.realtyTypes;

            panelsHandler.initialize();
        }
    }
}