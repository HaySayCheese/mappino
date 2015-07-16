module Mappino.Cabinet {

    export function publicationControls(window): angular.IDirective {
        return {
            restrict:'A',

            link: function(scope, element: JQuery, attrs, modelCtrl) {
                var $window = angular.element(window),
                    $element = angular.element(element),
                    $mdCard = angular.element($element.parent().find('md-card')),
                    $mdFirstCard = $mdCard.first(),
                    $mdLastCard = $mdCard.last();

                var width = $mdFirstCard.width() + 'px';


                $element.css({
                    'position': 'fixed',
                    'bottom': 0,
                    'left': $mdFirstCard.offset().left,
                    'z-index': 9999
                });
                $element.css('width', width);
                $mdLastCard.attr('style', 'margin-bottom: 50px !important;');


                $window.on('resize', () => {
                    width = $mdFirstCard.width() + 'px';

                    $element.css({
                        width: width,
                        left: $mdFirstCard.offset().left
                    });

                    if ($window.width() < 800) {
                        $element.css({
                            right: $mdFirstCard.offset().left
                        });
                        $mdLastCard.attr('style', 'margin-bottom: 50px !important;');
                    } else {
                        $element.css({
                            right: 'none'
                        });
                    }
                });
            }
        }
    }


    publicationControls.$inject = [
        '$window'
    ]

}