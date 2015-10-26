namespace Mappino.Core.PublicationPreview {

    import IHttpService = angular.IHttpService;
    import IStateService = angular.ui.IStateService;
    import IHttpPromise = angular.IHttpPromise;

    "use strict";


    export class PublicationPreviewService {
        private _publication: any;

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

        constructor(
            private $http: IHttpService,
            private $state: IStateService,
            private $mdToast: any,
            private TXT: any) {
            // ---------------------------------------------------------------------------------------------------------


        }


        public loadPublicationData(publicationIds: any): IHttpPromise<any>  {
            var promise: IHttpPromise<any> = this.$http.get(`/ajax/api/detailed/publication/${publicationIds.tid}:${publicationIds.hid}/`);

            promise.success(response => {
                this._publication = response.data;
            });

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



        public loadPublicationContacts(publicationIds: any): IHttpPromise<any> {
            var promise: IHttpPromise<any> = this.$http.get(`/ajax/api/detailed/publication/${publicationIds.tid}:${publicationIds.hid}/contacts/`);

            promise.success(response => {
                this._publication.contacts = response.data;
            });

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.LOAD_CONTACTS.ERROR)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }



        public sendMessage(message: Object, publicationIds: any): IHttpPromise<any> {
            var promise: IHttpPromise<any> = this.$http.post(`/ajax/api/notifications/send-message/${publicationIds.tid}:${publicationIds.hid}/`, {
                'name':     message['userName'],
                'email':    message['email'],
                'message':  message['text']
            });

            promise.success(response => {});

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.SEND_MESSAGE.ERROR)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }



        public sendCallRequest(callRequest: Object, publicationIds: any): IHttpPromise<any> {
            var promise: IHttpPromise<any> = this.$http.post(`/ajax/api/notifications/send-call-request/${publicationIds.tid}:${publicationIds.hid}/`, {
                'name': callRequest['userName'],
                'phone_number': callRequest['phoneNumber']
            });

            promise.success(response => {});

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.SEND_CALL_REQUEST.ERROR)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }



        public sendClaim(claim: Object, publicationIds: any): IHttpPromise<any> {
            var promise: IHttpPromise<any> = this.$http.post(`/ajax/api/publications/${publicationIds.tid}:${publicationIds.hid}/claims/`, {
                'email':        claim['email'],
                'reason_tid':   claim['reason_sid'],
                'message':      claim['another_reason']
            });


            promise.success(response => {});

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.SEND_CLAIM.ERROR)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }



        public get publication() {
            return this._publication;
        }
    }
}