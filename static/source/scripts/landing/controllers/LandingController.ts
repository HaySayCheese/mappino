namespace Mappino.Landing {
    import IAugmentedJQuery = angular.IAugmentedJQuery;

    export class LandingController {

        public static $inject = [
            '$scope',
            '$mdMedia',
            '$mdSidenav',
            '$location',
            '$rootScope'
        ];

        constructor(private $scope: any,
                    private $mdMedia: any,
                    private $mdSidenav: any,
                    private $location: ng.ILocationService,
                    private $rootScope: any) {
            // ---------------------------------------------------------------------------------------------------------
            $scope.search = {
                realty_type_sid: 0,
                operation_sid: 0,
                period_type_sid: 0,
                date_enter: undefined,
                date_leave: undefined,
                city: '',
                l: ''
            };
            $scope.$watch(() => $mdMedia('sm'), (isSmall) => !isSmall && this.$mdSidenav('left-sidenav').close());
            this.$scope.search.l = "48.455935,34.41285";
            $scope.$watch('search.operation_sid', newValue => {
                if (newValue == 2) {
                    this.$scope.operation_sid = 1;
                    this.$scope.url_part1 = '&b_r_d_min=';
                    this.$scope.url_part2 ='&b_r_d_max=';
                    this.$scope.url_part3 ='&b_pr_sid=0';
                }
                else {
                    this.$scope.operation_sid = this.$scope.search.operation_sid;
                    this.$scope.url_part1 = '';
                    this.$scope.url_part2 = '';

                }
            });
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
                var place: any;
                place = autocomplete.getPlace();
                this.$scope.search.l = autocomplete.getPlace().geometry.location;
                this.$scope.search.city = place.formatted_address;
                this.$scope.search.l = place.geometry.location.lat().toString() + ',' + place.geometry.location.lng().toString();

            });
        }

    }
}