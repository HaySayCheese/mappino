namespace Mappino.Landing {
    import IAugmentedJQuery = angular.IAugmentedJQuery;
    import ITimeoutService = angular.ITimeoutService;

    export class LandingController {

        public static $inject = [
            '$scope',
            '$mdMedia',
            '$mdSidenav',
            '$location',
            '$rootScope',
            '$timeout',
            'BAuthService',
            '$cookies'
        ];

        constructor(private $scope: any,
                    private $mdMedia: any,
                    private $mdSidenav: any,
                    private $location: ng.ILocationService,
                    private $rootScope: any,
                    private $timeout: ITimeoutService,
                    private bAuthService: Mappino.Core.BAuth.BAuthService,
                    private $cookies: ng.cookies.ICookiesService) {
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

            $scope.authState = 'enterPhone';

            this.initUserData();

            $scope.$watch(() => $mdMedia('sm'), (isSmall) => !isSmall && this.$mdSidenav('left-sidenav').close());
            this.initAutocomplete(document.getElementById('landing-autucomplete'));
        }



        public scrollToTop() {
            this.$timeout(() => {
                angular.element('html,body').animate({
                    scrollTop: 0
                }, 'slow');
            }, 50);
        }

        public scrollToLoginForm() {
            this.$timeout(() => {
                angular.element('html,body').animate({
                    scrollTop: 700
                }, 'slow');
                this.toggleLoginForm();
            }, 50);

        }

        public search() {
            if (this.$scope.search.city.length) {
                this.$scope.zoom = '&z=15';
                this.$scope.lat_lng = '&l=' + this.$scope.search.l;
            }
            else {
                this.$scope.zoom = '';
                this.$scope.lat_lng = '';

            }
            if (this.$scope.search.operation_sid == 2) {
                this.$scope.operation_sid = 1;
                this.$scope.url_date_enter = '&b_r_d_min=' + this.$scope.search.date_enter;
                this.$scope.url_date_leave ='&b_r_d_max=' + this.$scope.search.date_leave;
                this.$scope.url_pr_sid ='&b_pr_sid=0';
            }
            else {
                this.$scope.operation_sid = this.$scope.search.operation_sid;
                this.$scope.url_date_enter = '';
                this.$scope.url_date_leave ='';
                this.$scope.url_pr_sid ='&b_pr_sid=1';

            }
        }



        public toggleSidenav() {
            if (!this.$mdMedia('sm')) {
                return;
            }
            this.$mdSidenav('left-sidenav').toggle();
        }







        public login() {
            if (this.$scope.authState === 'enterPhone') {
                if (this.$scope.loginForm.mobilePhone.$valid) {
                    this.bAuthService.checkPhoneNumber(this.$scope.account.mobileCode, this.$scope.account.mobilePhone)
                        .success(response => {
                            if (response.code == 10) {
                                window.location.pathname = '/cabinet/';
                            } else if (response.code == 1) {
                                this.$scope.loginForm.mobilePhone.$setValidity('invalid', false);
                            } else if (response.code == 200) {
                                this.$scope.loginForm.mobilePhone.$setValidity('throttled', false);
                            } else {
                                localStorage.setItem('mobile_code', this.$scope.account.mobileCode);
                                localStorage.setItem('mobile_phone', this.$scope.account.mobilePhone);

                                this.$scope.authState = 'enterSMSCode';
                            }
                        })
                        .error(response => {
                            this.$scope.loginForm.mobilePhone.$setValidity('invalid', false);
                        });
                }
            } else {
                if (this.$scope.loginForm.smsCode.$valid) {
                    this.bAuthService.checkSMSCode(this.$scope.account.mobileCode, this.$scope.account.mobilePhone, this.$scope.account.smsCode)
                        .success(response => {
                            if (response.code == 0) {
                                this.clearUserData();
                                window.location.pathname = '/cabinet/';

                            } else {
                                this.$scope.loginForm.smsCode.$setValidity('invalid', false);
                            }
                        })
                        .error(response => {
                            this.$scope.loginForm.smsCode.$setValidity('invalid', false);
                        });
                }
            }
        }



        public toggleLoginForm() {
            if (this.$cookies.get('sessionid')) {
                window.location.pathname = '/cabinet/';
            } else {
                this.$scope.showLoginForm = true;
            }
        }


        public returnToEnterPhoneState() {
            this.$cookies.remove("mcheck");
            this.clearUserData();
            this.resetLoginForm();
            this.$scope.authState = 'enterPhone';
        }

        private resetLoginForm() {
            if (this.$scope.authState == 'enterPhone') {
                if (angular.isDefined(this.$scope.loginForm.mobilePhone))
                    this.$scope.loginForm.mobilePhone.$setValidity('invalid', true);
                this.$scope.loginForm.mobilePhone.$setValidity('throttled', true);
            } else {
                if (angular.isDefined(this.$scope.loginForm.smsCode))
                    this.$scope.loginForm.smsCode.$setValidity('invalid', true);
            }

            this.$scope.loginForm.$setPristine();
        }

        private changeAuthState() {
            this.$scope.authState = this.$cookies.get('mcheck') ? 'enterSMSCode' : 'enterPhone';
        }



        private initUserData() {
            this.$scope.account = {
                mobileCode:     localStorage.getItem('mobile_code')     || '+380',
                mobilePhone:    localStorage.getItem('mobile_phone')    || '',
                smsCode:        ''
            };
        }



        private clearUserData() {
            this.$scope.account = {
                mobileCode:     '+380',
                mobilePhone:    '',
                smsCode:        ''
            };

            localStorage.removeItem('mobile_code');
            localStorage.removeItem('mobile_phone');
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