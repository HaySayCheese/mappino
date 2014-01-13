'use strict';

app.controller('RegistrationCtrl', function($scope, $timeout, $http, $cookies) {

    $scope.user = {
        firstName:  "",
        lastName:   "",

        email: "",

        phoneNumber: "",

        firstPassword: "",
        lastPassword:  ""
    };

    $timeout(function() {
        angular.element("input")[0].focus();
    }, 300);

    angular.element("input[name='email']").bind("focusout", function() {
        $http({
            method: 'POST',
            url: 'ajax/api/accounts/validate-email/',
            headers: {
                'X-CSRFToken': $cookies.csrftoken
            },
            data: {
                email: $scope.user.email
            }
            }).success(function(data, status) {
                console.log("aa")
            }).error(function(data, status) {
                console.log("aa")
        });
        console.log($scope.user.email)
    });


    $scope.submitRegistration = function() {

    }
});