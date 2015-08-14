/// <reference path='../_all.ts' />


namespace Mappino.Cabinet.Moderators {
    export class SettingsController {
        private profile: Mappino.Core.BAuth.IUser;

        public static $inject = [
            '$scope',
            '$rootScope',
            '$timeout',
            '$mdDialog',
            'BAuthService',
            'TXT'
        ];

        constructor(private $scope: any,
                    private $rootScope: any,
                    private $timeout: angular.ITimeoutService,
                    private $mdDialog: any,
                    private bAuthService: Mappino.Core.BAuth.IBAuthService,
                    private TXT: any) {
            // ---------------------------------------------------------------------------------------------------------
            $rootScope.pageTitle = 'Редактирование профиля';

            $scope.profile = this.profile;

            $rootScope.loaders.overlay = true;

            this.initInputsChange();

            bAuthService.loadProfile(response => {
                $scope.profile = response;
                console.log($scope.profile)
                $rootScope.loaders.overlay = false;
            });
        }



        public changeAvatar(avatar) {
            if (!avatar.length) return;

            this.$rootScope.loaders.avatar = true;

            this.bAuthService.uploadAvatar(avatar, response => {
                this.$rootScope.loaders.avatar = false;
                this.$scope.profile.account.avatar_url = this.bAuthService.user.account.avatar_url;

                this.$scope.imageFatal      = response.code === 1;
                this.$scope.imageTooLarge   = response.code === 2;
                this.$scope.ImageTooSmall   = response.code === 3;
                this.$scope.ImageUndefined  = response.code === 4;
            }, response => {
                this.$rootScope.loaders.avatar = false;
            });
        }



        public removeAvatar() {
            this.$rootScope.loaders.avatar = true;

            this.bAuthService.removeAvatar(response => {
                this.$rootScope.loaders.avatar = false;
                this.$scope.profile.account.avatar_url = null;
            });
        }



        private initInputsChange() {
            angular.element(".settings-page input[type='text'], " +
                            ".settings-page input[type='tel'], " +
                            ".settings-page input[type='email']").bind("focusout", (e) => {
                // -----------------------------------------------------------------------------------------------------
                var name  = e.currentTarget['name'],
                    value = e.currentTarget['value'].replace(/\s+/g, " ");

                if (!this.$scope.userProfileForm[name].$dirty) return;

                this.bAuthService.checkProfileField({ fieldName: name, fieldValue: value }, response => {
                    e.currentTarget['value'] = response;

                    this.$scope.userProfileForm[name].$setValidity("invalid",    true);
                    this.$scope.userProfileForm[name].$setValidity("duplicated", true);
                }, response => {
                    this.$scope.userProfileForm[name].$setValidity("invalid",       response.code !== 2);
                    this.$scope.userProfileForm[name].$setValidity("duplicated",    response.code !== 3);
                });
            });

            this.$scope.$watchCollection('profile.preferences', (newValue, oldValue) => {
                if (!angular.isUndefined(newValue) && !angular.isUndefined(oldValue)) {
                    for (var key in newValue) {
                        if (newValue[key] != oldValue[key]) {
                            this.bAuthService.checkProfileField({ fieldName: key, fieldValue: newValue[key] });
                        }
                    }
                }
            });
        }
    }
}