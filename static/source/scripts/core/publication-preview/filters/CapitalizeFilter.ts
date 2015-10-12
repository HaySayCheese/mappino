namespace Mappino.Core.PublicationPreview {

    import IFilterFunc = angular.IFilterFunc;

    'use strict';

    export function CapitalizeFilter() : IFilterFunc {
        return function (input, all) {

            if (input == undefined) {
                return;
            }
            return input.charAt(0).toUpperCase() + input.substr(1);
        }

    }
}







