namespace Mappino.Help {
    import ISidenavService = angular.material.ISidenavService;
    export class HelpController {

        public static $inject = [
            '$scope',
            '$mdSidenav',
            '$mdMedia',
            '$location',
            '$anchorScroll'
        ];

        constructor(
            private $scope: ng.IScope,
            private $mdSidenav: ISidenavService,
            private $mdMedia: any,
            private $location: ng.ILocationService,
            private $anchorScroll: any) {
            // -
        }

        public openSidenav() {
            if (!this.$mdMedia('sm')) {
                return;
            }
            this.$mdSidenav('left-sidenav')
                .open();
        }


        public closeSidenav(anchor) {
            if (!this.$mdMedia('sm')) {
                return;
            }
            this.$mdSidenav('left-sidenav')
                .close().then(() => {
                this.moveToAnchor(anchor)
            })
        }


        public moveToAnchor(anchor) {
            this.$location.hash(anchor);
            this.$anchorScroll();
        }

    }
}