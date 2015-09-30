namespace Mappino.Help {
    'use strict';

    export class ProvidersConfigs {

        constructor(private app: ng.IModule) {
            app.config(['$interpolateProvider', '$locationProvider',
                ($interpolateProvider, $locationProvider) => {
                    $interpolateProvider.startSymbol('[[');
                    $interpolateProvider.endSymbol(']]');
                }
            ]);
        }
    }
}