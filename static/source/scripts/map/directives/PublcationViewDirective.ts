module pages.map {
    export function PublcationViewDirective(
        navbarsHandler: NavbarsHandler,
        publicationHandler: PublicationHandler): angular.IDirective {

        return {
            restrict: 'E',
            replace: true,
            controller: PublicationController,
            controllerAs: 'pubCtrl',
            templateUrl: '/ajax/template/map/publication/view/',

            link: function(scope, element, attrs, modelCtrl) {
                angular.element(element).addClass('md-whiteframe-z3');


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
    }

    PublcationViewDirective.$inject = ['NavbarsHandler', 'PublicationHandler'];
}