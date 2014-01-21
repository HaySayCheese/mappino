'use strict';

app.controller('SidebarCtrl', function($scope, $rootScope, $cookies, $http) {

    $scope.userName = "";

    /**
     * Дивимся за кукою сесії, якщо вона є то
     * берем куку з іменем юзера якщо і вона є
     **/
    $scope.$watch(function() {

        return $cookies.sessionid;

    }, function(newValue, oldValue) {

        if (sessionStorage.userName)
            $scope.userName = sessionStorage.userName;
        else
            getUserName();

        if (!newValue)
            delete sessionStorage.userName;
    });


    /**
     * Дивимся за кукою з іменем юзера, якщо її нема
     * то видаляєм куку сесії
     **/
    $scope.$watch(function() {

        return sessionStorage.userName;

    }, function(newValue, oldValue) {

        if (!newValue)
            getUserName();
    });

    function getUserName() {
        $http({
            method: 'GET',
            url: 'ajax/api/accounts/on-login-info/',
            headers: {
                'X-CSRFToken': $cookies.csrftoken
            }
        }).success(function(data, status) {
            sessionStorage.userName = data;
        });
    }
});