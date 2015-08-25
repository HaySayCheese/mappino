
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



        public load(publicationIds: any, successCallback?, errorCallback?) {
            this.$http.get(`/ajax/api/detailed/publication/${publicationIds.tid}:${publicationIds.hid}/`)
                .then(response => {
                    if (response.data['code'] === 0) {
                        this.publication = response.data['data'];
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



        public loadContacts(publicationIds: any, successCallback?, errorCallback?) {
            this.$http.get(`/ajax/api/detailed/publication/${publicationIds.tid}:${publicationIds.hid}/contacts/`)
                .then(response => {
                    if (response.data['code'] === 0) {
                        this.publication = response.data['data'];
                        angular.isFunction(successCallback) && successCallback(response.data)
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    this.$mdToast.show(
                        this.$mdToast.simple()
                            .content(this.TXT.TOASTS.PUBLICATION.LOAD_CONTACTS.TITLE)
                            .position(this.toastOptions.position)
                            .hideDelay(this.toastOptions.delay)
                    );
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                });
        }



        public sendMessage(message: Object, publicationIds: any, successCallback?, errorCallback?) {
            this.$http.post(`/ajax/api/notifications/send-message/${publicationIds.tid}:${publicationIds.hid}/`, {
                'name':     message['userName'],
                'email':    message['email'],
                'message':  message['text']
            })
                .then(response => {
                    if (response.data['code'] == 0) {
                        angular.isFunction(successCallback) && successCallback(response.data)
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    this.$mdToast.show(
                        this.$mdToast.simple()
                            .content(this.TXT.TOASTS.PUBLICATION.SEND_MESSAGE.TITLE)
                            .position(this.toastOptions.position)
                            .hideDelay(this.toastOptions.delay)
                    );
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                })
        }



        public sendCallRequest(callRequest: Object, publicationIds: any, successCallback?, errorCallback?) {
            this.$http.post(`/ajax/api/notifications/send-call-request/${publicationIds.tid}:${publicationIds.hid}/`, {
                'name': callRequest['userName'],
                'phone_number': callRequest['phoneNumber']
            })
                .then(response => {
                    if (response.data['code'] == 0) {
                        angular.isFunction(successCallback) && successCallback(response.data)
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    this.$mdToast.show(
                        this.$mdToast.simple()
                            .content(this.TXT.TOASTS.PUBLICATION.SEND_CALL_REQUEST.TITLE)
                            .position(this.toastOptions.position)
                            .hideDelay(this.toastOptions.delay)
                    );
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                })
        }



        public sendClaim(claim: Object, publicationIds: any, successCallback?, errorCallback?) {
            this.$http.post(`/ajax/api/publications/${publicationIds.tid}:${publicationIds.hid}/claims/`, {
                'email':        claim['email'],
                'reason_sid':   claim['reason_sid'],
                'message':      claim['another_reason']
            })
                .then(response => {
                    if (response.data['code'] == 0) {
                        angular.isFunction(successCallback) && successCallback(response.data)
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    this.$mdToast.show(
                        this.$mdToast.simple()
                            .content(this.TXT.TOASTS.PUBLICATION.SEND_CLAIM.TITLE)
                            .position(this.toastOptions.position)
                            .hideDelay(this.toastOptions.delay)
                    );
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                })
        }
    }
}

