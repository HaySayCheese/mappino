namespace Mappino.Help {
    import ISidenavService = angular.material.ISidenavService;
    export class HelpController {

        public static $inject = [
            '$scope',
            '$mdSidenav',
            '$mdMedia',
            '$location'
        ];

        constructor(
            private $scope: ng.IScope,
            private $mdSidenav: ISidenavService,
            private $mdMedia: any,
            private $location: any) {
            // -
        }

        public openSidenav() {
            if (!this.$mdMedia('sm')) {
                return;
            }
            this.$mdSidenav('left-sidenav')
                .open();
        }


        public closeSidenav() {
            if (!this.$mdMedia('sm')) {
                return;
            }
            this.$mdSidenav('left-sidenav')
                .close().then(() => {
                //this.$location.move()
            })
        }
        //
        //public toggleSidenav() {
        //    if (!this.$mdMedia('sm')) {
        //        return;
        //    }
        //    this.$mdSidenav('left-sidenav')
        //        .toggle();
        //}
    }
}