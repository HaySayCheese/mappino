'use strict';

app.controller('LoginCtrl', function($scope, $timeout, Account) {

    /**
     * Змінні
     **/
    $scope.showValidationMessages = false;

    $scope.user = {
        name: "",
        password: ""
    };

    var loginModal = angular.element(".login-modal"),
        loginBtn   = loginModal.find(".btn-success"),
        tooltip    = loginModal.find("[data-toggle='tooltip']");

    loginModal.modal();


    /**
     * Ініціалізація тултіпів
     **/
    loginModal.on("shown.bs.modal", function() {
        tooltip.tooltip({
            container: loginModal.find(".modal-dialog"),
            animation: false
        });
    });


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

        if ((!$scope.user.name || $scope.user.name === "") || (!$scope.user.password || $scope.user.password === ""))
            return;

        loginBtn.button("loading");

        Account.login($scope.user, function(data) {
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
            sessionStorage.userName = user.name + " " + user.surname;

            loginModal.modal('hide');
        }

        if (code === 3)
            $scope.loginForm.password.$setValidity("login", false);
    }
});