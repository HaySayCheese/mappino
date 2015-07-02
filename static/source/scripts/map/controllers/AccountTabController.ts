/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class AccountTabController {
        public static $inject = [
            '$scope',
            'AuthService'
        ];

        constructor(private $scope,
                    private authService: bModules.Auth.IAuthService) {
            // ---------------------------------------------------------------------------------------------------------
            $scope.accountState = 'accountInformation';

            authService.tryLogin();
        }



        public changeState(stateName: string) {
            this.$scope.accountState = stateName;
        }
    }
}