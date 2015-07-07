module pages.map {
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


                //if (publicationHandler.isOpened()) {
                //    if (navbarsHandler.isOpened('navbar_right')) {
                //        openPublicationWithNavbarRight();
                //    } else {
                //        openPublication();
                //    }
                //} else {
                //    closePublication();
                //}
                //
                //
                //
                //
                //scope.$on('PublicationHandler.Open', openPublication);
                //scope.$on('PublicationHandler.OpenWithNavbarRight', openPublicationWithNavbarRight);
                //scope.$on('PublicationHandler.Close', closePublication);
                //
                //
                //var openPublication = () => {
                //    angular.element(element)
                //        .removeClass('-closed')
                //        .removeClass('-with-navbar-right')
                //        .addClass('-opened');
                //    console.log('opened')
                //
                //};
                //
                //
                //var openPublicationWithNavbarRight = () => {
                //    angular.element(element)
                //        .removeClass('-opened')
                //        .removeClass('-closed')
                //        .addClass('-with-navbar-right');
                //
                //    console.log('with')
                //};
                //
                //
                //var closePublication = () => {
                //    angular.element(element)
                //        .removeClass('-opened')
                //        .removeClass('-with-navbar-right')
                //        .addClass('-closed');
                //    console.log('closed')
                //
                //};

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