'use strict';

app.factory('authorizationQueries', function($http, $cookies) {

    return {

        // Запит на авторизацію користувача
        loginUser: function(user) {
            return $http({
                url: 'ajax/api/accounts/login/',
                method: "POST",
                headers: {
                    'X-CSRFToken': $cookies.csrftoken
                },
                data: {
                    username: user.name,
                    password: user.password
                }
            });
        },


        // Запит на вихід користувача
        logoutUser: function() {
            return $http({
                url: 'ajax/api/accounts/logout/',
                method: "POST",
                headers: {
                    'X-CSRFToken': $cookies.csrftoken
                }
            });
        },


        // Запит на реєстрацію користувача
        registerUser: function(user) {
            return $http({
                method: 'POST',
                url: 'ajax/api/accounts/registration/',
                headers: {
                    'X-CSRFToken': $cookies.csrftoken
                },
                data: {
                    'name':             user.name,
                    'surname':          user.surname,
                    'phone-number':     user.phoneNumber,
                    'email':            user.email,
                    'password':         user.password,
                    'password-repeat':  user.passwordRepeat
                }
            });
        },


        // Запит на повторну реєстрацію користувача
        repeatRegistration: function() {
            return $http({
                method: 'POST',
                url: 'ajax/api/accounts/registration/cancel/',
                headers: {
                    'X-CSRFToken': $cookies.csrftoken
                }
            });
        },


        // Запит на повторну відправку кода на телефон
        repeatSendCode: function() {
            return $http({
                method: 'POST',
                url: 'ajax/api/accounts/registration/resend-sms/',
                headers: {
                    'X-CSRFToken': $cookies.csrftoken
                }
            });
        },


        // Відправка пошти на валідацію
        validateEmail: function(email) {
            return $http({
                method: 'POST',
                url: 'ajax/api/accounts/validate-email/',
                headers: {
                    'X-CSRFToken': $cookies.csrftoken
                },
                data: {
                    email: email
                }
            });
        },


        // Відправка телефона на валідацію
        validatePhone: function(phone) {
            return $http({
                method: 'POST',
                url: 'ajax/api/accounts/validate-phone-number/',
                headers: {
                    'X-CSRFToken': $cookies.csrftoken
                },
                data: {
                    number: phone
                }
            });
        },


        // Відправка кода телефона на валідацію
        validatePhoneCode: function(code) {
            return $http({
                method: 'POST',
                url: 'ajax/api/accounts/registration/',
                headers: {
                    'X-CSRFToken': $cookies.csrftoken
                },
                data: {
                    code: code
                }
            });
        },


        // Відправка запита на отримання імені користувача
        getUserName: function() {
            return $http({
                method: 'GET',
                url: 'ajax/api/accounts/on-login-info/',
                headers: {
                    'X-CSRFToken': $cookies.csrftoken
                }
            });
        },


        // Відправка запита на відправку мила юзеру
        restoreAccessSendEmail: function(username) {
            return $http({
                method: 'POST',
                url: 'ajax/api/accounts/password-reset/',
                headers: {
                    'X-CSRFToken': $cookies.csrftoken
                },
                data: {
                    username: username
                }
            })
        },


        // Відправка нових паролів серверу
        restoreAccessSendPasswords: function(user) {
            return $http({
                method: 'POST',
                url: 'ajax/api/accounts/password-reset/',
                headers: {
                    'X-CSRFToken': $cookies.csrftoken
                },
                data: {
                    'token': user.token,
                    'password': user.password,
                    'password-repeat': user.passwordRepeat
                }
            })
        },


        // Перевірка токена
        checkToken: function(token) {
            return $http({
                method: 'POST',
                url: 'ajax/api/accounts/password-reset/check/',
                headers: {
                    'X-CSRFToken': $cookies.csrftoken
                },
                data: {
                    token: token
                }
            })
        }

    }
});