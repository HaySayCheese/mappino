/// <reference path='../_all.ts' />


module Mappino.Cabinet {
    export class PublicationsService implements IPublicationsService {
        private briefs: IBrief[];
        private publication: IPublication;

        public static $inject = [
            '$http',
            '$state',
            'Upload'
        ];


        constructor(private $http: angular.IHttpService,
                    private $state: angular.ui.IStateService,
                    private Upload: any) {
            // ---------------------------------------------------------------------------------------------------------
        }



        public create(publication: IPublicationNew, successCallback?, errorCallback?) {
            this.$http.post('/ajax/api/cabinet/publications/', publication)
                .then(response => {
                    if (response.data['code'] === 0) {
                        this.$state.go('publication_edit', { id: publication.tid + ":" + response.data['data']['id'] });
                        _.isFunction(successCallback) && successCallback(response.data)
                    } else {
                        _.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    _.isFunction(errorCallback) && errorCallback(response.data)
                });
        }



        public remove(publicationIds: IPublicationIds, successCallback?, errorCallback?) {
            this.$http.delete('/ajax/api/cabinet/publications/' + publicationIds.tid + ':' + publicationIds.hid + '/')
                .then(response => {
                    if (response.data['code'] === 0) {
                        this.$state.go('publications');
                        _.isFunction(successCallback) && successCallback(response.data)
                    } else {
                        _.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    _.isFunction(errorCallback) && errorCallback(response.data)
                });
        }



        public publish(publicationIds: IPublicationIds, successCallback?, errorCallback?) {
            this.$http.put('/ajax/api/cabinet/publications/' + publicationIds.tid + ':' + publicationIds.hid + '/publish/', null)
                .then(response => {
                    if (response.data['code'] === 0) {
                        this.$state.go('publications');
                        _.isFunction(successCallback) && successCallback(response.data)
                    } else {
                        _.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    _.isFunction(errorCallback) && errorCallback(response.data)
                });
        }



        public load(publicationIds: IPublicationIds, successCallback?, errorCallback?) {
            this.$http.get('/ajax/api/cabinet/publications/' + publicationIds.tid + ':' + publicationIds.hid + '/')
                .then(response => {
                    if (response.data['code'] === 0) {
                        this.publication = response.data['data'];
                        this.createDefaultTerms();
                        _.isFunction(successCallback) && successCallback(this.publication)
                    } else {
                        _.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    _.isFunction(errorCallback) && errorCallback(response.data)
                })
        }



        public uploadPhoto(publicationIds: IPublicationIds, photo: File, successCallback?, errorCallback?) {
            this.Upload.upload({
                url: '/ajax/api/cabinet/publications/' + publicationIds.tid + ':' + publicationIds.hid + '/photos/',
                file: photo
            }).then(response => {
                if (response.data['code'] === 0) {
                    if (!this.publication.photos) {
                        this.publication.photos = [];
                    }
                    this.publication.photos.push(response.data['data']);
                    _.isFunction(successCallback) && successCallback(this.publication)
                } else {
                    _.isFunction(errorCallback) && errorCallback(response.data)
                }
            });
        }



        public removePhoto(publicationIds: IPublicationIds, photoId, successCallback?, errorCallback?) {
            this.$http.delete('/ajax/api/cabinet/publications/' + publicationIds.tid + ':' + publicationIds.hid + '/photos/' + photoId + '/')
                .then(response => {
                    if (response.data['code'] === 0) {
                        _.each(this.publication.photos, (photo, index, list) => {
                            if (photo && photo.hash_id == photoId) {
                                this.publication.photos.splice(index, 1);
                            }

                            if (photo && photo.hash_id == response.data['data'].hash_id) {
                                this.publication.photos[index].is_title = true;
                            }
                        });

                        _.isFunction(successCallback) && successCallback(this.publication)
                    } else {
                        _.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    _.isFunction(errorCallback) && errorCallback(response.data)
                })
        }



        public setTitlePhoto(publicationIds: IPublicationIds, photoId, successCallback?, errorCallback?) {
            this.$http.put('/ajax/api/cabinet/publications/' + publicationIds.tid + ':' + publicationIds.hid + '/photos/' + photoId + '/title/', null)
                .then(response => {
                    if (response.data['code'] === 0) {
                        _.each(this.publication.photos, (photo, index, list) => {
                            photo.is_title = false;

                            if (photo.hash_id === photoId) {
                                this.publication.photos[index].is_title = true;
                            }
                        });

                        _.isFunction(successCallback) && successCallback(this.publication)
                    } else {
                        _.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    _.isFunction(errorCallback) && errorCallback(response.data)
                })
        }



        public checkField(publicationIds: IPublicationIds, field: IPublicationCheckField, successCallback?, errorCallback?) {
            this.$http.put('/ajax/api/cabinet/publications/' + publicationIds.tid + ':' + publicationIds.hid + '/', field)
                .then(response => {
                    if (response.data['code'] === 0) {
                        _.isFunction(successCallback) &&
                        successCallback(response.data['data'] && response.data['data'].value ? response.data['data'].value : field.fieldValue);
                    }
                }, response => {
                    _.isFunction(errorCallback) && errorCallback(response.data);
                });
        }



        public loadBriefs(successCallback?, errorCallback?) {
            this.$http.get('/ajax/api/cabinet/publications/briefs/all/')
                .then(response => {
                    if (response.data['code'] === 0) {
                        this.briefs = response.data['data'];
                        _.isFunction(successCallback) && successCallback(this.briefs)
                    } else {
                        _.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    _.isFunction(errorCallback) && errorCallback(response.data)
                });
        }



        private createDefaultTerms() {
            if (_.isNull(this.publication['sale_terms'])) {
                this.publication['sale_terms'] = {};

                _.defaults(this.publication['sale_terms'], {
                    add_terms:          null,
                    currency_sid:       '0',
                    is_contract:        false,
                    price:              null,
                    sale_type_sid:      '0',
                    transaction_sid:    '0'
                });
            }

            if (_.isNull(this.publication['rent_terms'])) {
                this.publication['rent_terms'] = {};

                _.defaults(this.publication['rent_terms'], {
                    add_terms:      null,
                    currency_sid:   '0',
                    is_contract:    false,
                    period_sid:     '1',
                    persons_count:  null,
                    price:          null,
                    rent_type_sid:  '0'
                });
            }
        }

    }
}

