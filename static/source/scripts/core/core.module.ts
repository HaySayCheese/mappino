/// <reference path='_all.ts' />


module mappino.core {
    var core: angular.IModule = angular.module('mappino.core', [
        'mappino.core.constants',
        'mappino.core.directives',

        'mappino.core.auth'
    ]);
}