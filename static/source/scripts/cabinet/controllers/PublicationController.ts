/// <reference path='../_references.ts' />


module pages.cabinet {
    export class PublicationController {
        private _publication: Object = {

        };

        public static $inject = [
            '$scope',
            '$rootScope',
            '$timeout',
            '$state',
            'CurrencyTypesService',
            'PeriodTypesService',
            'PublicationsService',
        ];

        constructor(
            private $scope: any,
            private $rootScope: any,
            private $timeout: angular.ITimeoutService,
            private $state: angular.ui.IStateService,

            private currencyTypesService: bModules.Types.CurrencyTypesService,
            private periodTypesService: bModules.Types.PeriodTypesService,

            private publicationsService: PublicationsService) {
            // ---------------------------------------------------------------------------------------------------------
            this._publication['tid']    = $state.params['id'].split(':')[0];
            this._publication['hid']    = $state.params['id'].split(':')[1];

            $scope.currencyTypes    = currencyTypesService.currency_types;
            $scope.periodTypes      = periodTypesService.period_types;

            $scope.publication = {};

            $scope.publicationTemplateUrl = '/ajax/template/cabinet/publications/unpublished/' + this._publication['tid'] + '/';

            this.loadPublicationData();
        }



        private loadPublicationData() {
            this.$rootScope.loaders.base = true;

            this.publicationsService.loadPublication(this._publication, (response) => {
                this.$scope.publication = response;
                this.$rootScope.loaders.base = false;
            });
        }
    }
}