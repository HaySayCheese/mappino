/// <reference path='../_all.ts' />


namespace Mappino.Cabinet.Moderators {
    export class SettingsController {
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
                    private $timeout: ng.ITimeoutService,
                    private $mdDialog: any,
                    private bAuthService: Mappino.Core.BAuth.BAuthService,
                    private TXT: any) {
            // ---------------------------------------------------------------------------------------------------------
            $rootScope.pageTitle = 'Редактирование профиля';

            $scope.profile = {
                account: null,
                preferences: null
            };

            $rootScope.loaders.overlay = true;
            bAuthService.loadProfile()
                .success(response => {
                    $scope.profile.account      = response.data.account;
                    $scope.profile.preferences  = response.data.preferences;

                    this.initInputsChange();

                    $rootScope.loaders.overlay = false;
                })
                .error(response => {

                });
        }



        public changeAvatar(avatar) {
            if (!avatar.length) return;

            this.$rootScope.loaders.avatar = true;

            this.bAuthService.uploadAvatar(avatar)
                .success(response => {
                    this.$rootScope.loaders.avatar = false;
                    this.$scope.profile.account.avatar_url = this.bAuthService.user.account.avatar_url;

                    this.$scope.imageFatal      = response.code === 1;
                    this.$scope.imageTooLarge   = response.code === 2;
                    this.$scope.ImageTooSmall   = response.code === 3;
                    this.$scope.ImageUndefined  = response.code === 4;
                })
                .error(response => {

                });
        }



        public removeAvatar() {
            this.$rootScope.loaders.avatar = true;

            this.bAuthService.removeAvatar()
                .success(response => {
                    this.$rootScope.loaders.avatar = false;
                    this.$scope.profile.account.avatar_url = null;
                })
                .error(response => {

                })
        }



        private initInputsChange() {
            angular.element(".settings-page input[type='text'], " +
                ".settings-page input[type='tel'], " +
                ".settings-page input[type='email']").bind("focusout", (e) => {
                // -----------------------------------------------------------------------------------------------------
                var name  = e.currentTarget['name'],
                    value = e.currentTarget['value'].replace(/\s+/g, " ");

                if (!this.$scope.userProfileForm[name].$dirty)
                    return;

                if (name == 'mobile_phone' || name == 'mobile_code') {
                    value = this.$scope.profile.account.mobile_code + this.$scope.profile.account.mobile_phone;
                }

                if (name == 'add_mobile_phone' || name == 'add_mobile_code') {
                    value = this.$scope.profile.account.add_mobile_code + this.$scope.profile.account.add_mobile_phone;
                }

                this.bAuthService.updateProfileField({ [name]: value })
                    .success(response => {
                        if (response.code == 0) {
                            if (response.data.value) {
                                e.currentTarget['value'] = response.data.value;
                            }
                            this.$scope.userProfileForm[name].$setValidity("invalid",    true);
                            this.$scope.userProfileForm[name].$setValidity("duplicated", true);
                        } else {
                            this.$scope.userProfileForm[name].$setValidity("invalid",       response.code !== 2);
                            this.$scope.userProfileForm[name].$setValidity("duplicated",    response.code !== 3);
                        }
                    })
                    .error(response => {});
            });
        }
    }
}