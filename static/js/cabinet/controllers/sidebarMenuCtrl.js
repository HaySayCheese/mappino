'use strict';

app.controller('SidebarMenuCtrl', function($scope, $rootScope, $compile) {

    /**
     * Змінні створення тега
     **/
    $scope.newTag = {
        colors:         ["#33CCFF", "#33FFCC", "#FF6633", "#FF3366", "#3366FF", "#FF33CC", "#FFCC33", "#66FF33"],

        defaultTagName: "Название",
        tagName:        "Название",

        defaultColor:   "#33CCFF",
        selectedColor:  "#33CCFF"
    };


    /**
     * Повернення змінних на базові значеня
     * після закриття діалога створення тега
     **/
    $scope.closeCreateTagDialog = function() {
        $scope.newTag.selectedColor = $scope.newTag.defaultColor;
        $scope.newTag.tagName       = $scope.newTag.defaultTagName;

        $scope.creatingTag = false;
    }

});