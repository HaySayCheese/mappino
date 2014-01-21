'use strict';

app.controller('RestoreAccessCtrl', function($scope, $rootScope, $location) {

    /**
     * Стан вікна восстановлення пароля
     **/
    //$rootScope.restoreAccessStatePart = "sendEmail";

    if ($location.search().token)
        $rootScope.restoreAccessStatePart = "changePassword";
    else
        $rootScope.restoreAccessStatePart = "sendEmail";

});



app.controller('RestoreAccessSendMailCtrl', function($scope, $rootScope, $timeout, $http, authorizationQueries) {

    /**
     * Змінні
     **/
    $scope.showValidationMessages = false;

    $scope.user = {
        login: ""
    };


    /**
     * Фокус першого поля і ініціалізація тултіпів
     **/
    $timeout(function() {
        angular.element("input")[0].focus();

        $("[data-toggle='tooltip']").tooltip({
            container: '.restore-access-dialog',
            animation: false
        });
    }, 300);


    /**
     * Валідація логіна при вводі даних в поле
     **/
    $scope.$watch("user.login", function(newValue, oldValue) {
        if (oldValue !== newValue)
            validateLogin();
    });


    /**
     * Клік по кнопці відправки пошти
     **/
    $scope.submitSendEmail = function() {
        $scope.showValidationMessages = true;

        if (!$scope.user.login || $scope.user.login === "")
            return;

        var sendBtn = $(".restore-access-dialog .btn-success");
        sendBtn.button('loading');

        authorizationQueries.restoreAccessSendEmail($scope.user.login).success(function(data) {
            console.log(data);
            sendBtn.button('reset');

            validateLogin(data.code)
        });
    };


    function validateLogin() {

        if (arguments[0])
            var code = arguments[0];

        if (!$scope.user.login && $scope.user.login === "")
            return;

        $scope.restoreAccessForm.login.$setValidity("login", true);
        $scope.restoreAccessForm.login.$setValidity("tokenInvalid", true);
        $scope.restoreAccessForm.login.$setValidity("token", true);


        if (code === 0) {
            $rootScope.restoreAccessStatePart = "emailSendMessage";
        }

        if (code === 3) {
            $scope.restoreAccessForm.login.$setValidity("login", false);
            $scope.restoreAccessForm.login.$setValidity("tokenInvalid", true);
            $scope.restoreAccessForm.login.$setValidity("token", true);
        }

        if (code === 7) {
            $rootScope.restoreAccessStatePart = "invalidToken";
        }

        if (code === 8) {
            $scope.restoreAccessForm.login.$setValidity("login", true);
            $scope.restoreAccessForm.login.$setValidity("tokenInvalid", true);
            $scope.restoreAccessForm.login.$setValidity("token", false);
        }

    }

});



app.controller('RestoreAccessChangePasswordCtrl', function($scope, $timeout, $http) {

    /**
     * Змінні
     **/
    $scope.showValidationMessages = false;

    $scope.user = {
        password: "",
        passwordRepeat: ""
    };


    /**
     * Фокус першого поля і ініціалізація тултіпів
     **/
    $timeout(function() {
        angular.element("input")[0].focus();

        $("[data-toggle='tooltip']").tooltip({
            container: '.restore-access-dialog',
            animation: false
        });
    }, 300);


    /**
     * Виклик валідації пароля при введенні
     **/
    $scope.$watchCollection("user", function() {
        validatePasswords();
    });



    /**
     * Клік по кнопці зміни пароля
     **/
    $scope.submitChangePassword = function() {
        $scope.showValidationMessages = true;

        validatePasswords();
    };


    /**
     * Валідація пароля
     **/
    function validatePasswords() {

        if (!$scope.user.passwordRepeat || $scope.user.passwordRepeat === "")
            return;

        if ($scope.user.password !== $scope.user.passwordRepeat) {
            $scope.restoreAccessForm.passwordRepeat.$setValidity("passwords", false)
        } else {
            $scope.restoreAccessForm.passwordRepeat.$setValidity("passwords", true)
        }

    }

});