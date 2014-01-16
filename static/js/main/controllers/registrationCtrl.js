'use strict';

app.controller('RegistrationCtrl', function($scope, $timeout, $http, $cookies) {

    $scope.showValidationMessages = false;
    $scope.showValidationEmail = false;

    var EMAIL_REGEXP = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$/;

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

        $("[data-toggle='tooltip']").tooltip({
            container: '.registration-dialog'
        })
    }, 300);


    $scope.$watchCollection("user", function(newValue, oldValue) {

        if (newValue.email && newValue.email != "") {
            if (!EMAIL_REGEXP.test(newValue.email)) {
                $scope.registrationForm.email.$setValidity("email", false);
            } else {
                $scope.registrationForm.email.$setValidity("email", true);
            }
        } else {
            $scope.registrationForm.email.$setValidity("email", true);
        }


        if (newValue.lastPassword != newValue.firstPassword && newValue.lastPassword.length)
            $scope.registrationForm.lastPassword.$setValidity("match", false);
        else
            $scope.registrationForm.lastPassword.$setValidity("match", true);

        console.log(newValue)
    });


    angular.element("input[name='email']").bind("focusout", function() {
        if (!$scope.registrationForm.email.$error.email && $scope.user.email != "")
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

                if (data.code == 0)
                    $scope.registrationForm.email.$setValidity("free", true);
                else
                    $scope.registrationForm.email.$setValidity("free", false);

                $scope.showValidationEmail = true;

            }).error(function(data, status) {
                $scope.registrationForm.email.$setValidity("free", false);
                $scope.showValidationEmail = true;
        });
    });


    $scope.submitRegistration = function() {
        //$scope.showValidationMessages = true;
    }
});