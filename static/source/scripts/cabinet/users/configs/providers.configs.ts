/// <reference path='../_all.ts' />


namespace Mappino.Cabinet.Users {
    'use strict';

    export class ProvidersConfigs {

        constructor(private app: angular.IModule) {
            app.config(['$interpolateProvider', '$locationProvider', ($interpolateProvider, $locationProvider) => {
                $interpolateProvider.startSymbol('[[');
                $interpolateProvider.endSymbol(']]');
            }]);
        }
    }
}