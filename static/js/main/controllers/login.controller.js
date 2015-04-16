app.controller('LoginController', ['$scope', '$rootScope', '$timeout', '$location', 'TXT', 'BAuthService',
    function($scope, $rootScope, $timeout, $location, TXT, BAuthService) {
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

            if ((!$scope.user.name || $scope.user.name === "") || (!$scope.user.password || $scope.user.password === "")) {
                return;
            }

            loginBtn.button("loading");

            BAuthService.login($scope.user, function () {
                loginBtn.button("reset");
                loginModal.modal('hide');
                window.location = "/cabinet/";
            }, function () {
                $scope.loginForm.password.$setValidity("login", false);

                loginBtn.button("reset");
            });
        };
    }
]);