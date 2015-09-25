namespace Mappino.Core.BAuth {
    'use strict';

    import IDirective = angular.IDirective;

    export function BAuthToolbarButtonDirective(bAuthService: BAuthService): IDirective {

        return {
            restrict: 'E',
            scope: {},
            template: `<div layout="row" layour-align="center center">
                            <b-auth-user-avatar class="b-auth-user-avatar--toolbar"></b-auth-user-avatar>

                            <span ng-show="user.full_name" ng-cloak>[[ user.full_name ]]</span>
                            <span ng-hide="user.full_name">Настройки</span>
                        </div>`,


            link: (scope, element, attrs) => {  },

            controller: ['$scope', ($scope) => {
                $scope.user = bAuthService.user;
            }]
        };
    }

    BAuthToolbarButtonDirective.$inject = ['BAuthService'];
}