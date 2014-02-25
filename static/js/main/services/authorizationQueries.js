'use strict';

app.factory('authorizationQueries', function($http) {

    return {

        // Запит на авторизацію користувача
        loginUser: function(user) {
            return $http.post('ajax/api/accounts/login/', {
                    username: user.name,
                    password: user.password
                });
        },


        // Запит на вихід користувача
        logoutUser: function() {
            return $http.post('ajax/api/accounts/logout/');
        },


        // Запит на реєстрацію користувача
        registerUser: function(user) {
            return $http.post('ajax/api/accounts/registration/', {
                    'name':             user.name,
                    'surname':          user.surname,
                    'phone-number':     user.phoneNumber,
                    'email':            user.email,
                    'password':         user.password,
                    'password-repeat':  user.passwordRepeat
                });
        },


        // Запит на повторну реєстрацію користувача
        repeatRegistration: function() {
            return $http.post('ajax/api/accounts/registration/cancel/');
        },


        // Запит на повторну відправку кода на телефон
        repeatSendCode: function() {
            return $http.post('ajax/api/accounts/registration/resend-sms/');
        },


        // Відправка пошти на валідацію
        validateEmail: function(email) {
            return $http.post('ajax/api/accounts/validate-email/', {
                    email: email
                });
        },


        // Відправка телефона на валідацію
        validatePhone: function(phone) {
            return $http.post('ajax/api/accounts/validate-phone-number/', {
                    number: phone
                });
        },


        // Відправка кода телефона на валідацію
        validatePhoneCode: function(code) {
            return $http.post('ajax/api/accounts/registration/', {
                    code: code
                });
        },


        // Відправка запита на отримання імені користувача
        getUserName: function() {
            return $http.get('ajax/api/accounts/on-login-info/');
        },


        // Відправка запита на відправку мила юзеру
        restoreAccessSendEmail: function(username) {
            return $http.post('ajax/api/accounts/password-reset/', {
                    username: username
                });
        },


        // Відправка нових паролів серверу
        restoreAccessSendPasswords: function(user) {
            return $http.post('ajax/api/accounts/password-reset/', {
                    'token': user.token,
                    'password': user.password,
                    'password-repeat': user.passwordRepeat
                });
        },


        // Перевірка токена
        checkToken: function(token) {
            return $http.post('ajax/api/accounts/password-reset/check/', {
                    token: token
                });
        }
    }
});