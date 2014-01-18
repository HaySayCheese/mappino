'use strict';

app.controller('LoginCtrl', function($scope, $http, $timeout, $cookies) {

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

        $http({
            method: 'POST',
            url: 'ajax/api/accounts/login/',
            headers: {
                'X-CSRFToken': $cookies.csrftoken
            },
            data: {
                username: $scope.user.name,
                password: $scope.user.password
            }
        }).success(function(data, status) {

            loginBtn.button("reset");

            validateLoginForm(data);
        });
    };


    /**
     * Логіка валідаці форми логіну
     **/
    function validateLoginForm() {

        if (arguments[0])
            var code = arguments[0].code,
                user = arguments[0].user;

        if (code === 0) {
            $cookies.userName = user.name + " " + user.surname;

            $('.login-dialog').parent().modal('hide');
        }

        if (code === 3)
            $scope.loginForm.password.$setValidity("login", false);
    }
});