/// <reference path='../_all.ts' />


module Mappino.Cabinet {
    export class SettingsController {
        private profile: Mappino.Core.Auth.IUser;

        public static $inject = [
            '$scope',
            '$rootScope',
            '$timeout',
            '$mdDialog',
            'AuthService',
            'TXT'
        ];

        constructor(private $scope: any,
                    private $rootScope: any,
                    private $timeout: angular.ITimeoutService,
                    private $mdDialog: any,
                    private authService: Mappino.Core.Auth.IAuthService,
                    private TXT: any) {
            // ---------------------------------------------------------------------------------------------------------
            $rootScope.pageTitle = 'Редактирование профиля';

            $scope.profile = this.profile;

            $rootScope.loaders.overlay = true;

            this.initInputsChange();

            authService.loadProfile(response => {
                $scope.profile = response;
                $rootScope.loaders.overlay = false;
            });
        }



        public changeAvatar(avatar) {
            if (!avatar.length) return;

            this.$rootScope.loaders.avatar = true;

            this.authService.uploadAvatar(avatar, response => {
                this.$rootScope.loaders.avatar = false;

                this.$scope.imageFatal      = response.code === 1;
                this.$scope.imageTooLarge   = response.code === 2;
                this.$scope.ImageTooSmall   = response.code === 3;
                this.$scope.ImageUndefined  = response.code === 4;
            });
        }



        public removeAvatar() {
            this.$rootScope.loaders.avatar = true;

            this.authService.removeAvatar(response => {
                this.$rootScope.loaders.avatar = false;
                console.log(this.$scope.profile)
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

                this.authService.checkProfileField({ fieldName: name, fieldValue: value }, response => {
                    e.currentTarget['value'] = response;

                    this.$scope.userProfileForm[name].$setValidity("invalid",    true);
                    this.$scope.userProfileForm[name].$setValidity("duplicated", true);
                }, response => {
                    this.$scope.userProfileForm[name].$setValidity("invalid",       response.code !== 2);
                    this.$scope.userProfileForm[name].$setValidity("duplicated",    response.code !== 3);
                });

            });

            this.$scope.$watchCollection('profile.preferences', (newValue, oldValue) => {
                this.checkIfAllMeansOfCommunicationDisabled();

                if (!angular.isUndefined(newValue) && !angular.isUndefined(oldValue)) {
                    for (var key in newValue) {
                        if (newValue[key] != oldValue[key]) {
                            this.authService.checkProfileField({ fieldName: key, fieldValue: newValue[key] });
                        }
                    }
                }
            });
        }



        private checkIfAllMeansOfCommunicationDisabled() {
            if (!this.$scope.profile) return;

            if (this.$scope.profile.preferences.hide_email && this.$scope.profile.preferences.hide_mobile_phone_number &&
                this.$scope.profile.preferences.hide_add_mobile_phone_number && this.$scope.profile.preferences.hide_landline_phone_number &&
                this.$scope.profile.preferences.hide_add_landline_phone_number && this.$scope.profile.preferences.hide_skype) {
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