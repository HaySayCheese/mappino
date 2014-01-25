'use strict';

app.controller('SidebarMenuCtrl', function($scope, $rootScope, $routeParams, $timeout, $compile, tagQueries) {

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
        $scope.loadingLabels = true;

        tagQueries.loadTags().success(function(data) {
            for (var i = 0; i <= data.dirtags.length - 1; i++) {
                $scope.tags.push({
                    id: data.dirtags[i].id,
                    title: data.dirtags[i].title,
                    color_id: data.dirtags[i].color_id,
                    color: $scope.newTag.colors[data.dirtags[i].color_id]
                })
            }

            $scope.loadingLabels = false;
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
    $scope.editTag = function(e, tag) {

        $scope.editableTag = tag;

        var popover = $(e.currentTarget),
            menuItem = $(e.currentTarget).parents("li"),
            menuItemLink = menuItem.find("a"),
            popovers = $("[data-toggle='popover']"),
            htmlText = "<div class='add-tag-block'>" +
                            "<div class='form-group'>" +
                                "<span>Пример: </span>" +
                                "<span class='label' style='background-color: [[ newTag.selectedColor ]]'>[[ editableTag.title ]]</span>" +
                            "</div>" +
                            "<div class='form-group'>" +
                                "<input type='text' class='form-control' ng-model='editableTag.title' select-on-click required>" +
                            "</div>" +
                            "<div class='select-color-box text-center'>" +
                                "<div class='select-color-box-item' ng-repeat='color in newTag.colors' ng-click='editableTag.selectedColor = color' style='background-color: [[ color ]]'></div>" +
                            "</div>" +
                            "<div class='btn-group btn-group-justified'>" +
                                "<div class='btn btn-cancel btn-block' ng-click='closeCreateTagDialog()'>Отмена</div>" +
                                "<div class='btn btn-success btn-block btn-creating' data-loading-text='Создание...' ng-click='createTag()'>Создать</div>" +
                            "</div>" +
                        "</div>",
            template = angular.element($compile(htmlText)($scope));


        menuItemLink.hide();
        menuItem.append(template);

        //tagQueries.editTag(tag);
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