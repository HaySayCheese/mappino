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



        public getPublicationId(successCallback?, errorCallback?) {
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



        public load(publicationIds: any, successCallback?, errorCallback?) {
            this.$http.get(`/ajax/api/moderators/publications/${publicationIds.tid}:${publicationIds.hid}/`)
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



        public loadHeld(successCallback?, errorCallback?) {
            this.$http.get(`/ajax/api/moderators/publications/held/briefs/`)
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



        public accept(publicationIds: any, successCallback?, errorCallback?) {
            this.$http.post(`/ajax/api/moderators/publications/${publicationIds.tid}:${publicationIds.hid}/accept/`, null)
                .then(response => {
                    if (response.data['code'] === 0) {
                        angular.isFunction(successCallback) && successCallback(response.data)
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    this.$mdToast.show(
                        this.$mdToast.simple()
                            .content(this.TXT.TOASTS.PUBLICATION.ACCEPT_MODERATING.TITLE)
                            .position(this.toastOptions.position)
                            .hideDelay(this.toastOptions.delay)
                    );
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                });
        }



        public reject(publicationIds: any, reject_reason: string, successCallback?, errorCallback?) {
            this.$http.post(`/ajax/api/moderators/publications/${publicationIds.tid}:${publicationIds.hid}/reject/`, {
                message: reject_reason
            })
                .then(response => {
                    if (response.data['code'] === 0) {
                        angular.isFunction(successCallback) && successCallback(response.data)
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    this.$mdToast.show(
                        this.$mdToast.simple()
                            .content(this.TXT.TOASTS.PUBLICATION.REJECT_MODERATING.TITLE)
                            .position(this.toastOptions.position)
                            .hideDelay(this.toastOptions.delay)
                    );
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                });
        }



        public hold(publicationIds: any, successCallback?, errorCallback?) {
            this.$http.post(`/ajax/api/moderators/publications/${publicationIds.tid}:${publicationIds.hid}/hold/`, null)
                .then(response => {
                    if (response.data['code'] === 0) {
                        angular.isFunction(successCallback) && successCallback(response.data)
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    this.$mdToast.show(
                        this.$mdToast.simple()
                            .content(this.TXT.TOASTS.PUBLICATION.HOLD_MODERATING.TITLE)
                            .position(this.toastOptions.position)
                            .hideDelay(this.toastOptions.delay)
                    );
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                });
        }



        public sendNotice(claimId: any, noticeMessage: any, successCallback?, errorCallback?) {
            this.$http.post(`/ajax/api/moderators/claims/${claimId}/notice/`, {
                notice: noticeMessage
            })
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



        public closeClaim(claimId: any, successCallback?, errorCallback?) {
            this.$http.post(`/ajax/api/moderators/claims/${claimId}/close/`, null)
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

