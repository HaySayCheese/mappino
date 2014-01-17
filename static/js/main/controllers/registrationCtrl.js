'use strict';

app.controller('RegistrationCtrl', function($scope, $rootScope, $timeout, $http, $cookies) {

    /**
     * Стан вікна реєстрації
     **/
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
        firstName:  "",
        lastName:   "",

        email: "",

        phoneNumber: "",

        firstPassword: "",
        lastPassword:  ""
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

//        if (newValue.email == "" || !newValue.email) {
//            $scope.registrationForm.email.$setValidity("free", true);
//            $scope.registrationForm.email.$setValidity("email", true);
//        }
//
//        if (newValue.phoneNumber == "" || !newValue.phoneNumber) {
//            $scope.registrationForm.phoneNumber.$setValidity("free", true);
//            $scope.registrationForm.phoneNumber.$setValidity("phone", true);
//            $scope.registrationForm.phoneNumber.$setValidity("code", true);
//        }

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

        if ($scope.registrationForm.$valid)
            $rootScope.registrationStatePart = "codeCheck";

        validateEmail();
        validatePhoneNumber();
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

                console.log("free- " + $scope.registrationForm.email.$error.free)
                console.log("email- " + $scope.registrationForm.email.$error.email)

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
        if ($scope.user.lastPassword != $scope.user.firstPassword && $scope.user.lastPassword.length)
            $scope.registrationForm.lastPassword.$setValidity("match", false);
        else
            $scope.registrationForm.lastPassword.$setValidity("match", true);
    }
});


/**
 * Контроллер який відповідає за форму введення коду підтвердження
 **/
app.controller("RegistrationUserCodeCheckCtrl", function($scope, $rootScope, $timeout, $http, $cookies) {

});