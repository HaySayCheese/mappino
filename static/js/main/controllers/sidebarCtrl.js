'use strict';

app.controller('SidebarCtrl', function($scope, $rootScope, $cookies, $timeout, Account) {

    $scope.userName = "";

    getUserName();


    /**
     * Дивимся за кукою сесії, якщо вона є то
     * берем куку з іменем юзера якщо і вона є
     **/
    $scope.$watch(function() {
        return $cookies.sessionid;
    }, function(newValue, oldValue) {

        if (sessionStorage.userName)
            $scope.userName = sessionStorage.userName;

        if (!$cookies.sessionid)
            delete sessionStorage.userName;
    });


    /**
     * Дивимся за кукою з іменем юзера, якщо її нема
     * то видаляєм куку сесії
     **/
    $scope.$watch(function() {
        return sessionStorage.userName;
    }, function(newValue, oldValue) {
        if (newValue)
            $scope.userName = sessionStorage.userName;
        else {
            $scope.userName = "";
            delete $cookies.sessionid;
        }

    });



    /**
     * Отримання імені користувача по кукі
     **/
    function getUserName() {
        Account.getUserName(function(data) {
            sessionStorage.userName = data.user.name + " " + data.user.surname;
        });
    }



    /**
     * Логаут юзера
     **/
    $scope.logoutUser = function() {
        Account.logoutUser(function(data) {
            delete $cookies.sessionid;
        });
    };

    $timeout(function() {
        angular.element(".type-selectpicker").selectpicker({
            style: 'btn-default btn-md',
            container: angular.element("body")
        });
    }, 50);

});