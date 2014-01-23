'use strict';

app.controller('SidebarMenuCtrl', function($scope, $rootScope, $routeParams, tagQueries) {

    loadTags();

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
     * Перегляд за зміною урла для встановлення активного
     * пункту меню
     **/
    $scope.$on("$routeChangeSuccess", function() {
        if ($routeParams.section)
            $scope.section = $routeParams.section;

        if ($routeParams.id)
            $scope.id = $routeParams.id;
    });


    /**
     * Логіка загрузки тегів
     **/
    function loadTags() {
        tagQueries.loadTags().success(function(data) {
            $scope.tags = data.dirtags;
        });
    }


    /**
     * Логіка створення тега
     **/
    $scope.createTag = function() {
        if (!$scope.newTag.tagName && $scope.newTag.tagName === "")
            return;

        var btn = $(".btn-creating").button("loading");

        tagQueries.createTag($scope.newTag).success(function() {
            btn.button("reset");

            $scope.closeCreateTagDialog();
        })
        .error(function() {
            btn.button("reset");
        });
    };


    /**
     * Логіка редагування тега
     **/
    $scope.editTag = function(tag) {
        tagQueries.editTag(tag);
    };


    /**
     * Логіка видалення тега
     **/
    $scope.removeTag = function(tag) {
        tagQueries.removeTag(tag);
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