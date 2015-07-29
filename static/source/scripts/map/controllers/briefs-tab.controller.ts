/// <reference path='../_all.ts' />


module Mappino.Map {
    'use strict';

    export class BriefsTabController {
        public static $inject = [
            '$scope',
            '$rootScope',
            'PublicationHandler',
            'BriefsService'
        ];

        constructor(private $scope,
                    private $rootScope: any,
                    private publicationHandler: PublicationHandler,
                    private briefsService: BriefsService) {
            // ---------------------------------------------------------------------------------------------------------
            //this.publicationHandler = PublicationHandler;

            $scope.briefs = briefsService.briefs;

            $scope.$watchCollection('briefs', (newValue) => {
                console.log(newValue)
            });
        }



        public onBriefMouseOver(brief) {
            this.$rootScope.$broadcast('Mappino.Map.BriefsService.BriefMouseOver', brief.id);
        }
    }
}