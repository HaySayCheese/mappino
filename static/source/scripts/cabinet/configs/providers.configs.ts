/// <reference path='../_all.ts' />


module mappino.cabinet {
    'use strict';

    export class ProvidersConfigs {

        constructor(private app: angular.IModule) {
            app.config(['$interpolateProvider', '$locationProvider',
                function($interpolateProvider, $locationProvider) {
                    $interpolateProvider.startSymbol('[[');
                    $interpolateProvider.endSymbol(']]');
                }
            ]);
        }
    }
}