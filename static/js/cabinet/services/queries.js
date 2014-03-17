'use strict';

app.factory('Queries', function($http) {

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
                return $http.get('/ajax/api/cabinet/publications/briefs/' + category + '/').success(callback);
            },


            search: function(value, callback) {
                return $http.get("/ajax/api/cabinet/search/?q=" + value).success(callback);
            }

        },


        Publications: {
            load: function(tid, hid, callback) {
                return $http.get("/ajax/api/cabinet/publications/" + tid + ":" + hid + "/").success(callback);
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

            check: function(tid, hid, data, callback) {
                return $http.put("/ajax/api/cabinet/publications/" + tid + ":" + hid + "/", data).success(callback);
            },

            uploadPhotos: function(tid, hid, photos, callback) {
                return $http.post('/ajax/api/cabinet/publications/' + tid + ':' + hid + '/photos/', { file: photos }).success(callback);
            },

            removePhoto: function(tid, hid, pid, callback) {
                return $http.delete('/ajax/api/cabinet/publications/' + tid + ':' + hid + '/photos/' + pid + '/').success(callback);
            },

            counts: function(callback) {
                return $http.get('/ajax/api/cabinet/publications/counters/').success(callback);
            }
        }

    }


});