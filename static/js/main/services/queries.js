/**
 * Файл з описом усіх http запитів
 **/

'use strict';

app.factory('Queries', function($http) {
   return {
       Map: {
           getMarkers: function(filters) {
               return $http.get('/ajax/api/markers/?p=' + filters)
           },

           getPublicationDescription: function(tid_hid) {
               return $http.get('/ajax/api/detailed/publication/' + tid_hid + '/')
           },

           getPublicationContacts: function(tid_hid) {
               return $http.get('/ajax/api/detailed/publication/' + tid_hid + '/contacts/')
           },

           sendPublicationMessage: function(tid_hid, message) {
               return $http.post('/ajax/api/notifications/send-message/' + tid_hid + '/', {
                   message: message.text,
                   email: message.email,
                   name: message.name
               })
           },

           sendPublicationCallRequest: function(tid_hid, call_request) {
               return $http.post('/ajax/api/notifications/send-call-request/' + tid_hid + '/', {
                   phone_number: call_request.phone,
                   name: call_request.name
               })
           }
       },


       Account: {
           loginUser: function(user) {
               return $http.post('/ajax/api/accounts/login/', {
                   username: user.name,
                   password: user.password
               });
           },

           logoutUser: function() {
               return $http.post('/ajax/api/accounts/logout/');
           },

           registerUser: function(user) {
               return $http.post('/ajax/api/accounts/registration/', {
                   'name':             user.name,
                   'surname':          user.surname,
                   'phone-number':     "+380" + user.phoneNumber,
                   'email':            user.email,
                   'password':         user.password,
                   'password-repeat':  user.passwordRepeat
               });
           },

           repeatRegistration: function() {
               return $http.post('/ajax/api/accounts/registration/cancel/');
           },

           repeatSendCode: function() {
               return $http.post('/ajax/api/accounts/registration/resend-sms/');
           },

           validateEmail: function(email) {
               return $http.post('/ajax/api/accounts/validate-email/', {
                   email: email
               });
           },

           validatePhone: function(phone) {
               return $http.post('/ajax/api/accounts/validate-phone-number/', {
                   number: phone
               });
           },


           // Відправка кода телефона на валідацію
           validatePhoneCode: function(code) {
               return $http.post('/ajax/api/accounts/registration/', {
                   code: code
               });
           },

           getUserName: function() {
               return $http.get('/ajax/api/accounts/on-login-info/');
           },

           restoreAccessSendEmail: function(username) {
               return $http.post('/ajax/api/accounts/password-reset/', {
                   username: username
               });
           },

           restoreAccessSendPasswords: function(user) {
               return $http.post('/ajax/api/accounts/password-reset/restore/', {
                   'token': user.token,
                   'password': user.password,
                   'password-repeat': user.passwordRepeat
               });
           }
       }
   }
});