/// <reference path='../_all.ts' />


module Mappino.Map {
    'use strict';

    export class AppController {
        public static $inject = [
            '$scope',
            '$rootScope'
        ];

        constructor(private $scope,
                    private $rootScope) {
            // ---------------------------------------------------------------------------------------------------------
            $rootScope.loaders = {
                publication: false
            };
        }
    }
}