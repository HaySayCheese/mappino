/// <reference path='_all.ts' />


namespace Mappino.Core {
    var core: angular.IModule = angular.module('Mappino.Core', [
        'Mappino.Core.Values',
        'Mappino.Core.Constants',
        'Mappino.Core.Directives',

        'Mappino.Core.bAuth',
        //'Mappino.Core.RentCalendar'
    ]);
}