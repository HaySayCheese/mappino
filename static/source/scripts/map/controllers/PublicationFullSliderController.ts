
namespace Mappino.Map {
    'use strict';

    export class PublicationFullSliderController {

        public static $inject = [
            '$scope',
            '$rootScope',

            'PublicationService',
        ];

        constructor(
            private $scope,
            private $rootScope,
            private publicationService: PublicationService) {
            // ---------------------------------------------------------------------------------------------------------
            $scope.photos = publicationService.publication.photos;
        }
    }
}