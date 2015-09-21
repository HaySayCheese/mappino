/// <reference path='../_all.ts' />


namespace Mappino.Cabinet.Moderators {
    export class ModeratingService {
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


        constructor(private $http: ng.IHttpService,
                    private $state: ng.ui.IStateService,
                    private $mdToast: any,
                    private TXT: any) {
            // ---------------------------------------------------------------------------------------------------------
        }



        public getPublicationId(): ng.IHttpPromise<any> {
            var promise: ng.IHttpPromise<any> = this.$http.get(`/ajax/api/moderators/publications/next/`);

            promise.success(response => {});

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.LOAD.ERROR)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }



        public load(publicationIds: any): ng.IHttpPromise<any> {
            var promise: ng.IHttpPromise<any> = this.$http.get(`/ajax/api/moderators/publications/${publicationIds.tid}:${publicationIds.hid}/`);

            promise.success(response => {});

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.LOAD.ERROR)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }



        public loadHeld(): ng.IHttpPromise<any> {
            var promise: ng.IHttpPromise<any> = this.$http.get(`/ajax/api/moderators/publications/held/briefs/`);

            promise.success(response => {});

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.LOAD.ERROR)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }



        public accept(publicationIds: any): ng.IHttpPromise<any> {
            var promise: ng.IHttpPromise<any> = this.$http.post(`/ajax/api/moderators/publications/${publicationIds.tid}:${publicationIds.hid}/accept/`, null);

            promise.success(response => {});

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.ACCEPT_MODERATING.ERROR)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }



        public reject(publicationIds: any, reject_reason: string): ng.IHttpPromise<any> {
            var promise: ng.IHttpPromise<any> = this.$http.post(`/ajax/api/moderators/publications/${publicationIds.tid}:${publicationIds.hid}/reject/`, {
                message: reject_reason
            });

            promise.success(response => {});

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.REJECT_MODERATING.ERROR)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }



        public hold(publicationIds: any): ng.IHttpPromise<any> {
            var promise: ng.IHttpPromise<any> = this.$http.post(`/ajax/api/moderators/publications/${publicationIds.tid}:${publicationIds.hid}/hold/`, null);

            promise.success(response => {});

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.HOLD_MODERATING.ERROR)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }



        public sendNotice(claimId: any, noticeMessage: any): ng.IHttpPromise<any> {
            var promise: ng.IHttpPromise<any> = this.$http.post(`/ajax/api/moderators/claims/${claimId}/notice/`, {
                notice: noticeMessage
            });

            promise.success(response => {});

            promise.error(response => {});

            return promise;
        }



        public closeClaim(claimId: any): ng.IHttpPromise<any> {
            var promise: ng.IHttpPromise<any> = this.$http.post(`/ajax/api/moderators/claims/${claimId}/close/`, null);

            promise.success(response => {});

            promise.error(response => {});

            return promise;
        }
    }
}

