/// <reference path='../_all.ts' />


module Mappino.Cabinet {
    export class PublicationController {
        private _publication: Object = {};

        public static $inject = [
            '$scope',
            '$state',
        ];

        constructor(private $scope: any,
                    private $state: angular.ui.IStateService) {
            // ---------------------------------------------------------------------------------------------------------
            this._publication['tid'] = $state.params['id'].split(':')[0];
            this._publication['hid'] = $state.params['id'].split(':')[1];

            $scope.publicationTemplateUrl = '/ajax/template/cabinet/publications/unpublished/' + this._publication['tid'] + '/';
        }
    }
}