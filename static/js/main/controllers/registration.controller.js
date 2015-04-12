app.controller('RegistrationController', ['$scope', '$rootScope', '$cookieStore', 'TXT',
    function($scope, $rootScope, $cookieStore, TXT) {
        "use strict";

        $rootScope.pageTitle = "Регистрация - " + TXT.SERVICE_NAME;
        angular.element(".registration-modal").modal();

        ga('send', 'pageview', {
            'page': '#!/account/registration',
            'title': $rootScope.pageTitle
        });

        /**
         * Стан вікна реєстрації
         **/
        if ($cookieStore.get("mcheck")) {
            $rootScope.registrationStatePart = "codeCheck";
        } else {
            $rootScope.registrationStatePart = "registration";
        }
    }
]);





/**
 * Контроллер який відповідає за форму реєстрації
 **/
app.controller('RegistrationUserController', ['$scope', '$rootScope', '$cookies', 'Account', 'BAuthService',
    function($scope, $rootScope, $cookies, Account, BAuthService) {
        "use strict";

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
            name:           "",
            surname:        "",
            email:          "",
            phoneNumber:    "",
            password:       "",
            passwordRepeat: ""
        };


        /**
         * Змінні
         **/
        var registrationModal = angular.element(".registration-modal"),
            registrationBtn   = registrationModal.find(".btn-success"),
            tooltip           = registrationModal.find("[data-toggle='tooltip']"),
            emailInput        = registrationModal.find("input[name='email']"),
            phoneInput        = registrationModal.find("input[name='phoneNumber']");


        /**
         * Ініціалізація тултіпів
         **/
        registrationModal.on("shown.bs.modal", function() {
            tooltip.tooltip({
                container: registrationModal.find(".modal-dialog"),
                animation: false
            });
        });


        /**
         * Валідація даних при вводі
         **/
        $scope.$watchCollection("user", function() {
            validatePassword();
        });


        /**
         * Валідація пошти при вводі даних в поле
         **/
        $scope.$watch("user.email", function(newValue, oldValue) {
            if (oldValue !== newValue) {
                validateEmail();
            }
        });


        /**
         * Валідація телефона при вводі даних в поле
         **/
        $scope.$watch("user.phoneNumber", function(newValue, oldValue) {
            if (oldValue !== newValue) {
                validatePhone();
            }
        });


        /**
         * Валідація пошти при втраті фокуса з поля
         **/
        emailInput.bind("focusout", function() {
            sendEmailToValidate();
        });


        /**
         * Валідація телефона при втраті фокуса з поля
         **/
        phoneInput.bind("focusout", function() {
            sendPhoneToValidate();
        });


        /**
         * Клік по кнопці реєстрації
         **/
        $scope.submitRegistration = function() {
            $scope.showValidationMessages   = true;
            $scope.showValidationEmail      = true;
            $scope.showValidationPhone      = true;

            if (!$scope.validated.email) {
                sendEmailToValidate();
            }

            if (!$scope.validated.phone) {
                sendPhoneToValidate();
            }

            if ($scope.registrationForm.$valid) {
                registerUser();
            }
        };


        /**
         * Логіка валідації пошти
         **/
        function validateEmail() {
            $scope.registrationForm.email.$setValidity("free", true);
            $scope.registrationForm.email.$setValidity("email", true);
            $scope.registrationForm.email.$setValidity("isOk", false);


            var code = null;
            if (arguments[0]) {
                code = arguments[0];
            }


            if (!$scope.user.email && $scope.user.email === "") {
                return;
            }

            if (code === 0) {
                $scope.registrationForm.email.$setValidity("free", true);
            }

            if (code === 1) {
                $scope.registrationForm.email.$setValidity("email", false);
            }

            if (code === 2) {
                $scope.registrationForm.email.$setValidity("free", false);
            }

            $scope.showValidationEmail = true;
        }


        /**
         * Відправка пошти на валідацію
         **/
        function sendEmailToValidate() {
            $scope.registrationForm.email.$setValidity("isOk", false);

            if (!$scope.user.email || $scope.user.email === "") {
                return;
            }

            $scope.validated.email = false;

            BAuthService.validateEmail($scope.user.email, function() {
                $scope.registrationForm.email.$setValidity("isOk", true);

                $scope.validated.email = true;
            }, function(response) {
                validateEmail(response.code);
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

            var code = null;
            if (arguments[0]) {
                code = arguments[0];
            }

            if (!$scope.user.phoneNumber && $scope.user.phoneNumber === "") {
                return;
            }

            if (code === 0) {
                $scope.registrationForm.phoneNumber.$setValidity("free", true);
            }

            if (code === 1) {
                $scope.registrationForm.phoneNumber.$setValidity("phone", false);
            }

            if (code === 2) {
                $scope.registrationForm.phoneNumber.$setValidity("code", false);
            }

            if (code === 3) {
                $scope.registrationForm.phoneNumber.$setValidity("free", false);
            }

            $scope.showValidationPhone = true;
        }


        /**
         * Відправка телефона на валідацію
         **/
        function sendPhoneToValidate() {
            $scope.registrationForm.phoneNumber.$setValidity("isOk", false);

            if (!$scope.user.phoneNumber || $scope.user.phoneNumber === "") {
                return;
            }

            $scope.validated.phone = false;

            Account.checkPhone($scope.user.phoneNumber, function(data) {
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
            if ($scope.user.password !== $scope.user.passwordRepeat && $scope.user.passwordRepeat.length) {
                $scope.registrationForm.passwordRepeat.$setValidity("match", false);
            } else {
                $scope.registrationForm.passwordRepeat.$setValidity("match", true);
            }
        }


        /**
         * Функція відправки введених даних
         **/
        function registerUser() {
            registrationBtn.button('loading');

            MAuthService.register($scope.user, function() {
                registrationBtn.button('reset');

                $rootScope.registrationStatePart = "codeCheck";
            }, function() {
                registrationBtn.button('reset');
            });
        }
    }
]);





/**
 * Контроллер який відповідає за форму введення коду підтвердження
 **/
app.controller("RegistrationUserCodeCheckController", ['$scope', '$cookies', '$rootScope', 'TXT',
    function($scope, $cookies, $rootScope, TXT) {
        "use strict";

        /**
         * Змінні
         **/
        $scope.codeCheck = "";

        var registrationModal = angular.element(".registration-modal"),
            registrationBtn   = registrationModal.find(".btn-success"),
            tooltip           = registrationModal.find("[data-toggle='tooltip']"),
            attempt,
            max_attempts;


        /**
         * Функція відправки кода на перевірку
         **/
        $scope.checkPhoneCode = function() {

            if (!$scope.codeCheck || $scope.codeCheck === "") {

                tooltip.tooltip('destroy');
                tooltip.tooltip({
                    container: registrationModal.find(".modal-dialog"),
                    animation: false,
                    title: "Обязательное поле"
                });

                $scope.incorrectCode = true;

                return;
            }

            sendCodeToValidate();
        };


        /**
         * Функція повторної реєстрації
         **/
        $scope.repeatRegistration = function() {
            Account.repeatRegister(function() {
                $rootScope.registrationStatePart = "registration";
            });
        };


        /**
         * Функція повторної відправки кода
         **/
        $scope.repeatSendCode = function(e) {
            Account.repeatSendCode(function(data) {
                if (data.code === 0)
                    $scope.codeSend = true;
                else
                    $scope.codeSendBefore = true;
            });
        };


        /**
         * Відправка кода на валідацію
         **/
        function sendCodeToValidate() {

            registrationBtn.button('loading');

            Account.checkPhoneCode($scope.codeCheck, function(data) {
                registrationBtn.button('reset');

                attempt = data.attempts;
                max_attempts = data.max_attempts;

                validateAttempts(data);
            });

        }


        /**
         * Валідація спроб вводу кода
         **/
        function validateAttempts() {

            if (attempt && (attempt === max_attempts)) {
                $rootScope.registrationStatePart = "registration";

                return;
            }

            if (arguments[0])
                var code = arguments[0].code,
                    user = arguments[0].user;

            tooltip.tooltip('destroy');
            tooltip.tooltip({
                container: registrationModal.find(".modal-dialog"),
                animation: false,
                title: "Некорректный код. Попытка " +  attempt + " из " +  max_attempts + "."
            });

            if (code == 0) {
                sessionStorage.userName = user.name + " " + user.surname;
                registrationModal.modal('hide');

                window.location = "/cabinet/";
            }

            $scope.incorrectCode = true;
        }

    }
]);