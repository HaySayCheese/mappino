
namespace Mappino.Map {
    export class PublicationService  {
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



        public load(publicationIds: any): angular.IHttpPromise<any>  {
            var promise: angular.IHttpPromise<any> = this.$http.get(`/ajax/api/detailed/publication/${publicationIds.tid}:${publicationIds.hid}/`);

            promise.success(response => {
                this.publication = response.data;
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



        public loadContacts(publicationIds: any): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.$http.get(`/ajax/api/detailed/publication/${publicationIds.tid}:${publicationIds.hid}/contacts/`);

            promise.success(response => {
                this.publication.contacts = response.data;
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



        public sendMessage(message: Object, publicationIds: any): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.$http.post(`/ajax/api/notifications/send-message/${publicationIds.tid}:${publicationIds.hid}/`, {
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



        public sendCallRequest(callRequest: Object, publicationIds: any): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.$http.post(`/ajax/api/notifications/send-call-request/${publicationIds.tid}:${publicationIds.hid}/`, {
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



        public sendClaim(claim: Object, publicationIds: any): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.$http.post(`/ajax/api/publications/${publicationIds.tid}:${publicationIds.hid}/claims/`, {
                'email':        claim['email'],
                'reason_sid':   claim['reason_sid'],
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
    }
}

