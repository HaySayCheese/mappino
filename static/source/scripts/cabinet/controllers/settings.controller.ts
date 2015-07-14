/// <reference path='../_all.ts' />


module mappino.cabinet {
    export class SettingsController {

        public static $inject = [
            '$scope',
            '$rootScope',
            '$timeout',
            'AuthService'
        ];

        constructor(private $scope: any,
                    private $rootScope: any,
                    private $timeout: angular.ITimeoutService,
                    private authService: mappino.core.auth.IAuthService) {
            // ---------------------------------------------------------------------------------------------------------
            $rootScope.loaders.base = true;

            this.initInputsChange();

            authService.loadProfile((response) => {
                $scope.user = response;
                $rootScope.loaders.base = false;
            });
        }



        public changeAvatar(event) {
            event.preventDefault();

            angular.element('#photo-field').click();
        }



        public removeAvatar() {
            this.$rootScope.loaders.avatar = true;

            this.authService.removeAvatar((response) => {
                //this.$scope.user.account.avatar_url = null;
                this.$rootScope.loaders.avatar = false;

                console.log(this.$scope.user)
            });
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

                    this.$scope.userProfileForm[name].$setValidity("invalid",    true);
                    this.$scope.userProfileForm[name].$setValidity("duplicated", true);
                }, (response) => {
                    this.$scope.userProfileForm[name].$setValidity("invalid",       response.code !== 2);
                    this.$scope.userProfileForm[name].$setValidity("duplicated",    response.code !== 3);
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