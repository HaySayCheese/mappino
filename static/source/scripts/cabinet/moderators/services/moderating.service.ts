/// <reference path='../_all.ts' />


module Mappino.Cabinet.Moderators {
    export class ModeratingService {
        private publication: any;

        private toastOptions = {
            position:   'top right',
            delay:      5000
        };

        public static $inject = [
            '$http',
            '$state',
            '$mdToast',
            'TXT'
        ];


        constructor(private $http: angular.IHttpService,
                    private $state: angular.ui.IStateService,
                    private $mdToast: any,
                    private TXT: any) {
            // ---------------------------------------------------------------------------------------------------------
        }



        public load(successCallback?, errorCallback?) {
            this.$http.get(`/ajax/api/moderators/publications/next/`)
                .then(response => {
                    if (response.data['code'] === 0) {
                        angular.isFunction(successCallback) && successCallback(response.data)
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    this.$mdToast.show(
                        this.$mdToast.simple()
                            .content(this.TXT.TOASTS.PUBLICATION.LOAD.TITLE)
                            .position(this.toastOptions.position)
                            .hideDelay(this.toastOptions.delay)
                    );
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                });
        }



        public accept(successCallback?, errorCallback?) {
            this.$http.post(`/ajax/api/moderators/publications/accept/`, null)
                .then(response => {
                    if (response.data['code'] === 0) {
                        angular.isFunction(successCallback) && successCallback(response.data)
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    //this.$mdToast.show(
                    //    this.$mdToast.simple()
                    //        .content(this.TXT.TOASTS.PUBLICATION.REMOVE.TITLE)
                    //        .position(this.toastOptions.position)
                    //        .hideDelay(this.toastOptions.delay)
                    //);
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                });
        }



        public reject(reject_reason: string, successCallback?, errorCallback?) {
            this.$http.post(`/ajax/api/moderators/publications/reject/`, reject_reason)
                .then(response => {
                    if (response.data['code'] === 0) {
                        angular.isFunction(successCallback) && successCallback(response.data)
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    //this.$mdToast.show(
                    //    this.$mdToast.simple()
                    //        .content(this.TXT.TOASTS.PUBLICATION.PUBLISH.TITLE)
                    //        .position(this.toastOptions.position)
                    //        .hideDelay(this.toastOptions.delay)
                    //);
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                });
        }
    }
}

