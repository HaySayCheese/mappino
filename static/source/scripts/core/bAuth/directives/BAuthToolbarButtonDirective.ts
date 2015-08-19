namespace Mappino.Core.BAuth {

    export function BAuthToolbarButtonDirective(bAuthService: BAuthService): angular.IDirective {

        return {
            restrict: 'E',
            scope: {},
            template: `<div layout="row" layour-align="center center">
                            <b-auth-user-avatar class="-mini -toolbar"></b-auth-user-avatar>

                            <span ng-show="user.account.first_name && user.account.last_name" ng-cloak>[[ user.account.full_name ]]</span>
                            <span ng-hide="user.account.first_name && user.account.last_name">Настройки</span>
                        </div>`,


            link: (scope, element, attrs) => {
                //
            },

            controller: ['$scope', ($scope) => {
                $scope.user = bAuthService.user;
            }]
        };
    }

    BAuthToolbarButtonDirective.$inject = ['BAuthService'];
}