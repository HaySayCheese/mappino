module Mappino.Core.BAuth {

    export function BAuthToolbarButtonDirective(authService: AuthService): angular.IDirective {

        return {
            restrict: 'E',
            scope: {},
            template: `<div layout="row" layour-align="center center">
                            <b-auth-user-avatar class="-mini -toolbar"></b-auth-user-avatar>

                            <span ng-show="user.account.full_name" ng-cloak>[[ user.account.full_name ]]</span>
                            <span ng-hide="user.account.full_name">Настройки</span>
                        </div>`,


            link: (scope, element, attrs) => {
                //
            },

            controller: ['$scope', ($scope) => {
                $scope.user = authService.user;
            }]
        };
    }

    BAuthToolbarButtonDirective.$inject = ['AuthService'];
}