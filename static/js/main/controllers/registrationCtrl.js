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

    var EMAIL_REGEXP = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$/;

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
        validateRegistrationForm();
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
        $scope.showValidationMessages = true;

        if ($scope.registrationForm.$valid)
            $rootScope.registrationStatePart = "codeCheck"
    };

    /**
     * Логіка валідації форми реєстрації
     **/
    function validateRegistrationForm() {
        var form = $scope.user;

        // Валідація мила
        if (form.email && form.email != "") {
            if (!EMAIL_REGEXP.test(form.email)) {
                $scope.registrationForm.email.$setValidity("email", false);
            } else {
                $scope.registrationForm.email.$setValidity("email", true);
            }
        } else {
            $scope.registrationForm.email.$setValidity("email", true);
        }


        // Валідація пароля
        if (form.lastPassword != form.firstPassword && form.lastPassword.length)
            $scope.registrationForm.lastPassword.$setValidity("match", false);
        else
            $scope.registrationForm.lastPassword.$setValidity("match", true);
    }

    /**
     * Логіка валідації пошти
     **/
    function validateEmail() {
        if ($scope.registrationForm.email.$valid)
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

                if (data.code == 0)
                    $scope.registrationForm.email.$setValidity("free", true);
                else
                    $scope.registrationForm.email.$setValidity("free", false);

                $scope.showValidationEmail = true;

            }).error(function(data, status) {
                $scope.registrationForm.email.$setValidity("free", false);
                $scope.showValidationEmail = true;
        });
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

                if (data.code == 0)
                    $scope.registrationForm.phoneNumber.$setValidity("free", true);
                else
                    $scope.registrationForm.phoneNumber.$setValidity("free", false);

                $scope.showValidationPhone = true;

            }).error(function(data, status) {
                $scope.registrationForm.phoneNumber.$setValidity("free", false);
                $scope.showValidationPhone = true;
        });
    }
});


/**
 * Контроллер який відповідає за форму введення коду підтвердження
 **/
app.controller("RegistrationUserCodeCheckCtrl", function($scope, $rootScope, $timeout, $http, $cookies) {

});