/// <reference path='../_all.ts' />


namespace Mappino.Cabinet.Users {
    export class PublicationsService {
        private _briefs: Array<Brief> = [];

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



        public create(publication: IPublicationNew): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.$http.post(`/ajax/api/cabinet/publications/`, publication);

            promise.success(response => {});

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.CREATE.TITLE)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }



        public remove(publicationIds: IPublicationIds): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.$http.delete(`/ajax/api/cabinet/publications/${publicationIds.tid}:${publicationIds.hid}/`);

            promise.success(response => {});

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.REMOVE.TITLE)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }



        public publish(publicationIds: IPublicationIds): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.$http.put(`/ajax/api/cabinet/publications/${publicationIds.tid}:${publicationIds.hid}/publish/`, null);

            promise.success(response => {});

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.PUBLISH.TITLE)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }



        public unpublish(publicationIds: IPublicationIds): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.$http.put(`/ajax/api/cabinet/publications/${publicationIds.tid}:${publicationIds.hid}/unpublish/`, null);

            promise.success(response => {});

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.UNPUBLISH.TITLE)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }



        public load(publicationIds: IPublicationIds): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.$http.get(`/ajax/api/cabinet/publications/${publicationIds.tid}:${publicationIds.hid}/`);

            promise.success(response => {
                this.publication = response.data;
            });

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



        public uploadPhoto(publicationIds: IPublicationIds, photo: File): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.Upload.upload({
                url: `/ajax/api/cabinet/publications/${publicationIds.tid}:${publicationIds.hid}/photos/`,
                file: photo
            });

            promise.success(response => {
                if (!this.publication.photos) {
                    this.publication.photos = [];
                }
                this.publication.photos.push(response.data);
            });

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.UPLOAD_PHOTO.TITLE)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }



        public removePhoto(publicationIds: IPublicationIds, photoId): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.$http.delete(`/ajax/api/cabinet/publications/${publicationIds.tid}:${publicationIds.hid}/photos/${photoId}/`);

            promise.success(response => {
                var photos = this.publication.photos;

                for (let i = 0, len = photos.length; i < len; i++) {
                    var photo = photos[i];

                    if (photo && photo.hash_id == photoId) {
                        this.publication.photos.splice(i, 1);
                    }
                }

                for (let i = 0, len = photos.length; i < len; i++) {
                    var photo = photos[i];
                    if (photo && photo.hash_id == response.data.hash_id) {
                        photo.is_title = true;
                    }
                }
            });

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.REMOVE_PHOTO.TITLE)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }



        public setTitlePhoto(publicationIds: IPublicationIds, photoId: string): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.$http.put(`/ajax/api/cabinet/publications/${publicationIds.tid}:${publicationIds.hid}/photos/${photoId}/title/`, null);

            promise.success(response => {
                var photos = this.publication.photos;

                for (let i = 0, len = photos.length; i < len; i++) {
                    var photo = photos[i];
                    photo.hash_id === photoId ? photo.is_title = true : photo.is_title = false;
                }
            });

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.SET_TITLE_PHOTO.TITLE)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }



        public checkField(publicationIds: IPublicationIds, field: IPublicationCheckField): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.$http.put(`/ajax/api/cabinet/publications/${publicationIds.tid}:${publicationIds.hid}/`, field);

            promise.success(response => {});

            promise.error(response => {
                this.$mdToast.show(this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.CHECK_FIELD.TITLE)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }


        public loadBriefs(): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.$http.get(`/ajax/api/cabinet/publications/briefs/all/`);

            promise.success(response => {
                for (let i = 0, len = response.data.length; i < len; i++) {
                    var brief = response.data[i];

                    this._briefs.push(new Brief(
                        brief.tid,
                        brief.hid,
                        brief.created,
                        brief.for_rent,
                        brief.for_sale,
                        brief.photo_url,
                        brief.state_sid,
                        brief.title,
                        brief.description,
                        brief.moderator_message
                    ));
                }
            });

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.LOAD_BRIEFS.TITLE)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }



        public get briefs() {
            return this._briefs;
        }
    }
}

