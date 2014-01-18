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

    $scope.validated = {
        email: false,
        phone: false
    };

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

    $scope.$watchCollection("user", function() {
        validatePassword();
    });

    /**
     * Валідація пошти при вводі даних в поле
     **/
    $scope.$watch("user.email", function(newValue, oldValue) {
        if (oldValue !== newValue)
            validateEmail();
    });

    /**
     * Валідація телефона при вводі даних в поле
     **/
    $scope.$watch("user.phoneNumber", function(newValue, oldValue) {
        if (oldValue !== newValue)
            validatePhone();
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
        sendPhoneToValidate();
    });


    /**
     * Клік по кнопці реєстрації
     **/
    $scope.submitRegistration = function() {
        $scope.showValidationMessages   = true;
        $scope.showValidationEmail      = true;
        $scope.showValidationPhone      = true;

        if (!$scope.validated.email)
            sendEmailToValidate();

        if (!$scope.validated.phone)
            sendPhoneToValidate();

        if ($scope.registrationForm.$valid)
            registerUser();
    };

    /**
     * Логіка валідації пошти
     **/
    function validateEmail() {

        $scope.registrationForm.email.$setValidity("free", true);
        $scope.registrationForm.email.$setValidity("email", true);

        $scope.registrationForm.email.$setValidity("isOk", false);

        if (arguments[0])
            var code = arguments[0];

        if (!$scope.user.email && $scope.user.email === "")
            return;


        if (code === 0)
            $scope.registrationForm.email.$setValidity("free", true);


        if (code === 1)
            $scope.registrationForm.email.$setValidity("email", false);


        if (code === 2)
            $scope.registrationForm.email.$setValidity("free", false);


        $scope.showValidationEmail = true;
    }

    /**
     * Відправка пошти на валідацію
     **/
    function sendEmailToValidate() {

        $scope.registrationForm.email.$setValidity("isOk", false);

        if (!$scope.user.email || $scope.user.email === "")
            return;

        $scope.validated.email = false;

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

            if (data.code === 0) {
                $scope.registrationForm.email.$setValidity("isOk", true);

                $scope.validated.email = true;
            }
        });

    }

    /**
     * Логіка валідація телефона
     **/
    function validatePhone() {

        $scope.registrationForm.phoneNumber.$setValidity("free", true);
        $scope.registrationForm.phoneNumber.$setValidity("phone", true);
        $scope.registrationForm.phoneNumber.$setValidity("code", true);

        $scope.registrationForm.phoneNumber.$setValidity("isOk", false);

        if (arguments[0])
            var code = arguments[0];

        if (!$scope.user.phoneNumber && $scope.user.phoneNumber === "")
            return;


        if (code === 0)
            $scope.registrationForm.phoneNumber.$setValidity("free", true);


        if (code === 1)
            $scope.registrationForm.phoneNumber.$setValidity("phone", false);


        if (code === 2)
            $scope.registrationForm.phoneNumber.$setValidity("code", false);


        if (code === 3)
            $scope.registrationForm.phoneNumber.$setValidity("free", false);


        $scope.showValidationPhone = true;
    }

    /**
     * Відправка телефона на валідацію
     **/
    function sendPhoneToValidate() {

        $scope.registrationForm.phoneNumber.$setValidity("isOk", false);

        if (!$scope.user.phoneNumber || $scope.user.phoneNumber === "")
            return;

        $scope.validated.phone = false;

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

            validatePhone(data.code);

            if (data.code === 0) {
                $scope.registrationForm.phoneNumber.$setValidity("isOk", true);

                $scope.validated.phone = true;
            }
        });
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


    /**
     * Функція відправки введених даних
     **/
    function registerUser() {

        var registrationBtn = $(".registration-dialog .btn-success");

        registrationBtn.button('loading');

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
            registrationBtn.button('reset');

            $rootScope.registrationStatePart = "codeCheck";
        });
    }
});




/**
 * Контроллер який відповідає за форму введення коду підтвердження
 **/
app.controller("RegistrationUserCodeCheckCtrl", function($scope, $http, $cookies, $timeout, $rootScope) {

    $scope.codeCheck = "";

    var attempt,
        max_attempts,
        registrationBtn = $(".registration-dialog .btn-success");

    /**
     * Фокус першого поля
     **/
    $timeout(function() {
        angular.element("input")[0].focus();
    }, 300);


    /**
     * Функція відправки кода на перевірку
     **/
    $scope.checkPhoneCode = function() {

        if (!$scope.codeCheck || $scope.codeCheck === "") {
            var tooltip = $("[data-toggle='tooltip']");

            tooltip.tooltip('destroy');
            tooltip.tooltip({
                container: '.registration-dialog',
                animation: false,
                title: "Обязательное поле"
            });

            $scope.incorrectCode = true;

            return;
        }

        registrationBtn.button('loading');

        sendCodeToValidate();
    };

    /**
     * Відправка кода на валідацію
     **/
    function sendCodeToValidate() {
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

           registrationBtn.button('reset');

           attempt = data.attempts;
           max_attempts = data.max_attempts;

           validateAttempts(data.code);
        });
    }

    /**
     * Валідація спроб вводу кода
     **/
    function validateAttempts() {

        if (arguments[0])
            var code = arguments[0];

        if (attempt && (attempt - 1 === max_attempts))
            $rootScope.registrationStatePart = "registration";

        var tooltip = $("[data-toggle='tooltip']");

        tooltip.tooltip('destroy');
        tooltip.tooltip({
            container: '.registration-dialog',
            animation: false,
            title: "Некоректний код. Попитка " +  attempt + " из " +  max_attempts + "."
        });

        if (code == 0) {
            $('.registration-dialog').parent().modal('hide');
        }

        if (code == 1) {
            $scope.incorrectCode = true;
        }
    }

});