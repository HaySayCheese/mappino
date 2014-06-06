'use strict';

app.factory('Queries', function($http, $q, $upload) {

    return {

        Tags: {
            load: function(callback) {
                return $http.get('/ajax/api/cabinet/dirtags/').success(callback);
            },

            create: function(tag, callback) {
                return $http.post('/ajax/api/cabinet/dirtags/', tag).success(callback);
            },

            remove: function(tagId, callback) {
                return $http.delete('/ajax/api/cabinet/dirtags/' + tagId + "/").success(callback);
            },

            update: function(tagId, tag, callback) {
                return $http.put('/ajax/api/cabinet/dirtags/' + tagId + "/", tag).success(callback);
            }

        },


        Briefs: {
            load: function(category, callback) {
                //var canceler = $q.defer(), request = "";
                return $http.get('/ajax/api/cabinet/publications/briefs/' + category + '/').success(callback);
                //canceler.resolve();
            },

            search: function(value, callback) {
                return $http.get("/ajax/api/cabinet/search/?q=" + value).success(callback);
            }
        },


        Publications: {
            load: function(tid, hid, callback) {
                return $http.get("/ajax/api/cabinet/publications/" + tid + ":" + hid + "/").success(callback);
            },

            loadChartData: function(tid, hid, days, callback) {
                return $http.get("/ajax/api/cabinet/stats/publications/" + tid + ":" + hid + "/visits/?count=" + days).success(callback);
            },

            create: function(publication, callback) {
                return $http.post('/ajax/api/cabinet/publications/', publication).success(callback);
            },

            publish: function(tid, hid, callback) {
                return $http.put('/ajax/api/cabinet/publications/' + tid + ":" + hid + '/publish/').success(callback);
            },

            unpublish: function(tid, hid, callback) {
                return $http.put('/ajax/api/cabinet/publications/' + tid + ":" + hid + '/unpublish/').success(callback);
            },

            toTrash: function(tid, hid, callback) {
                return $http.delete('/ajax/api/cabinet/publications/' + tid + ":" + hid + '/').success(callback);
            },

            remove: function(tid, hid, callback) {
                return $http.delete('/ajax/api/cabinet/publications/' + tid + ":" + hid + '/delete-permanent/').success(callback);
            },

            check: function(tid, hid, data, callback) {
                return $http.put("/ajax/api/cabinet/publications/" + tid + ":" + hid + "/", data).success(callback);
            },

            uploadPhotos: function(tid, hid, photos, callback) {
                return $upload.upload({
                    url: '/ajax/api/cabinet/publications/' + tid + ':' + hid + '/photos/',
                    file: photos
                })
                .success(callback);
            },

            removePhoto: function(tid, hid, pid, callback) {
                return $http.delete('/ajax/api/cabinet/publications/' + tid + ':' + hid + '/photos/' + pid + '/').success(callback);
            },

            setMainPhoto: function(tid, hid, pid, callback) {
                return $http.post('/ajax/api/cabinet/publications/' + tid + ':' + hid + '/photos/' + pid + '/title/').success(callback);
            },

            counts: function(callback) {
                return $http.get('/ajax/api/cabinet/publications/counters/').success(callback);
            }
        },


        Settings: {
            load: function(callback) {
                return $http.get("/ajax/api/cabinet/account/").success(callback);
            },

            check: function(data, callback) {
                return $http.post("/ajax/api/cabinet/account/", data).success(callback);
            },

            uploadUserPhoto: function(photo, callback) {
                return $upload.upload({
                    url: '/ajax/api/cabinet/account/photo/',
                    file: photo
                }).success(callback);
            },

            logoutUser: function(callback) {
                return $http.post('/ajax/api/accounts/logout/').success(callback);
            }
        },


        Support: {
            loadTickets: function(callback) {
                return $http.get("/ajax/api/cabinet/support/tickets/").success(callback);
            },

            loadTicketData: function(ticketId, callback) {
                return $http.get("/ajax/api/cabinet/support/tickets/" + ticketId + "/messages/").success(callback);
            },

            createTicket: function(callback) {
                return $http.post("/ajax/api/cabinet/support/tickets/").success(callback);
            },

            sendMessage: function(ticketId, message, callback) {
                return $http.post("/ajax/api/cabinet/support/tickets/" + ticketId + "/messages/", message).success(callback);
            }
        }

    }


});