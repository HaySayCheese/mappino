'use strict';

app.controller('LoginCtrl', function($scope, $timeout, $cookies, authorizationQueries) {

    /**
     * Змінні
     **/
    $scope.showValidationMessages = false;

    $scope.user = {
        name: "",
        password: ""
    };


    /**
     * Фокус першого поля і ініціалізація тултіпів
     **/
    $timeout(function() {
        angular.element("input")[0].focus();

        $("[data-toggle='tooltip']").tooltip({
            container: '.login-dialog',
            animation: false
        });
    }, 300);


    /**
     * Якщо в полях є дані і юзер змфнює їх
     * то забирати повідомлення про помилку
     **/
    $scope.$watchCollection("user", function(newValue, oldValue) {
        $scope.loginForm.password.$setValidity("login", true);
    });


    /**
     * Клік по кнопці входу
     **/
    $scope.submitLogin = function() {

        $scope.showValidationMessages = true;

        var loginBtn = $(".login-dialog .btn-success");

        if ((!$scope.user.name || $scope.user.name === "") || (!$scope.user.password || $scope.user.password === ""))
            return;

        loginBtn.button("loading");

        authorizationQueries.loginUser($scope.user).success(function(data) {
            loginBtn.button("reset");

            validateLoginForm(data);
        })
    };


    /**
     * Логіка валідаці форми логіну
     **/
    function validateLoginForm() {

        if (arguments[0])
            var code = arguments[0].code,
                user = arguments[0].user;

        if (code === 0) {
            sessionStorage.userName = user.name + " " + user.surname;

            $('.login-dialog').parent().modal('hide');
        }

        if (code === 3)
            $scope.loginForm.password.$setValidity("login", false);
    }
});