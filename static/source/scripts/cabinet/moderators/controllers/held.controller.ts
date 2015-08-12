/// <reference path='../_all.ts' />


module Mappino.Cabinet.Moderators {
    export class HeldController {
        private publicationIds: any = {
            tid: null,
            hid: null
        };

        public static $inject = [
            '$scope',
            '$rootScope',
            'ModeratingService'
        ];

        constructor(private $scope: any,
                    private $rootScope: any,
                    private moderatingService: ModeratingService) {
            // ---------------------------------------------------------------------------------------------------------
            $rootScope.pageTitle = 'Отложенные mappino';

            this.load();
        }



        private load() {
            this.$rootScope.loaders.overlay = true;
            this.moderatingService.loadHeld(response => {
                this.$scope.briefs = response.data;
                this.$rootScope.loaders.overlay = false;
            }, response => {
                //
            });
        }
    }
}