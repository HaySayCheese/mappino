namespace Mappino.Map {
    export function PublicationPhotosSliderDirective(): angular.IDirective {
        return {
            restrict: 'E',
            controller: NavbarRightController,
            controllerAs: 'navCtrl',
            templateUrl: '/ajax/template/map/navbar-right/',

            link: function(scope, element, attrs, modelCtrl) {
                var $element        = angular.element(element),
                    $elementToggleButton = angular.element('[publication-photos-slider-toggle-button]'),
                    $overlayElement = '<div class="publication-photos-slider-overlay"></div>',
                    $overlay        = angular.element('.publication-photos-slider-overlay');

                angular.element('body').append($overlayElement);

                $elementToggleButton.on('click', () => togglePublicationPhotosSlider($element, $overlay))
            }
        };



        function togglePublicationPhotosSlider($element: angular.IAugmentedJQuery, $overlay: angular.IAugmentedJQuery) {
            if ($overlay.hasClass('-opened')) {
                $overlay.removeClass('-opened')
            } else {
                $overlay.addClass('-opened')
            }
        }
    }

    PublicationPhotosSliderDirective.$inject = [];
}