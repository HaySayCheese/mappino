/**
 * Файл з описом усіх http запитів
 * Змінні путів знаходяться в файлі "/services/http_const.js"
 **/

'use strict';

app.factory('Queries', function($http, HTTP_URL) {
   return {
       Map: {
           getMarkers: function(filters) {
               return $http.get(HTTP_URL.MAP.GET_MARKERS.fmt(filters))
           },

           getPublicationDescription: function(tid_hid) {
               return $http.get(HTTP_URL.MAP.GET_PUBLICATION_DESCRIPTION.fmt(tid_hid))
           },

           getPublicationContacts: function(tid_hid) {
               return $http.get(HTTP_URL.MAP.GET_PUBLICATION_CONTACTS.fmt(tid_hid))
           },

           sendPublicationMessage: function(tid_hid, message) {
               return $http.post(HTTP_URL.MAP.SEND_PUBLICATION_MESSAGE.fmt(tid_hid), {
                   name:    message.name,
                   email:   message.email,
                   message: message.text
               })
           },

           sendPublicationCallRequest: function(tid_hid, call_request) {
               return $http.post(HTTP_URL.MAP.SEND_PUBLICATION_MESSAGE.fmt(tid_hid), {
                   name:            call_request.name,
                   phone_number:    call_request.phone
               })
           }
       },


       Account: {
           loginUser: function(user) {
               return $http.post(HTTP_URL.ACCOUNT.LOGIN, {
                   username: user.name,
                   password: user.password
               });
           },

           logoutUser: function() {
               return $http.post(HTTP_URL.ACCOUNT.LOGOUT);
           },

           registerUser: function(user) {
               return $http.post(HTTP_URL.ACCOUNT.REGISTRATION, {
                   'name':             user.name,
                   'surname':          user.surname,
                   'phone-number':     "+380" + user.phoneNumber,
                   'email':            user.email,
                   'password':         user.password,
                   'password-repeat':  user.passwordRepeat
               });
           },

           repeatRegistration: function() {
               return $http.post(HTTP_URL.ACCOUNT.REPEAT_REGISTRATION);
           },

           repeatSendCode: function() {
               return $http.post(HTTP_URL.ACCOUNT.REPEAT_SEND_CODE);
           },

           validateEmail: function(email) {
               return $http.post(HTTP_URL.ACCOUNT.VALIDATE_EMAIL, {
                   email: email
               });
           },

           validatePhone: function(phone) {
               return $http.post(HTTP_URL.ACCOUNT.VALIDATE_PHONE_NUMBER, {
                   number: phone
               });
           },


           // Відправка кода телефона на валідацію
           validatePhoneCode: function(code) {
               return $http.post(HTTP_URL.ACCOUNT.VALIDATE_PHONE_CODE, {
                   code: code
               });
           },

           getUserName: function() {
               return $http.get(HTTP_URL.ACCOUNT.GET_USER_NAME);
           },

           restoreAccessSendEmail: function(username) {
               return $http.post(HTTP_URL.ACCOUNT.RESTORE_ACCESS_SEND_EMAIL, {
                   username: username
               });
           },

           restoreAccessSendPasswords: function(user) {
               return $http.post(HTTP_URL.ACCOUNT.RESTORE_ACCESS_SEND_PASSWORD, {
                   'token': user.token,
                   'password': user.password,
                   'password-repeat': user.passwordRepeat
               });
           }
       }
   }
});