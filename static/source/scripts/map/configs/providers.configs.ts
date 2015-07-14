/// <reference path='../_all.ts' />


module mappino.map {
    'use strict';

    export class ProvidersConfigs {

        constructor(private app: angular.IModule) {
            app.config(['$interpolateProvider', '$resourceProvider', '$locationProvider',
                function($interpolateProvider, $resourceProvider, $locationProvider) {
                    $interpolateProvider.startSymbol('[[');
                    $interpolateProvider.endSymbol(']]');

                    $resourceProvider.defaults.stripTrailingSlashes = false;
                }
            ]);
        }
    }
}