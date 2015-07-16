module Mappino.Cabinet {

    export function publicationControls(window): angular.IDirective {
        return {
            restrict:'A',

            link: function(scope, element: JQuery, attrs, modelCtrl) {
                var $window         = angular.element(window),
                    $main           = angular.element('main'),
                    $uiView         = $main.find('[ui-view]'),
                    $element        = angular.element(element),
                    $mdCard         = angular.element($element.parent().find('md-card')),
                    $mdFirstCard    = $mdCard.first(),
                    $mdLastCard     = $mdCard.last(),

                    scrollBottom                = $uiView.height() - ($main.height() + $main.scrollTop()),
                    mdLastCardBottomMargin      = $window.width() < 800 ? $element.height() : 24 + $element.height(),
                    elementStartFixedPosition   = $window.width() < 800 ? 20 : 43;



                $mdLastCard.attr('style', 'margin-bottom:' + mdLastCardBottomMargin + 'px !important;');

                $element.css({
                    'width':    $mdFirstCard.width() + 'px',
                    'position': 'fixed',
                    'bottom':   0,
                    'left':     $mdFirstCard.offset().left,
                    'z-index':  9999
                });


                scrollBottom >= elementStartFixedPosition ? $element.addClass('-fixed') : $element.removeClass('-fixed');


                $window.on('resize', () => {
                    scrollBottom                = $uiView.height() - ($main.height() + $main.scrollTop())
                    mdLastCardBottomMargin      = $window.width() < 800 ? $element.height() : 24 + $element.height();
                    elementStartFixedPosition   = $window.width() < 800 ? 20 : 43;

                    $element.css({
                        width: $mdFirstCard.width() + 'px',
                        left: $mdFirstCard.offset().left
                    });

                    scrollBottom >= elementStartFixedPosition ? $element.addClass('-fixed') : $element.removeClass('-fixed');

                    if ($window.width() < 800) {
                        $element.css({
                            right: $mdFirstCard.offset().left
                        });

                        $mdLastCard.attr('style', 'margin-bottom:' + mdLastCardBottomMargin + 'px !important;');
                    } else {
                        $element.css({
                            right: 'none'
                        });
                    }
                });



                $main.scroll(() => {
                    scrollBottom = $uiView.height() - ($main.height() + $main.scrollTop());

                    scrollBottom >= elementStartFixedPosition ? $element.addClass('-fixed') : $element.removeClass('-fixed');
                });
            }
        };
    }


    publicationControls.$inject = [
        '$window',
    ]

}