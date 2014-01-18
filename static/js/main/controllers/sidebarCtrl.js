'use strict';

app.controller('SidebarCtrl', function($scope, $rootScope, $cookies) {

    $scope.userName = "";

    /**
     * Дивимся за кукою сесії, якщо вона є то
     * берем куку з іменем юзера якщо і вона є
     **/
    $scope.$watch(function() {

        return $cookies.sessionid;

    }, function(newValue, oldValue) {

        if ($cookies.userName)
            $scope.userName = $cookies.userName;
        else
            $scope.userName = "";
    });


    /**
     * Дивимся за кукою з іменем юзера, якщо її нема
     * то видаляєм куку сесії
     **/
    $scope.$watch(function() {

        return $cookies.userName;

    }, function(newValue, oldValue) {

        if (!$cookies.userName)
            delete $cookies.sessionid;
    });
});