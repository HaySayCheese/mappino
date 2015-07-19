/// <reference path='_all.ts' />


module Mappino.Core {
    var core: angular.IModule = angular.module('Mappino.Core', [
        'Mappino.Core.Values',
        'Mappino.Core.Directives',

        'Mappino.Core.Auth'
    ]);
}