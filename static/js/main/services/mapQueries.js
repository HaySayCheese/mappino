'use strict';

app.factory('mapQueries', function($http) {

    return {
        getMarkers: function(tid, filters, viewport) {
            return $http.get('ajax/api/markers/?tid=' + tid + viewport + filters)
        },

        getPublicationDescription: function(tid_hid) {
            return $http.get('ajax/api/detailed/publication/' + tid_hid + '/')
        },

        getPublicationContacts: function(tid_hid) {
            return $http.get('ajax/api/detailed/publication/' + tid_hid + '/contacts/')
        },

        sendPublicationMessage: function(tid_hid, message) {
            return $http.post('ajax/api/notifications/send-message/' + tid_hid + '/', {
                message: message.text,
                email: message.email,
                name: message.name
            })
        },

        sendPublicationCallRequest: function(tid_hid, call_request) {
            return $http.post('ajax/api/notifications/send-call-request/' + tid_hid + '/', {
                phone_number: call_request.phone,
                name: call_request.name
            })
        }

    }

});