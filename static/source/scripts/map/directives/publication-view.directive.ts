namespace Mappino.Map {
    export function PublcationViewDirective($rootScope, $stateParams): angular.IDirective {

        return {
            restrict: 'E',
            controller: PublicationController,
            controllerAs: 'pubCtrl',
            templateUrl: '/ajax/template/map/publication/view/',

            link: function(scope, element, attrs, modelCtrl) {
                var $element = angular.element(element);

                $element.addClass('md-whiteframe-z3');


                if ($stateParams['publication_id'] == 0) {
                    close($element)
                } else {
                    if ($stateParams['navbar_right'] == 0) {
                        open($element, false)
                    } else {
                        open($element, true)
                    }
                }

                $rootScope.$on('$stateChangeSuccess', () => {
                    if ($stateParams['publication_id'] == 0) {
                        close($element)
                    } else {
                        if ($stateParams['navbar_right'] == 0) {
                            open($element, false)
                        } else {
                            open($element, true)
                        }
                    }
                });
            }
        };


        function open($element, with_navbar_right) {
            if (!$element.hasClass('-opened') || !$element.hasClass('-with-navbar-right')) {
                if (with_navbar_right && with_navbar_right == true) {
                    $element.removeClass('-closed -opened').addClass('-with-navbar-right');
                } else {
                    $element.removeClass('-closed -with-navbar-right').addClass('-opened');
                }

            }
        }

        function close($element) {
            if (!$element.hasClass('-closed') || !$element.hasClass('-with-navbar-right')) {
                $element.removeClass('-opened -with-navbar-right').addClass('-closed');
            }
        }
    }

    PublcationViewDirective.$inject = ['$rootScope', '$stateParams'];
}