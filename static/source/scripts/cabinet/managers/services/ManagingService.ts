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


        public loadUserBriefs(userHid): ng.IHttpPromise<any> {
            var promise: ng.IHttpPromise<any> = this.$http.get(`/ajax/api/managers/users/${userHid}/publications/`);

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

        public createPublication(userHid: string|number, publication: IPublicationNew): IHttpPromise<any> {
            var promise: IHttpPromise<any> = this.$http.post(`/ajax/api/managers/users/${userHid}/publications/`, publication);

            promise.success(response => {});

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.CREATE.ERROR)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }


    }
}

