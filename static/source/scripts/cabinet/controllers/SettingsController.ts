/// <reference path='../_references.ts' />


module pages.cabinet {
    export class SettingsController {

        public static $inject = [
            '$scope',
            '$rootScope',
            '$timeout',
            'AuthService'
        ];

        constructor(
            private $scope: any,
            private $rootScope: any,
            private $timeout: angular.ITimeoutService,
            private authService: bModules.Auth.AuthService) {
            // ---------------------------------------------------------------------------------------------------------
            $rootScope.loaders.base = true;

            this.initInputsChange();

            authService.loadProfile((response) => {
                $scope.user = response;
                $rootScope.loaders.base = false;
            });
        }



        // used in scope, don't remove
        private changePhoto(event) {
            event.preventDefault();

            angular.element('#photo-field').click();
        }



        private initInputsChange() {
            angular.element(".settings-page input[type='file']").bind('change', (event) => {
                this.$rootScope.loaders.avatar = true;

                this.authService.uploadAvatar(event.target['files'][0], (response) => {
                    this.$rootScope.loaders.avatar = false;

                    this.$scope.imageFatal      = response.code === 1;
                    this.$scope.imageTooLarge   = response.code === 2;
                    this.$scope.ImageTooSmall   = response.code === 3;
                    this.$scope.ImageUndefined  = response.code === 4;
                });
            });

            angular.element(".settings-page input[type='text'], " +
                            ".settings-page input[type='tel'], " +
                            ".settings-page input[type='email']").bind("focusout", (e) => {
                // -----------------------------------------------------------------------------------------------------
                var name  = e.currentTarget['name'],
                    value = e.currentTarget['value'].replace(/\s+/g, " ");

                if (!this.$scope.userProfileForm[name].$dirty) {
                    return;
                }

                if (name === "mobile_phone" && (value === "+38 (0__) __ - __ - ___" || value[22] === "_")) {
                    return;
                }

                this.authService.checkProfileField({ f: name, v: value }, (newValue) => {
                    e.currentTarget['value'] = newValue;
                }, (response) => {
                    this.$scope.userProfileForm[name].$setValidity("incorrect",   response.code !== 10);
                    this.$scope.userProfileForm[name].$setValidity("inUsed",      response.code !== 11);
                });

            });

            this.$scope.$watchCollection('user.preferences', (newValue, oldValue) => {
                if (!_.isUndefined(newValue) && !_.isUndefined(oldValue)) {
                    for (var key in newValue) {
                        if (newValue[key] != oldValue[key]) {
                            this.authService.checkProfileField({ f: key, v: newValue[key] });
                        }
                    }
                }
            });
        }
    }
}