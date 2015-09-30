namespace Mappino.Help {
    export class HelpController {

        public static $inject = [
            '$scope',
            '$mdSidenav',
            '$mdMedia'
        ];

        constructor(
            private $scope: ng.IScope,
            private $mdSidenav: any,
            private $mdMedia: any) {
            // -
        }

        public toggleSidenav() {
            if (!this.$mdMedia('sm')) {
                return;
            }
            this.$mdSidenav('left-sidenav')
                .toggle();
        }
    }
}