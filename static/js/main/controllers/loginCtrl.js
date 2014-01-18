'use strict';

app.controller('LoginCtrl', function($scope, $rootScope, $timeout, $http, $cookies) {

    $scope.user = {
        name: "",
        password: ""
    };


    $scope.submitLogin = function() {
        $http({
            method: 'POST',
            url: 'ajax/api/accounts/login/',
            headers: {
                'X-CSRFToken': $cookies.csrftoken
            },
            data: {
                username: $scope.user.name,
                password: $scope.user.password
            }
        }).success(function(data, status) {
                if (data.code == 0)
                    $('.login-dialog').parent().modal('hide');
        });
    }
});