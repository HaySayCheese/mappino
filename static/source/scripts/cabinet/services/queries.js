/**
 * Файл з описом усіх http запитів
 * Змінні путів знаходяться в файлі "/services/http_const.js"
 **/



app.factory('Queries', ['$http', '$upload', 'HTTP_URL', function($http, $upload, HTTP_URL) {
    'use strict';

    return {

        Tags: {
            load: function(callback) {
                return $http.get(HTTP_URL.TAGS.GET_TAGS).success(callback);
            },

            create: function(tag, callback) {
                return $http.post(HTTP_URL.TAGS.CREATE_TAG, tag).success(callback);
            },

            remove: function(tagId, callback) {
                return $http.delete(HTTP_URL.TAGS.REMOVE_TAG.fmt(tagId)).success(callback);
            },

            update: function(tagId, tag, callback) {
                return $http.put(HTTP_URL.TAGS.UPDATE_TAG.fmt(tagId), tag).success(callback);
            }

        },


        Briefs: {
            load: function(category, callback) {
                return $http.get(HTTP_URL.BRIEFS.GET_BRIEFS.fmt(category)).success(callback);
            },

            search: function(value, callback) {
                return $http.get(HTTP_URL.BRIEFS.SEARCH.fmt(value)).success(callback);
            }
        },


        Publications: {
            load: function(tid, hid, callback) {
                return $http.get(HTTP_URL.PUBLICATIONS.GET_PUBLICATIONS.fmt(tid, hid)).success(callback);
            },

            loadChartData: function(tid, hid, days, callback) {
                return $http.get(HTTP_URL.PUBLICATIONS.GET_CHART_DATA.fmt(tid, hid, days)).success(callback);
            },

            create: function(publication, callback) {
                return $http.post(HTTP_URL.PUBLICATIONS.CREATE_PUBLICATION, publication).success(callback);
            },

            publish: function(tid, hid) {
                return $http.put(HTTP_URL.PUBLICATIONS.PUBLISH_PUBLICATION.fmt(tid, hid));
            },

            unpublish: function(tid, hid, callback) {
                return $http.put(HTTP_URL.PUBLICATIONS.UNPUBLISH_PUBLICATION.fmt(tid, hid)).success(callback);
            },

            toTrash: function(tid, hid, callback) {
                return $http.delete(HTTP_URL.PUBLICATIONS.TO_TRASH_PUBLICATION.fmt(tid, hid)).success(callback);
            },

            remove: function(tid, hid, callback) {
                return $http.delete(HTTP_URL.PUBLICATIONS.REMOVE_PUBLICATION.fmt(tid, hid)).success(callback);
            },

            check: function(tid, hid, data, callback) {
                return $http.put(HTTP_URL.PUBLICATIONS.CHECK_PUBLICATION_FIELD.fmt(tid, hid), data).success(callback);
            },

            uploadPhotos: function(tid, hid, photos, callback) {
                return $upload.upload({
                    url: HTTP_URL.PUBLICATIONS.UPLOAD_PUBLICATION_PHOTOS.fmt(tid, hid),
                    file: photos
                }).success(callback);
            },

            removePhoto: function(tid, hid, pid, callback) {
                return $http.delete(HTTP_URL.PUBLICATIONS.REMOVE_PUBLICATION_PHOTO.fmt(tid, hid, pid)).success(callback);
            },

            setMainPhoto: function(tid, hid, pid, callback) {
                return $http.post(HTTP_URL.PUBLICATIONS.SET_MAIN_PUBLICATION_PHOTO.fmt(tid, hid, pid)).success(callback);
            },

            counts: function(callback) {
                return $http.get(HTTP_URL.PUBLICATIONS.GET_PUBLICATIONS_COUNT).success(callback);
            }
        },


        Settings: {
            load: function(callback) {
                return $http.get(HTTP_URL.SETTINGS.GET_SETTINGS).success(callback);
            },

            check: function(data, callback) {
                return $http.post(HTTP_URL.SETTINGS.CHECK_SETTING_FIELD, data).success(callback);
            },

            uploadUserPhoto: function(photo, callback) {
                return $upload.upload({
                    url: HTTP_URL.SETTINGS.UPLOAD_USER_PHOTO,
                    file: photo
                }).then(callback);
            },

            logoutUser: function(callback) {
                return $http.post(HTTP_URL.SETTINGS.LOGOUT_USER).success(callback);
            }
        },


        Support: {
            loadTickets: function(callback) {
                return $http.get(HTTP_URL.SUPPORT.GET_TICKETS).success(callback);
            },

            loadTicketData: function(ticketId, callback) {
                return $http.get(HTTP_URL.SUPPORT.GET_TICKET_DATA.fmt(ticketId)).success(callback);
            },

            createTicket: function(callback) {
                return $http.post(HTTP_URL.SUPPORT.CREATE_TICKET).success(callback);
            },

            sendMessage: function(ticketId, message, callback) {
                return $http.post(HTTP_URL.SUPPORT.GET_TICKET_DATA.fmt(ticketId), message).success(callback);
            }
        }

    };
}]);