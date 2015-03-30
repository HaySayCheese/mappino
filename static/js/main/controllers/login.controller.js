app.controller('LoginController', ['$scope', '$rootScope', '$timeout', '$location', 'Account', 'TXT',
    function($scope, $rootScope, $timeout, $location, Account, TXT) {
        "use strict";

        /**
         * Змінні
         **/
        $rootScope.pageTitle = "Логин - " + TXT.SERVICE_NAME;
        $scope.showValidationMessages = false;

        $scope.user = {
            name: "",
            password: ""
        };

        var loginModal = angular.element(".login-modal"),
            loginBtn   = loginModal.find(".btn-success"),
            tooltip    = loginModal.find("[data-toggle='tooltip']");

        loginModal.modal();


        ga('send', 'pageview', {
            'page': '#!/account/login',
            'title': $rootScope.pageTitle
        });


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

                window.location = "/cabinet/";
            }

            if (code === 3)
                $scope.loginForm.password.$setValidity("login", false);
        }
    }
]);