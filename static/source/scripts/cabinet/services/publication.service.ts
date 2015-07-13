/// <reference path='../_all.ts' />


module mappino.cabinet {
    export class PublicationsService {
        private _publication: Object;
        private _publications: Object;

        public static $inject = [
            '$http',
            '$state'
        ];


        constructor(
            private $http: angular.IHttpService,
            private $state: angular.ui.IStateService) {
            // ---------------------------------------------------------------------------------------------------------
        }



        public loadBriefs(success?, error?) {
            this.$http.get('/ajax/api/cabinet/publications/briefs/all/')
                .then((response) => {
                    if (response.data['code'] === 0) {
                        this._publications = response.data['data'];
                        _.isFunction(success) && success(this._publications)
                    } else {
                        _.isFunction(error) && error(response.data)
                    }
                }, (response) => {
                    _.isFunction(error) && error(response.data)
                });
        }



        public create(publication: Object, success?, error?) {
            this.$http.post('/ajax/api/cabinet/publications/', publication)
                .then((response) => {
                    if (response.data['code'] === 0) {
                        this.$state.go('publication_edit', { id: publication['tid'] + ":" + response.data['data']['id'] });
                        _.isFunction(success) && success(response.data)
                    } else {
                        _.isFunction(error) && error(response.data)
                    }
                }, (response) => {
                    _.isFunction(error) && error(response.data)
                });
        }



        public publish(publication: Object, success?, error?) {
            this.$http.put('/ajax/api/cabinet/publications/' + publication['tid'] + ':' + publication['hid'] + '/publish/', null)
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



        public loadPublication(publication: Object, success?, error?) {
            this.$http.get('/ajax/api/cabinet/publications/' + publication['tid'] + ':' + publication['hid'] + '/')
                .then((response) => {
                    if (response.data['code'] === 0) {
                        console.log(response.data['data']);
                        this._publication = response.data['data'];
                        this.createDefaultTerms();
                        _.isFunction(success) && success(this._publication)
                    } else {
                        _.isFunction(error) && error(response.data)
                    }
                }, (response) => {
                    _.isFunction(error) && error(response.data)
                })
        }



        public checkField(publication: Object, field, success?, error?) {
            var fieldName   = field.f,
                fieldValue  = field.v;

            this.$http.put('/ajax/api/cabinet/publications/' + publication['tid'] + ':' + publication['hid'] + '/', field)
                .then((response) => {
                    if (response.data['code'] === 0) {
                        _.isFunction(success) && success(response.data['data'] && response.data['data'].value ? response.data['data'].value : fieldValue);
                    }
                }, (response) => {
                    _.isFunction(error) && error(response.data);
                });
        }



        private createDefaultTerms() {
            if (_.isNull(this._publication['sale_terms'])) {
                this._publication['sale_terms'] = {};

                _.defaults(this._publication['sale_terms'], {
                    add_terms:          null,
                    currency_sid:       '0',
                    is_contract:        false,
                    price:              null,
                    sale_type_sid:      '0',
                    transaction_sid:    '0'
                });
            }

            if (_.isNull(this._publication['rent_terms'])) {
                this._publication['rent_terms'] = {};

                _.defaults(this._publication['rent_terms'], {
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

