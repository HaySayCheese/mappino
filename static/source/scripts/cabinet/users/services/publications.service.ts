/// <reference path='../_all.ts' />


namespace Mappino.Cabinet.Users {
    export class PublicationsService implements IPublicationsService {
        private briefs: IBrief[];
        private publication: IPublication;

        private toastOptions = {
            position:   'top right',
            delay:      5000
        };

        public static $inject = [
            '$http',
            '$state',
            '$mdToast',
            'Upload',
            'TXT'
        ];


        constructor(private $http: angular.IHttpService,
                    private $state: angular.ui.IStateService,
                    private $mdToast: any,
                    private Upload: any,
                    private TXT: any) {
            // ---------------------------------------------------------------------------------------------------------
        }



        public create(publication: IPublicationNew, successCallback?, errorCallback?) {
            this.$http.post(`/ajax/api/cabinet/publications/`, publication)
                .then(response => {
                    if (response.data['code'] === 0) {
                        angular.isFunction(successCallback) && successCallback(response.data)
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    this.$mdToast.show(
                        this.$mdToast.simple()
                            .content(this.TXT.TOASTS.PUBLICATION.CREATE.TITLE)
                            .position(this.toastOptions.position)
                            .hideDelay(this.toastOptions.delay)
                    );
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                });
        }



        public remove(publicationIds: IPublicationIds, successCallback?, errorCallback?) {
            this.$http.delete(`/ajax/api/cabinet/publications/${publicationIds.tid}:${publicationIds.hid}/`)
                .then(response => {
                    if (response.data['code'] === 0) {
                        this.$state.go('publications');
                        angular.isFunction(successCallback) && successCallback(response.data)
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    this.$mdToast.show(
                        this.$mdToast.simple()
                            .content(this.TXT.TOASTS.PUBLICATION.REMOVE.TITLE)
                            .position(this.toastOptions.position)
                            .hideDelay(this.toastOptions.delay)
                    );
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                });
        }



        public publish(publicationIds: IPublicationIds, successCallback?, errorCallback?) {
            this.$http.put(`/ajax/api/cabinet/publications/${publicationIds.tid}:${publicationIds.hid}/publish/`, null)
                .then(response => {
                    if (response.data['code'] === 0) {
                        this.$state.go('publications');
                        angular.isFunction(successCallback) && successCallback(response.data)
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    this.$mdToast.show(
                        this.$mdToast.simple()
                            .content(this.TXT.TOASTS.PUBLICATION.PUBLISH.TITLE)
                            .position(this.toastOptions.position)
                            .hideDelay(this.toastOptions.delay)
                    );
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                });
        }



        public unpublish(publicationIds: IPublicationIds, successCallback?, errorCallback?) {
            this.$http.put(`/ajax/api/cabinet/publications/${publicationIds.tid}:${publicationIds.hid}/unpublish/`, null)
                .then(response => {
                    if (response.data['code'] === 0) {
                        this.$state.go('publications');
                        angular.isFunction(successCallback) && successCallback(response.data)
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    this.$mdToast.show(
                        this.$mdToast.simple()
                            .content(this.TXT.TOASTS.PUBLICATION.UNPUBLISH.TITLE)
                            .position(this.toastOptions.position)
                            .hideDelay(this.toastOptions.delay)
                    );
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                });
        }



        public load(publicationIds: IPublicationIds, successCallback?, errorCallback?) {
            this.$http.get(`/ajax/api/cabinet/publications/${publicationIds.tid}:${publicationIds.hid}/`)
                .then(response => {
                    if (response.data['code'] === 0) {
                        this.publication = response.data['data'];
                        angular.isFunction(successCallback) && successCallback(this.publication)
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



        public uploadPhoto(publicationIds: IPublicationIds, photo: File, successCallback?, errorCallback?) {
            this.Upload.upload({
                url: `/ajax/api/cabinet/publications/${publicationIds.tid}:${publicationIds.hid}/photos/`,
                file: photo
            }).then(response => {
                if (response.data['code'] === 0) {
                    if (!this.publication.photos) {
                        this.publication.photos = [];
                    }
                    this.publication.photos.push(response.data['data']);
                    angular.isFunction(successCallback) && successCallback(this.publication)
                } else {
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                }
            }, response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.UPLOAD_PHOTO.TITLE)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
                angular.isFunction(errorCallback) && errorCallback(response.data)
            });
        }



        public removePhoto(publicationIds: IPublicationIds, photoId, successCallback?, errorCallback?) {
            this.$http.delete(`/ajax/api/cabinet/publications/${publicationIds.tid}:${publicationIds.hid}/photos/${photoId}/`)
                .then(response => {
                    if (response.data['code'] === 0) {
                        angular.forEach(this.publication.photos, (photo, index) => {
                            if (photo && photo.hash_id == photoId) {
                                this.publication.photos.splice(index, 1);
                            }
                        });

                        angular.forEach(this.publication.photos, (photo, index) => {
                            if (photo && photo.hash_id == response.data['data'].hash_id) {
                                this.publication.photos[index].is_title = true;
                            }
                        });

                        angular.isFunction(successCallback) && successCallback(this.publication)
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    this.$mdToast.show(
                        this.$mdToast.simple()
                            .content(this.TXT.TOASTS.PUBLICATION.REMOVE_PHOTO.TITLE)
                            .position(this.toastOptions.position)
                            .hideDelay(this.toastOptions.delay)
                    );
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                })
        }



        public setTitlePhoto(publicationIds: IPublicationIds, photoId, successCallback?, errorCallback?) {
            this.$http.put(`/ajax/api/cabinet/publications/${publicationIds.tid}:${publicationIds.hid}/photos/${photoId}/title/`, null)
                .then(response => {
                    if (response.data['code'] === 0) {
                        angular.forEach(this.publication.photos, (photo, index) => {
                            photo.hash_id === photoId ? this.publication.photos[index].is_title = true :
                                this.publication.photos[index].is_title = false;
                        });

                        angular.isFunction(successCallback) && successCallback(this.publication)
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    this.$mdToast.show(
                        this.$mdToast.simple()
                            .content(this.TXT.TOASTS.PUBLICATION.SET_TITLE_PHOTO.TITLE)
                            .position(this.toastOptions.position)
                            .hideDelay(this.toastOptions.delay)
                    );
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                })
        }



        public checkField(publicationIds: IPublicationIds, field: IPublicationCheckField, successCallback?, errorCallback?) {
            this.$http.put(`/ajax/api/cabinet/publications/${publicationIds.tid}:${publicationIds.hid}/`, field)
                .then(response => {
                    if (response.data['code'] === 0) {
                        angular.isFunction(successCallback) &&
                        successCallback(response.data['data'] && response.data['data'].value ? response.data['data'].value : field.fieldValue);
                    }
                }, response => {
                    this.$mdToast.show(this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.CHECK_FIELD.TITLE)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                    );
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                });
        }



        public loadBriefs(successCallback?, errorCallback?) {
            this.$http.get(`/ajax/api/cabinet/publications/briefs/all/`)
                .then(response => {
                    if (response.data['code'] === 0) {
                        this.briefs = response.data['data'];
                        angular.isFunction(successCallback) && successCallback(this.briefs)
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    this.$mdToast.show(
                        this.$mdToast.simple()
                            .content(this.TXT.TOASTS.PUBLICATION.LOAD_BRIEFS.TITLE)
                            .position(this.toastOptions.position)
                            .hideDelay(this.toastOptions.delay)
                    );
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                });
        }
    }
}

