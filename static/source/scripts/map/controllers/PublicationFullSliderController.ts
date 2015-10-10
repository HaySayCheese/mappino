
namespace Mappino.Map {
    'use strict';

    export class PublicationFullSliderController {

        public static $inject = [
            '$scope',
            '$rootScope',
            '$mdDialog',
            'PublicationPreviewService',
        ];

        constructor(
            private $scope,
            private $rootScope,
            private $mdDialog: any,
            private publicationPreviewService: Mappino.Core.PublicationPreview.PublicationPreviewService) {
            // ---------------------------------------------------------------------------------------------------------
            $scope.publicationFullSliderIndex = 0;

            $scope.photos = publicationPreviewService.publication.photos;
        }


        public close() {
            this.$scope.photos = [];
            this.$mdDialog.cancel();
        }



        public prevSlide() {
            this.$scope.publicationFullSliderIndex -= 1;
        }

        public nextSlide() {
            this.$scope.publicationFullSliderIndex += 1;
        }

        public toggleSlide($event) {
            if ($event.keyCode == 37 && this.$scope.publicationFullSliderIndex != 0) {
                this.prevSlide();
            }

            if ($event.keyCode == 39 && this.$scope.publicationFullSliderIndex != this.$scope.photos.length - 1) {
                this.nextSlide();
            }
        }
    }
}