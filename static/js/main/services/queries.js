/**
 * Файл з описом усіх http запитів
 * Змінні путів знаходяться в файлі "/services/http_const.js"
 **/



app.factory('Queries', ['$http','HTTP_URL', function($http, HTTP_URL) {
    'use strict';

    return {
        Map: {
            getMarkers: function(filters) {
                return $http.get(HTTP_URL.MAP.GET_MARKERS.fmt(filters));
            },

            getPublicationDescription: function(tid_hid) {
                return $http.get(HTTP_URL.MAP.GET_PUBLICATION_DESCRIPTION.fmt(tid_hid));
            },

            getPublicationContacts: function(tid_hid) {
                return $http.get(HTTP_URL.MAP.GET_PUBLICATION_CONTACTS.fmt(tid_hid));
            },

            sendPublicationMessage: function(tid_hid, message) {
                return $http.post(HTTP_URL.MAP.SEND_PUBLICATION_MESSAGE.fmt(tid_hid), {
                    name:    message.name,
                    email:   message.email,
                    message: message.text
                });
            },

            sendPublicationCallRequest: function(tid_hid, call_request) {
                return $http.post(HTTP_URL.MAP.SEND_PUBLICATION_CALL_REQUEST.fmt(tid_hid), {
                    name:            call_request.name,
                    phone_number:    call_request.phone
                });
            }
        },


        Account: {
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
    };
}]);