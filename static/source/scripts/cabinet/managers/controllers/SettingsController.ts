/// <reference path='../_all.ts' />


namespace Mappino.Cabinet.Managers {
    export class SettingsController {
        public static $inject = [
            '$scope',
            '$rootScope',
            '$timeout',
            '$mdDialog',
            'BAuthService',
            'TXT',
            '$state',
            'ManagingService'
        ];

        public userHid : any;

        constructor(private $scope: any,
                    private $rootScope: any,
                    private $timeout: ng.ITimeoutService,
                    private $mdDialog: any,
                    private bAuthService: Mappino.Core.BAuth.BAuthService,
                    private TXT: any,
                    private $state: ng.ui.IStateService,
                    private managingService: ManagingService) {
            // ---------------------------------------------------------------------------------------------------------
            $rootScope.pageTitle = 'Редактирование профиля';

            this.userHid = this.$state.params['user_hid'];

            $rootScope.loaders.overlay = true;
            this.loadUserData();
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


        private loadUserData() {
            if (this.$state.includes('settings')) {
                this.$scope.managerUser = true;
                this.$scope.profile = this.bAuthService.user;
                this.bAuthService.loadProfile()
                    .success(response => {
                        this.initInputsChange();
                        this.$rootScope.loaders.overlay = false;
                    })
                    .error(response => {
                    });
            }
            else {
                this.$scope.managerUser = false;
                this.managingService.getUserData(this.userHid)
                    .success(response => {
                        this.$scope.profile = response.data;
                        this.initInputsChange();
                    })
                    .error(response => {});
                this.$rootScope.loaders.overlay = false;
            }
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
                if (this.$state.includes('settings')) {
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
                } else {
                    this.managingService.updateUserProfileField(this.userHid, fieldName, fieldValue, fieldValuePrefix)
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
                }

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
    }
}