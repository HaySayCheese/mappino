angular.module('binno.utils.angular.services.user', ['ngCookies'])
    .factory('UserService', ['$http', '$cookieStore', function($http, $cookieStore) {
        "use strict";


        return {

            checkIfLoginIn: function(callback) {
                var that = this;

                $http.get('/ajax/api/accounts/on-login-info/')
                    .success(function(data) {
                        that.setToStores(data);
                        _.isFunction(callback) && callback();
                    })
                    .error(function() {
                        that.removeFromStores();
                        _.isFunction(callback) && callback();
                    });
            },



            setToStores: function(data) {
                if (sessionStorage) {
                    sessionStorage.userName = data.user.name + " " + data.user.surname;
                }
                if (localStorage) {
                    localStorage.userName = data.user.name + " " + data.user.surname;
                }
            },



            removeFromStores: function() {
                if (sessionStorage.userName) {
                    delete sessionStorage.userName;
                }
                if (localStorage.userName) {
                    delete localStorage.userName;
                }
                $cookieStore.remove('sessionid');
            },



            getUserName: function() {
                return localStorage.userName || sessionStorage.userName || null;
            },



            logoutUser: function(callback) {
                var that = this;

                $http.post('/ajax/api/accounts/logout/')
                    .success(function() {
                        that.removeFromStores();
                        $cookieStore.remove('sessionid');
                        _.isFunction(callback) && callback();
                    });
            }
        };
    }]
);