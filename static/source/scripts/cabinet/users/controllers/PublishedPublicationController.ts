namespace Mappino.Cabinet.Users  {
    'use strict';

    export class PublishedPublicationController {

        private publicationIds:any = {
            tid: undefined,
            hid: undefined
        };

        public static $inject = [
            '$scope',
            '$state'
        ];

        constructor(private $scope,
                    private $state) {
            $scope.showRentDetails = false;

            if ($state.params['publication_id'] && $state.params['publication_id'] != 0) {
                this.publicationIds.tid = $state.params['publication_id'].split(':')[0];
                this.publicationIds.hid = $state.params['publication_id'].split(':')[1];
            }


            $scope.reservation = {
                dateEnter: undefined,
                dateLeave: undefined,
                clientName: undefined
            };

        }

    }
}