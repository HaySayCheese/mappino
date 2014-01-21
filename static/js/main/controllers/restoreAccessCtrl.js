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



app.controller('RestoreAccessSendMailCtrl', function($scope, $timeout, $http, authorizationQueries) {

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
     * Клік по кнопці відправки пошти
     **/
    $scope.submitSendEmail = function() {
        $scope.showValidationMessages = true;

        var sendBtn = $(".restore-access-dialog .btn-success");

        sendBtn.button('loading');

        authorizationQueries.restoreAccessSendEmail($scope.user.login).success(function(data) {
            console.log(data);
            sendBtn.button('reset');
        });
    };

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