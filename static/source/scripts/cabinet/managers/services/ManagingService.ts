/// <reference path='../_all.ts' />


namespace Mappino.Cabinet.Managers {

    import IHttpPromise = angular.IHttpPromise;

    "use strict";

    export class ManagingService {
        private toastOptions = {
            position:   'top right',
            delay:      5000
        };

        private publication: any;

        public static $inject = [
            '$http',
            '$state',
            '$mdToast',
            'TXT'
        ];


        constructor(private $http: ng.IHttpService,
                    private $state: ng.ui.IStateService,
                    private $mdToast: any,
                    private TXT: any) {
            // ---------------------------------------------------------------------------------------------------------

        }


        public loadUsersData(): ng.IHttpPromise<any> {
            var promise: ng.IHttpPromise<any> = this.$http.get(`/ajax/api/managers/users/`);

            promise.success(response => {});

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.MANAGERS.LOAD_USERS.ERROR)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }


        public createUser(userData): ng.IHttpPromise<any> {
            var promise: ng.IHttpPromise<any> = this.$http.post(`/ajax/api/managers/user/add/`, userData);

            promise.success(response => {
                if (response.code == 0) {
                    this.$mdToast.show(
                        this.$mdToast.simple()
                            .content(this.TXT.TOASTS.MANAGERS.CREATE_USER.SUCCESS)
                            .position(this.toastOptions.position)
                            .hideDelay(this.toastOptions.delay)
                    );
                }
            });

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.MANAGERS.CREATE_USER.ERROR)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }

        public getUserData(userHid) {
            var promise: ng.IHttpPromise<any> = this.$http.get(`/ajax/api/managers/user/${userHid}/`);

            promise.success(response => {});

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.MANAGERS.USER_DATA.ERROR)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }

        public updateUserProfileField(userHid: number|string, fieldName: string,
                                      fieldValue: number|string, fieldValuePrefix?: number|string) {
            var promise: IHttpPromise<any> = this.$http.put(`/ajax/api/managers/user/${userHid}/`, {
                [fieldName]: `${fieldValuePrefix ? fieldValuePrefix : ''}${fieldValue}`
            });

            promise.success(response => {
            });

            promise.error(response => { /* error */ });

            return promise;

        }

        public getStatistics() {
            var promise: ng.IHttpPromise<any> = this.$http.get(`/ajax/api/managers/statistics/`);

            promise.success(response => {});

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.MANAGERS.STATISTICS.ERROR)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }
    }
}

