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
                    this.initInputsChange();
                    $rootScope.loaders.overlay = false;
                })
                .error(response => { /* error */ });
        }



        public changeAvatar(avatar) {
            if (!avatar.length) return;

            this.$rootScope.loaders.avatar = true;

            this.bAuthService.uploadAvatar(avatar)
                .success(response => {
                    this.$rootScope.loaders.avatar = false;

                    this.$scope.imageFatal      = response.code === 1;
                    this.$scope.imageTooLarge   = response.code === 2;
                    this.$scope.ImageTooSmall   = response.code === 3;
                    this.$scope.ImageUndefined  = response.code === 4;
                })
                .error(response => { /* error */ });
        }



        public removeAvatar() {
            this.$rootScope.loaders.avatar = true;

            this.bAuthService.removeAvatar()
                .success(response => {
                    this.$rootScope.loaders.avatar = false;
                })
                .error(response => { /* error */ })
        }



        private initInputsChange() {
            angular.element(".settings-page input[type='text'], " +
                ".settings-page input[type='tel'], " +
                ".settings-page input[type='email']").bind("focusout", (e) => {
                // -----------------------------------------------------------------------------------------------------
                var fieldName  = e.currentTarget['name'],
                    fieldValue = e.currentTarget['value'].replace(/\s+/g, " ");

                if (!this.$scope.userProfileForm[fieldName].$dirty || this.$scope.userProfileForm[fieldName].$invalid)
                    return;

                if (fieldName == 'mobile_phone' || fieldName == 'mobile_code') {
                    fieldValue = this.$scope.profile.mobile_code + this.$scope.profile.mobile_phone;
                }

                if (fieldName == 'add_mobile_phone' || fieldName == 'add_mobile_code') {
                    fieldValue = this.$scope.profile.add_mobile_code + this.$scope.profile.add_mobile_phone;
                }

                this.bAuthService.updateProfileField(fieldName, fieldValue)
                    .success(response => {
                    if (response.code == 0) {
                        if (response.data.value) {
                            e.currentTarget['value'] = response.data.value;
                        }
                        this.$scope.userProfileForm[fieldName].$setValidity("invalid",    true);
                        this.$scope.userProfileForm[fieldName].$setValidity("duplicated", true);
                    } else {
                        this.$scope.userProfileForm[fieldName].$setValidity("invalid",       response.code !== 2);
                        this.$scope.userProfileForm[fieldName].$setValidity("duplicated",    response.code !== 3);
                    }
                })
                    .error(response => {});
            });
        }
    }
}