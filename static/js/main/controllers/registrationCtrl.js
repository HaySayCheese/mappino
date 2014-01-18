'use strict';

app.controller('RegistrationCtrl', function($scope, $rootScope, $timeout, $http, $cookieStore) {

    /**
     * Стан вікна реєстрації
     **/
    if ($cookieStore.get("mcheck"))
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
//        validatePassword();
//
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

        validateEmail();

    });


    /**
     * Валідація пошти при втраті фокуса з поля
     **/
    angular.element("input[name='email']").bind("focusout", function() {
        sendEmailToValidate();
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
//        $scope.showValidationMessages   = true;
//        $scope.showValidationEmail      = true;
//        $scope.showValidationPhone      = true;
//
//        validateEmail();
//        validatePhoneNumber();
//
//        if ($scope.registrationForm.$valid)
//            registerUser();

    };

    /**
     * Логіка валідації пошти
     **/
    function validateEmail() {

        if (arguments[0])
            var code = arguments[0];

        if (!$scope.user.email && $scope.user.email === "")
            return;

        $scope.registrationForm.email.$setValidity("free", true);
        $scope.registrationForm.email.$setValidity("email", true);

        $scope.registrationForm.email.$setValidity("isOk", false);

        if (code === 0)
            $scope.registrationForm.email.$setValidity("free", true);


        if (code === 1)
            $scope.registrationForm.email.$setValidity("email", false);


        if (code === 2)
            $scope.registrationForm.email.$setValidity("free", false);


        $scope.showValidationEmail = true;
    }


    function sendEmailToValidate() {

        if (!$scope.user.email || $scope.user.email === "")
            return;

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

            validateEmail(data.code);

            if (data.code === 0)
                $scope.registrationForm.email.$setValidity("isOk", true);
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
app.controller("RegistrationUserCodeCheckCtrl", function($scope, $http, $cookies, $timeout, $rootScope) {

    $scope.codeCheck = "";

    var attempt, max_attempts;

    /**
     * Фокус першого поля
     **/
    $timeout(function() {
        angular.element("input")[0].focus();
    }, 300);

    $scope.checkPhoneCode = function() {

        if (attempt && (attempt == max_attempts))
            $rootScope.registrationStatePart = "registration";

        if ($scope.codeCheck && $scope.codeCheck != "") {
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
                    attempt = data.attempts;
                    max_attempts = data.max_attempts;

                    var tooltip = $("[data-toggle='tooltip']");

                    tooltip.tooltip('destroy');
                    tooltip.tooltip({
                        container: '.registration-dialog',
                        animation: false,
                        title: "Некоректний код. Попитка " +  data.attempts + " из " +  data.max_attempts + "."
                    });

                if (data.code == 0) {
                    $('.registration-dialog').parent().modal('hide');
                }
                if (data.code == 1) {
                    $scope.incorrectCode = true;
                }
            });
        } else {
            var tooltip = $("[data-toggle='tooltip']");

            tooltip.tooltip('destroy');
            tooltip.tooltip({
                container: '.registration-dialog',
                animation: false,
                title: "Обовязкове поле."
            });

            $scope.incorrectCode = true;
        }
    }

});