/// <reference path='../_references.ts' />


module pages.cabinet {
    export class SettingsController {

        public static $inject = [
            '$scope',
            '$timeout',
            'SettingsService'
        ];

        constructor(
            private $scope: any,
            private $timeout: angular.ITimeoutService,
            private settingsService: bModules.Auth.SettingsService) {
            // -
            $timeout(() => $('select').material_select());


            settingsService.load((response) => {
                $scope.user = response;
                $timeout(() => {
                    angular.element('.settings-page input').change()
                });
            });
        }
    }
}