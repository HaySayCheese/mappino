/// <reference path='../_all.ts' />


namespace Mappino.Map {
    'use strict';

    export class ProvidersConfigs {

        constructor(private app: ng.IModule) {
            app.config(['$interpolateProvider', '$resourceProvider', '$locationProvider',
                ($interpolateProvider, $resourceProvider, $locationProvider) => {
                    $interpolateProvider.startSymbol('[[');
                    $interpolateProvider.endSymbol(']]');

                    $resourceProvider.defaults.stripTrailingSlashes = false;
                }
            ]);
        }
    }
}