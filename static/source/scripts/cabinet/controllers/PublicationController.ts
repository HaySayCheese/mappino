/// <reference path='../_references.ts' />


module pages.cabinet {
    export class PublicationController {

        public static $inject = [
            '$scope',
            '$timeout'
        ];

        constructor(
            private $scope: any,
            private $timeout: angular.ITimeoutService) {
            // -
            $timeout(() => $('select').material_select());

            $scope.publicationTemplateUrl = '/ajax/template/cabinet/publications/unpublished/2/'
        }

    }
}