/// <reference path='../_all.ts' />


module Mappino.Cabinet {
    export class BriefsController {
        private briefs: Array<IBrief> = [];

        private newPublication: IPublicationNew = {
            tid:        0,
            for_sale:   true,
            for_rent:   false
        };

        public static $inject = [
            '$scope',
            '$rootScope',
            '$mdDialog',
            'PublicationsService'
        ];

        constructor(private $scope: any,
                    private $rootScope: any,
                    private $mdDialog: any,
                    private publicationsService: IPublicationsService) {
            // ---------------------------------------------------------------------------------------------------------
            $scope.briefs = this.briefs;
            $scope.newPublication = this.newPublication;

            this.loadBriefs();
        }


        public removeBrief($event, briefTid, briefId) {
            // Appending dialog to document.body to cover sidenav in docs app
            var confirm = this.$mdDialog
                .confirm()
                .parent(angular.element(document.body))
                .title('Р’С‹ РЅР° СЃР°РјРѕРј РґРµР»Рµ С…РѕС‚РёС‚Рµ СѓРґР°Р»РёС‚СЊ СЌС‚Рѕ РѕР±СЉСЏРІР»РµРЅРёРµ?')
                .content('Р’СЃРµ РґР°РЅРЅС‹Рµ РїРѕ СЌС‚РѕРјСѓ РѕР±СЉСЏРІР»РµРЅРёСЋ Р±СѓРґСѓС‚ СѓРґР°Р»РµРЅС‹ РЅР°РІСЃРµРіРґР°.')
                //.ariaLabel('Lucky day')
                .ok('РЈРґР°Р»РёС‚СЊ')
                .cancel('РћС‚РјРµРЅРёС‚СЊ СѓРґР°Р»РµРЅРёРµ')
                .targetEvent($event);


            this.$mdDialog.show(confirm)
                .then(() => {
                    this.publicationsService.remove({ tid: briefTid, hid: briefId }, () => {
                        angular.forEach(this.$scope.briefs, (brief, index) => {
                            if (brief.id == briefId) {
                                this.$scope.briefs.splice(index, 1)
                            }
                        })
                    })
                });
        }



        public loadBriefs() {
            this.$rootScope.loaders.navbar = true;

            this.publicationsService.loadBriefs(response => {
                this.$scope.briefs = response;
                this.$rootScope.loaders.navbar = false;
            });
        }



        // using in scope
        private createPublication() {
            this.publicationsService.create(this.$scope.newPublication);
        }
    }
}