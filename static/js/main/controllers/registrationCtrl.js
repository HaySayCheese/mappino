'use strict';

app.controller('RegistrationCtrl', function($scope, $rootScope, $timeout, $http, $cookies) {

    /**
     * Стан вікна реєстрації
     **/
    if ($cookies.mcheck != "")
        $rootScope.registrationStatePart = "codeCheck";
    else
        $rootScope.registrationStatePart = "registration";

});


/**
 * Контроллер який відповідає за форму реєстрації
 **/
app.controller('RegistrationUserCtrl', function($scope, $rootScope, $timeout, $http, $cookies) {

    /**
     * Зміннні які відповідають за показ повідомлень при валідації
     **/
    $scope.showValidationMessages   = false;
    $scope.showValidationEmail      = false;
    $scope.showValidationPhone      = false;

    /**
     * Колекція змінних полів
     **/
    $scope.user = {
        name:  "",
        surname:   "",
        email: "",
        phoneNumber: "",
        password:       "",
        passwordRepeat: ""
    };


    /**
     * Фокус першого поля і ініціалізація тултіпів
     **/
    $timeout(function() {
        angular.element("input")[0].focus();

        $("[data-toggle='tooltip']").tooltip({
            container: '.registration-dialog',
            animation: false
        })
    }, 300);


    /**
     * Валідація при вводі даних в поле
     **/
    $scope.$watchCollection("user", function(newValue, oldValue) {
        validatePassword();

        if (newValue.email == "" || !newValue.email) {
            $scope.registrationForm.email.$setValidity("free", true);
            $scope.registrationForm.email.$setValidity("email", true);
        }

        if (newValue.phoneNumber == "" || !newValue.phoneNumber) {
            $scope.registrationForm.phoneNumber.$setValidity("free", true);
            $scope.registrationForm.phoneNumber.$setValidity("phone", true);
            $scope.registrationForm.phoneNumber.$setValidity("code", true);
        }

    });


    /**
     * Валідація пошти при втраті фокуса з поля
     **/
    angular.element("input[name='email']").bind("focusout", function() {
        validateEmail();
    });

    /**
     * Валідація телефона при втраті фокуса з поля
     **/
    angular.element("input[name='phoneNumber']").bind("focusout", function() {
        validatePhoneNumber();
    });


    /**
     * Клік по кнопці реєстрації
     **/
    $scope.submitRegistration = function() {
        $scope.showValidationMessages   = true;
        $scope.showValidationEmail      = true;
        $scope.showValidationPhone      = true;

        validateEmail();
        validatePhoneNumber();

        if ($scope.registrationForm.$valid)
            registerUser();

    };

    /**
     * Логіка валідації пошти
     **/
    function validateEmail() {
        if ($scope.user.email && $scope.user.email != "") {
            $http({
                method: 'POST',
                url: 'ajax/api/accounts/validate-email/',
                headers: {
                    'X-CSRFToken': $cookies.csrftoken
                },
                data: {
                    email: $scope.user.email
                }
            }).success(function(data, status) {

                if (data.code == 0) {
                    $scope.registrationForm.email.$setValidity("free", true);
                    $scope.registrationForm.email.$setValidity("email", true);
                }
                if (data.code == 1) {
                    $scope.registrationForm.email.$setValidity("free", true);
                    $scope.registrationForm.email.$setValidity("email", false);
                }
                if (data.code == 2) {
                    $scope.registrationForm.email.$setValidity("free", false);
                    $scope.registrationForm.email.$setValidity("email", true);
                }

                $scope.showValidationEmail = true;
            });
        } else {
            $scope.registrationForm.email.$setValidity("free", true);
            $scope.registrationForm.email.$setValidity("email", true);
        }
    }

    /**
     * Валідація телефона
     **/
    function validatePhoneNumber() {
        if ($scope.registrationForm.phoneNumber.$valid)
            $http({
                method: 'POST',
                url: 'ajax/api/accounts/validate-phone-number/',
                headers: {
                    'X-CSRFToken': $cookies.csrftoken
                },
                data: {
                    number: $scope.user.phoneNumber
                }
            }).success(function(data, status) {

                if (data.code == 0) {
                    $scope.registrationForm.phoneNumber.$setValidity("free", true);
                    $scope.registrationForm.phoneNumber.$setValidity("phone", true);
                    $scope.registrationForm.phoneNumber.$setValidity("code", true);
                }
                if (data.code == 1) {
                    $scope.registrationForm.phoneNumber.$setValidity("free", true);
                    $scope.registrationForm.phoneNumber.$setValidity("phone", false);
                    $scope.registrationForm.phoneNumber.$setValidity("code", true);
                }
                if (data.code == 2) {
                    $scope.registrationForm.phoneNumber.$setValidity("code", false);
                    $scope.registrationForm.phoneNumber.$setValidity("free", true);
                    $scope.registrationForm.phoneNumber.$setValidity("phone", true);
                }
                if (data.code == 3) {
                    $scope.registrationForm.phoneNumber.$setValidity("free", false);
                    $scope.registrationForm.phoneNumber.$setValidity("phone", true);
                    $scope.registrationForm.phoneNumber.$setValidity("code", true);
                }

                $scope.showValidationPhone = true;
            });
        else {
            $scope.registrationForm.phoneNumber.$setValidity("free", true);
            $scope.registrationForm.phoneNumber.$setValidity("phone", true);
            $scope.registrationForm.phoneNumber.$setValidity("code", true);
        }
    }

    /**
     * Валідація пароля
     **/
    function validatePassword() {
        if ($scope.user.password != $scope.user.passwordRepeat && $scope.user.passwordRepeat.length)
            $scope.registrationForm.passwordRepeat.$setValidity("match", false);
        else
            $scope.registrationForm.passwordRepeat.$setValidity("match", true);
    }

    function registerUser() {
        $http({
            method: 'POST',
            url: 'ajax/api/accounts/registration/',
            headers: {
                'X-CSRFToken': $cookies.csrftoken
            },
            data: {
                'name':             $scope.user.name,
                'surname':          $scope.user.surname,
                'phone-number':     $scope.user.phoneNumber,
                'email':            $scope.user.email,
                'password':         $scope.user.password,
                'password-repeat':  $scope.user.passwordRepeat
            }
        }).success(function() {
            $rootScope.registrationStatePart = "codeCheck";
        })

    }
});


/**
 * Контроллер який відповідає за форму введення коду підтвердження
 **/
app.controller("RegistrationUserCodeCheckCtrl", function($scope, $http, $cookies) {

    $scope.attempts = 0;

    $scope.checkPhoneCode = function() {
        $scope.attempts++;

        $http({
            method: 'POST',
            url: 'ajax/api/accounts/registration/',
            headers: {
                'X-CSRFToken': $cookies.csrftoken
            },
            data: {
                code: $scope.codeCheck
            }
        }).success(function(data, status) {
            $scope.max_attempts = data.max_attempts;

            if (data.code == 1) {
                $scope.incorrectCode = true;
            }
        });
    }

});