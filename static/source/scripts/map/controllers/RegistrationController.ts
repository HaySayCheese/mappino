/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class RegistrationController {
        public static $inject = [
            '$scope',
            'AuthService'
        ];

        constructor(private $scope,
                    private authService: bModules.Auth.IAuthService) {
            // ---------------------------------------------------------------------------------------------------------
            $scope.registration = {};
            $scope.registration.user = {
                firstName:      '',
                lastName:       '',
                email:          '',
                phoneNumber:    '',
                password:       '',
                passwordRepeat: ''
            };

            $scope.validationInProggress = false;

            this.initWatchers();
        }



        private registration() {
            var user = this.$scope.registration.user;

            // check if passwords match
            this.$scope.registrationForm.userPasswordRepeat.$setValidity('passwordsNotMatch',
                !(this.$scope.registration.user.password != this.$scope.registration.user.passwordRepeat));


            if (this.$scope.registrationForm.$valid && !this.$scope.validationInProggress) {
                this.authService.registration(user, () => {

                }, (response) => {
                    console.log(response)

                });
            }
        }



        private initWatchers() {
            // check email on blur
            angular.element("form[name='registrationForm'] input[name='userEmail']").on('blur', (el) => {
                if (!_.isEmpty(this.$scope.registration.user.email)) {
                    this.$scope.validationInProggress = true;

                    this.authService.validateEmail(this.$scope.registration.user.email, () => {
                        this.$scope.validationInProggress = false;

                        this.$scope.registrationForm.userEmail.$setValidity('emailIncorrect', true);
                        this.$scope.registrationForm.userEmail.$setValidity('emailIsUsed', true);
                    }, (response) => {
                        this.$scope.validationInProggress = false;

                        this.$scope.registrationForm.userEmail.$setValidity('emailIncorrect', response.code !== 1);
                        this.$scope.registrationForm.userEmail.$setValidity('emailIsUsed', response.code !== 2);
                    })
                }
            });


            // check phone number on blur
            angular.element("form[name='registrationForm'] input[name='userPhone']").on('blur', (el) => {
                if (!_.isEmpty(this.$scope.registration.user.phoneNumber)) {
                    this.$scope.validationInProggress = true;

                    this.authService.validatePhoneNumber(this.$scope.registration.user.phoneNumber, () => {
                        this.$scope.validationInProggress = false;

                        this.$scope.registrationForm.userPhone.$setValidity('phoneNumberIncorrect', true);
                        this.$scope.registrationForm.userPhone.$setValidity('phoneNumberIsUsed', true);
                        this.$scope.registrationForm.userPhone.$setValidity('phoneCodeIncorrect', true);

                    }, (response) => {
                        this.$scope.validationInProggress = false;

                        this.$scope.registrationForm.userPhone.$setValidity('phoneNumberIncorrect', response.code !== 1);
                        this.$scope.registrationForm.userPhone.$setValidity('phoneCodeIncorrect', response.code !== 2);
                        this.$scope.registrationForm.userPhone.$setValidity('phoneNumberIsUsed', response.code !== 3);
                    })
                }
            });


            // reset password match error on edit
            this.$scope.$watchGroup(['registration.user.password', 'registration.user.passwordRepeat'], () => {
                this.$scope.registrationForm.userPasswordRepeat.$setValidity('passwordsNotMatch', true);
            });
        }
    }
}