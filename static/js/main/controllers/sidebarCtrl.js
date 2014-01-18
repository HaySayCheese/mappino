'use strict';

app.controller('SidebarCtrl', function($scope, $rootScope, $cookies) {

    $scope.userName = "";

    $scope.$watch(function() {
        return $cookies.sessionid;
    }, function(newValue, oldValue) {
        $scope.userName = $cookies.userName;
    });
});