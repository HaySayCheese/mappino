/// <reference path='../_all.ts' />


module mappino.cabinet {
    export class PublicationsService {
        private briefs: Object[];
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



        public loadBriefs(success?, error?) {
            this.$http.get('/ajax/api/cabinet/publications/briefs/all/')
                .then((response) => {
                    if (response.data['code'] === 0) {
                        this.briefs = response.data['data'];
                        _.isFunction(success) && success(this.briefs)
                    } else {
                        _.isFunction(error) && error(response.data)
                    }
                }, (response) => {
                    _.isFunction(error) && error(response.data)
                });
        }



        public create(publication: IPublicationNew, success?, error?) {
            this.$http.post('/ajax/api/cabinet/publications/', publication)
                .then((response) => {
                    if (response.data['code'] === 0) {
                        this.$state.go('publication_edit', { id: publication.tid + ":" + response.data['data']['id'] });
                        _.isFunction(success) && success(response.data)
                    } else {
                        _.isFunction(error) && error(response.data)
                    }
                }, (response) => {
                    _.isFunction(error) && error(response.data)
                });
        }



        public publish(publicationIds: IPublicationIds, success?, error?) {
            this.$http.put('/ajax/api/cabinet/publications/' + publicationIds.tid + ':' + publicationIds.hid + '/publish/', null)
                .then((response) => {
                    if (response.data['code'] === 0) {
                        this.$state.go('publications');
                        _.isFunction(success) && success(response.data)
                    } else {
                        _.isFunction(error) && error(response.data)
                    }
                }, (response) => {
                    _.isFunction(error) && error(response.data)
                });
        }



        public loadPublication(publicationIds: IPublicationIds, success?, error?) {
            this.$http.get('/ajax/api/cabinet/publications/' + publicationIds.tid + ':' + publicationIds.hid + '/')
                .then((response) => {
                    if (response.data['code'] === 0) {
                        this.publication = response.data['data'];
                        this.createDefaultTerms();
                        _.isFunction(success) && success(this.publication)
                    } else {
                        _.isFunction(error) && error(response.data)
                    }
                }, (response) => {
                    _.isFunction(error) && error(response.data)
                })
        }



        public checkField(publicationIds: IPublicationIds, field: IPublicationCheckField, success?, error?) {
            this.$http.put('/ajax/api/cabinet/publications/' + publicationIds.tid + ':' + publicationIds.hid + '/', field)
                .then((response) => {
                    if (response.data['code'] === 0) {
                        _.isFunction(success) && success(response.data['data'] && response.data['data'].value ? response.data['data'].value : field.fieldValue);
                    }
                }, (response) => {
                    _.isFunction(error) && error(response.data);
                });
        }



        public uploadPublicationPhotos(publicationIds: IPublicationIds, photos: Array<File>, success?, error?) {
            if (photos && photos.length) {
                for (var i = 0; i < photos.length; i++) {
                    var file = photos[i];

                    this.Upload.upload({
                        url: '/ajax/api/cabinet/publications/' + publicationIds.tid + ':' + publicationIds.hid + '/photos/',
                        file: file
                    }).then((response) => {
                        if (response.data['code'] === 0) {
                            if (!this.publication.photos) {
                                this.publication.photos = [];
                            }
                            this.publication.photos.push(response.data['data']);
                            _.isFunction(success) && success(this.publication)
                        } else {
                            _.isFunction(error) && error(response.data)
                        }
                    });
                }
            }
        }


        public removePublicationPhoto(publicationIds: IPublicationIds, photoId: any, success?, error?) {
            this.$http.delete('/ajax/api/cabinet/publications/' + publicationIds.tid + ':' + publicationIds.hid + '/photos/' + photoId + '/')
                .then((response) => {
                    if (response.data['code'] === 0) {
                        _.each(this.publication.photos, (photo, index, list) => {
                            if (photo.hash_id === photoId) {
                                this.publication.photos.splice(index, 1);
                            }
                        });

                        _.isFunction(success) && success(this.publication)
                    } else {
                        _.isFunction(error) && error(response.data)
                    }
                }, (response) => {
                    _.isFunction(error) && error(response.data)
                })
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

