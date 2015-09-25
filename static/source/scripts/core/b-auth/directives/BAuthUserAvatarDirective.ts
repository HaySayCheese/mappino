namespace Mappino.Core.BAuth {
    'use strict';

    import IDirective = angular.IDirective;


    export function BAuthUserAvatarDirective(bAuthService: BAuthService): IDirective {
        return {
            restrict: 'E',
            scope: {},
            template: `<div layout="row" layout-align="center center">
                            <img ng-src="[[ user.avatar_url ]]" on-error-src="${EMPTY_OR_ERROR_USER_AVATAR_URL}"
                                ng-show="user.avatar_url" alt="[[ user.full_name ]]" />

                            <img src="${EMPTY_OR_ERROR_USER_AVATAR_URL}" ng-hide="user.avatar_url" alt="[[ user.full_name ]]" />
                        </div>`,
            

            link: (scope, element, attrs) => {
                var $element = angular.element(element);

                $element.addClass('b-auth-user-avatar');
            },

            controller: ['$scope', ($scope) => {
                $scope.user = bAuthService.user;
            }]
        };
    }

    BAuthUserAvatarDirective.$inject = ['BAuthService'];
}