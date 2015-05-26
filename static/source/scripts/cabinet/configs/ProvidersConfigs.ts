/// <reference path='../_references.ts' />


module pages.cabinet {
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