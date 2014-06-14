'use strict';

app.controller('RestoreAccessCtrl', function($scope, $rootScope, $location) {

    angular.element(".restore-access-modal").modal();

    /**
     * Стан вікна восстановлення пароля
     **/
    $rootScope.restoreAccessStatePart = "sendEmail";

    if ($location.search().token)
        $rootScope.restoreAccessStatePart = "changePassword";

});





/**
 * Контроллер який відповідає відправку мила юзеру
 **/
app.controller('RestoreAccessSendMailCtrl', function($scope, $rootScope, Account) {

    /**
     * Змінні
     **/
    $scope.showValidationMessages = false;

    $scope.user = {
        login: ""
    };

    var restoreAccessModal = angular.element(".restore-access-modal"),
        restoreAccessBtn   = restoreAccessModal.find(".btn-success"),
        tooltip            = restoreAccessModal.find("[data-toggle='tooltip']");


    /**
     * Ініціалізація тултіпів
     **/
    restoreAccessModal.on("shown.bs.modal", function() {
        tooltip.tooltip({
            container: restoreAccessModal.find(".modal-dialog"),
            animation: false
        });
    });


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

        restoreAccessBtn.button('loading');

        Account.restoreAccessSendEmail($scope.user.login, function(data) {
            restoreAccessBtn.button('reset');

            if (data.code === 0) {
                $rootScope.restoreAccessStatePart = "emailSendMessage";

                return
            }

            validateLogin(data.code);
        });
    };


    /**
     * Логіка валідації логіна
     **/
    function validateLogin() {

        if (arguments[0])
            var code = arguments[0];

        if (!$scope.user.login && $scope.user.login === "")
            return;

        $scope.restoreAccessForm.login.$setValidity("login", true);
        $scope.restoreAccessForm.login.$setValidity("tokenInvalid", true);
        $scope.restoreAccessForm.login.$setValidity("token", true);

        if (code === 3) {
            $scope.restoreAccessForm.login.$setValidity("login", false);
            $scope.restoreAccessForm.login.$setValidity("tokenInvalid", true);
            $scope.restoreAccessForm.login.$setValidity("token", true);
        }

        if (code === 7)
            $rootScope.restoreAccessStatePart = "invalidTokenMessage";

        if (code === 8) {
            $scope.restoreAccessForm.login.$setValidity("login", true);
            $scope.restoreAccessForm.login.$setValidity("tokenInvalid", true);
            $scope.restoreAccessForm.login.$setValidity("token", false);
        }
    }

});





/**
 * Контроллер який відповідає за зміну пароля
 **/
app.controller('RestoreAccessChangePasswordCtrl', function($scope, $rootScope, $location, Account) {

    /**
     * Змінні
     **/
    $scope.showValidationMessages = false;

    $scope.user = {
        password: "",
        passwordRepeat: "",
        token: $location.search().token
    };

    var restoreAccessModal = angular.element(".restore-access-modal"),
        restoreAccessBtn   = restoreAccessModal.find(".btn-success"),
        tooltip            = restoreAccessModal.find("[data-toggle='tooltip']");


    /**
     * Провірка токена
     **/
//    Account.checkToken(function(data) {
//        if (data.code !== 0)
//            $rootScope.restoreAccessStatePart = "invalidTokenMessage";
//    });


    /**
     * Ініціалізація тултіпів
     **/
    restoreAccessModal.on("shown.bs.modal", function() {
        tooltip.tooltip({
            container: restoreAccessModal.find(".modal-dialog"),
            animation: false
        });
    });


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

        if ($scope.restoreAccessForm.$invalid)
            return;

        restoreAccessBtn.button('loading');

        Account.restoreAccessSendPasswords($scope.user).success(function(data) {
            restoreAccessBtn.button('reset');

            if (data.code === 0)
                sessionStorage.userName = data.user.name + " " + data.user.surname;

            if (data.code === 1)
                $rootScope.restoreAccessStatePart = "invalidTokenMessage";

            $location.search("token", null);
            $location.path("/search");
        });

    };


    /**
     * Валідація пароля
     **/
    function validatePasswords() {

        if (!$scope.user.passwordRepeat || $scope.user.passwordRepeat === "")
            return;

        if ($scope.user.password !== $scope.user.passwordRepeat)
            $scope.restoreAccessForm.passwordRepeat.$setValidity("passwords", false);
        else
            $scope.restoreAccessForm.passwordRepeat.$setValidity("passwords", true);
    }

});