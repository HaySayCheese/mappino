'use strict';

app.controller('SidebarMenuCtrl', function($scope, $rootScope, $routeParams, tagQueries) {

    loadTags();

    /**
     * Змінні створення тега
     **/
    $scope.newTag = {
        colors:         ["#971a93", "#cf1d4f", "#daad11", "#06b358", "#399b8a", "#1d69cf", "#FFCC33", "#66FF33"],

        defaultTagName: "Название",
        title:          "Название",

        defaultColor:   "#971a93",
        selectedColor:  "#971a93"
    };

    $scope.tags = [];


    /**
     * Перегляд за зміною урла для встановлення активного
     * пункту меню
     **/
    $scope.$on("$routeChangeSuccess", function() {
        if ($routeParams.section) {
            $scope.section = $routeParams.section;
            $scope.tagId = "";
        }


        if ($routeParams.id) {
            $scope.tagId = $routeParams.id;
            $scope.section = "";
        }
    });


    /**
     * Логіка загрузки тегів
     **/
    function loadTags() {
        tagQueries.loadTags().success(function(data) {
            for (var i = 0; i <= data.dirtags.length - 1; i++) {
                $scope.tags.push({
                    id: data.dirtags[i].id,
                    title: data.dirtags[i].title,
                    color_id: data.dirtags[i].color_id
                })
            }
        });
    }


    /**
     * Логіка створення тега
     **/
    $scope.createTag = function() {
        if (!$scope.newTag.tagName && $scope.newTag.tagName === "")
            return;

        var btn = $(".btn-creating").button("loading");

        tagQueries.createTag($scope.newTag).success(function(data) {
            btn.button("reset");

            $scope.tags.push({
                id: data.id,
                title: $scope.newTag.title,
                color_id: $scope.tags.indexOf($scope.newTag.selectedColor)
            });

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
        tagQueries.removeTag(tag.id).success(function() {
            $scope.tags.splice($scope.tags.indexOf(tag), 1);
        });
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