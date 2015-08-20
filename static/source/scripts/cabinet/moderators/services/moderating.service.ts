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


        constructor(private $http: angular.IHttpService,
                    private $state: angular.ui.IStateService,
                    private $mdToast: any,
                    private TXT: any) {
            // ---------------------------------------------------------------------------------------------------------
        }



        public getPublicationId(): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.$http.get(`/ajax/api/moderators/publications/next/`);
            promise.success(response => {});
            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.LOAD.TITLE)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });
            return promise;

        }



        public load(publicationIds: any): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.$http.get(`/ajax/api/moderators/publications/${publicationIds.tid}:${publicationIds.hid}/`);
            promise.success(response => {});
            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.LOAD.TITLE)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });
            return promise;
        }



        public loadHeld(): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.$http.get(`/ajax/api/moderators/publications/held/briefs/`);
            promise.success(response => {});
            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.LOAD.TITLE)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });
            return promise;
        }



        public accept(publicationIds: any): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.$http.post(`/ajax/api/moderators/publications/${publicationIds.tid}:${publicationIds.hid}/accept/`, null);
            promise.success(response => {});
            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.ACCEPT_MODERATING.TITLE)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });
            return promise;
        }



        public reject(publicationIds: any, reject_reason: string): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.$http.post(`/ajax/api/moderators/publications/${publicationIds.tid}:${publicationIds.hid}/reject/`, {
                message: reject_reason
            });
            promise.success(response => {});
            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.REJECT_MODERATING.TITLE)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });
            return promise;
        }



        public hold(publicationIds: any): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.$http.post(`/ajax/api/moderators/publications/${publicationIds.tid}:${publicationIds.hid}/hold/`, null);
            promise.success(response => {});
            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.HOLD_MODERATING.TITLE)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });
            return promise;
        }



        public sendNotice(claimId: any, noticeMessage: any): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.$http.post(`/ajax/api/moderators/claims/${claimId}/notice/`, {
                notice: noticeMessage
            });
            promise.success(response => {});
            promise.error(response => {});
            return promise;
        }



        public closeClaim(claimId: any): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.$http.post(`/ajax/api/moderators/claims/${claimId}/close/`, null);
            promise.success(response => {});
            promise.error(response => {});
            return promise;

        }
    }
}

