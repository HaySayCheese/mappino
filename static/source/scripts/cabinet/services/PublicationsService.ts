/// <reference path='../_references.ts' />


module pages.cabinet {
    export class PublicationsService {
        private publication: Object;

        public static $inject = [
            '$http',
            '$state'
        ];

        constructor(
            private $http: angular.IHttpService,
            private $state: angular.ui.IStateService) {
            // -
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



        public loadPublicationData(publication: Object, callback: Function) {
            var self = this;

            this.$http.get('/ajax/api/cabinet/publications/' + publication['tid'] + ':' + publication['hid'] + '/')
                .then((response) => {
                    console.log(response)
                    callback(response)
                }, () => {
                    // -
                })
        }

    }
}

