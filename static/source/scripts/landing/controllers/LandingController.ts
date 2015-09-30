namespace Mappino.Landing {
    import IAugmentedJQuery = angular.IAugmentedJQuery;

    export class LandingController {

        public static $inject = [
            '$scope',
            '$mdMedia',
            '$mdSidenav'
        ];

        constructor(private $scope: any,
                    private $mdMedia: any,
                    private $mdSidenav: any) {
            // ---------------------------------------------------------------------------------------------------------
            $scope.search = {
                realty_type_sid: 0,
                operation_sid: 0,
                period_type_sid: 0,
                date_enter: undefined,
                date_leave: undefined,
                city: ''
            };

            $scope.$watch(() => $mdMedia('sm'), (isSmall) => !isSmall && this.$mdSidenav('left-sidenav').close());

            this.initAutocomplete(document.getElementById('landing-autucomplete'));
        }



        public toggleSidenav() {
            if (!this.$mdMedia('sm')) {
                return;
            }
            this.$mdSidenav('left-sidenav').toggle();
        }



        private initAutocomplete(element: HTMLElement) {
            var autocomplete = new google.maps.places.Autocomplete(<HTMLInputElement>element, {
                componentRestrictions: {
                    country: "ua"
                }
            });

            google.maps.event.addListener(autocomplete, 'place_changed', () => {
                this.$scope.search.city = autocomplete.getPlace().formatted_address
            });
        }
    }
}