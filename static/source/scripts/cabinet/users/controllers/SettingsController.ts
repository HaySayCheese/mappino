/// <reference path='../_all.ts' />


namespace Mappino.Cabinet.Users {
    "use strict";

    import ITimeoutService  = angular.ITimeoutService;
    import BAuthService     = Mappino.Core.BAuth.BAuthService;
    import IDialogService   = angular.material.IDialogService;

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
                    private $timeout: ITimeoutService,
                    private $mdDialog: IDialogService,
                    private bAuthService: BAuthService,
                    private TXT: any) {
            // ---------------------------------------------------------------------------------------------------------
            $rootScope.pageTitle = 'Редактирование профиля';

            $scope.profile = bAuthService.user;

            $rootScope.loaders.overlay = true;
            bAuthService.loadProfile()
                .success(response => {
                    this.initInputsChange();
                    $rootScope.loaders.overlay = false;
                })
                .error(response => { /* error */ });

            this.restoreFieldState();
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



        public checkboxOnChange(fieldName: string) {
            var fieldValue = this.$scope.profile[fieldName];
            console.log(fieldValue);

            this.bAuthService.updateProfileField(fieldName, fieldValue);

            this.checkIfAllMeansOfCommunicationDisabled();
        }



        private initInputsChange() {
            angular.element(".settings-page input[type='text'], " +
                ".settings-page input[type='tel'], " +
                ".settings-page input[type='email']").bind("focusout", (e) => {
                // -----------------------------------------------------------------------------------------------------
                var fieldName  = e.currentTarget['name'],
                    fieldValue = e.currentTarget['value'].replace(/\s+/g, " "),
                    fieldValuePrefix = '';

                if (!this.$scope.userProfileForm[fieldName].$dirty || this.$scope.userProfileForm[fieldName].$invalid)
                    return;

                if (fieldName == 'mobile_phone' || fieldName == 'mobile_code') {
                    fieldValuePrefix = this.$scope.profile.mobile_code;
                }

                if (fieldName == 'add_mobile_phone' || fieldName == 'add_mobile_code') {
                    fieldValuePrefix = this.$scope.profile.add_mobile_code;
                }

                this.bAuthService.updateProfileField(fieldName, fieldValue, fieldValuePrefix)
                    .success(response => {
                        if (response.code == 0) {
                            if (response.data && response.data.value) {
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



        private restoreFieldState() {
            angular.element(".settings-page input[type='text'], " +
                ".settings-page input[type='tel'], " +
                ".settings-page input[type='email']").on('input', (e) => {
                var fieldName  = e.currentTarget['name'];

                this.$scope.userProfileForm[fieldName].$setValidity("invalid",    true);
                this.$scope.userProfileForm[fieldName].$setValidity("duplicated", true);
            })
        }


        private checkIfAllMeansOfCommunicationDisabled() {
            if (!this.$scope.profile)
                return;

            if (this.$scope.profile.hide_email && this.$scope.profile.hide_mobile_phone_number &&
                this.$scope.profile.hide_add_mobile_phone_number && this.$scope.profile.hide_landline_phone_number &&
                this.$scope.profile.hide_add_landline_phone_number && this.$scope.profile.hide_skype) {
                // ------------------------------------------------------------------------------------------------------
                var alert = this.$mdDialog.confirm()
                    .parent(angular.element(document.body))
                    .title(this.TXT.DIALOGS.ALL_MEANS_OF_COMMUNICATION_DISABLED.TITLE)
                    .content(this.TXT.DIALOGS.ALL_MEANS_OF_COMMUNICATION_DISABLED.BODY)
                    .ariaLabel(this.TXT.DIALOGS.ALL_MEANS_OF_COMMUNICATION_DISABLED.ARIA_LABEL)
                    .ok(this.TXT.DIALOGS.ALL_MEANS_OF_COMMUNICATION_DISABLED.OK_BTN);

                this.$mdDialog.show(alert);
            }
        }
    }
}