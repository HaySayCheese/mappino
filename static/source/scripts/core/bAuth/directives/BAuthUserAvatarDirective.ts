module Mappino.Core.BAuth {

    export function BAuthUserAvatarDirective(authService: AuthService): angular.IDirective {

        var staticUrl = 'http://localhost/mappino_static';

        return {
            restrict: 'E',
            scope: {},
            template: `<div layout="row" layout-align="center center">
                            <img ng-src="[[ user.account.avatar_url ]]" on-error-src="${staticUrl}/build/images/common/no-user.png"
                                ng-show="user.account.avatar_url" />

                            <img src="${staticUrl}/build/images/common/no-user.png" ng-hide="user.account.avatar_url"
                                alt="[[ user.account.full_name ]]" />
                        </div>`,
            

            link: (scope, element, attrs) => {
                //
            },

            controller: ['$scope', ($scope) => {
                $scope.user = authService.user;
            }]
        };
    }

    BAuthUserAvatarDirective.$inject = ['AuthService'];
}