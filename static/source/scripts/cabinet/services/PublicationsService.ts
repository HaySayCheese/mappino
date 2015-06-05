/// <reference path='../_references.ts' />


module pages.cabinet {
    export class PublicationsService {
        private _publication: Object;

        public static $inject = [
            '$http',
            '$state'
        ];


        constructor(
            private $http: angular.IHttpService,
            private $state: angular.ui.IStateService) {
            // ---------------------------------------------------------------------------------------------------------
        }



        public create(publication: Object, callback: Function) {
            var self = this;

            this.$http.post('/ajax/api/cabinet/publications/', publication)
                .then((response) => {
                    self.$state.go('publication_edit', { id: publication['tid'] + ":" + response.data['data']['id'] });

                    callback(response);
                }, () => {
                    // error
                });
        }



        public load(publication: Object, success_callback?, error_callback?) {
            var self = this;

            this.$http.get('/ajax/api/cabinet/publications/' + publication['tid'] + ':' + publication['hid'] + '/')
                .then((response) => {
                    if (response.data['code'] === 0) {
                        console.log(response.data['data']);
                        this._publication = response.data['data'];
                        this.createDefaultTerms();
                        _.isFunction(success_callback) && success_callback(this._publication)
                    } else {
                        _.isFunction(error_callback) && error_callback(response.data)
                    }

                }, (response) => {
                    _.isFunction(error_callback) && error_callback(response.data)
                })
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

