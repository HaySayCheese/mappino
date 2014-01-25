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
     * Ініціалізкація скролбара
     **/
    initScrollbar();


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
     * Створення діалога редагування
     **/
    $scope.createEditTagDialog = function() {
        $scope.closeTagDialog();

        if (!arguments[0])
            $scope.creatingTag = true;
        else {
            $scope.editingTag = angular.copy(arguments[0]);

            var e = arguments[1],
                htmlText = "<div class='tag-edit-panel state-edit'>" +
                                "<span>Пример: </span>" +
                                "<span class='label' style='background-color: [[ editingTag.color ]]'>[[ editingTag.title ]]</span>" +
                                "<div class='form-group'>" +
                                    "<input type='text' class='form-control' ng-model='editingTag.title' select-on-click required>" +
                                "</div>" +
                                "<div class='pick-color-box text-center'>" +
                                    "<div class='color-item' ng-repeat='color in newTag.colors' ng-click='editingTag.color = color' style='background-color: [[ color ]]'></div>" +
                                "</div>" +
                                "<div class='btn-group btn-group-justified'>" +
                                    "<div class='btn btn-cancel btn-block' ng-click='closeTagDialog()'>Отмена</div>" +
                                    "<div class='btn btn-success btn-block btn-creating' data-loading-text='Применение...' ng-click='editTag(editingTag)'>Применить</div>" +
                                "</div>" +
                            "</div>",
            template = angular.element($compile(htmlText)($scope));

            angular.element(e.target.parentNode.parentNode).after(template);
        }
    };


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
                color: $scope.newTag.selectedColor,
                color_id: $scope.tags.indexOf($scope.newTag.selectedColor)
            });

            $scope.closeTagDialog();
        });
    };


    /**
     * Логіка редагування тега
     **/
    $scope.editTag = function(tag) {
        var btn = $(".btn-creating").button("loading");

        tagQueries.editTag(tag).success(function() {
            for (var i = 0; i <= $scope.tags.length - 1; i++) {
                if ($scope.tags[i].id == tag.id)
                    $scope.tags[i] = tag;
            }

            btn.button("reset");
        });
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
    $scope.closeTagDialog = function() {
        $scope.newTag.selectedColor = $scope.newTag.defaultColor;
        $scope.newTag.title         = $scope.newTag.defaultTagName;

        $scope.creatingTag = false;

        angular.element(".tag-edit-panel.state-edit").remove();
    }


    /**
     * Функція скролбара
     **/
    function initScrollbar() {
        var sidebar = angular.element(".sidebar-menu-body");

        sidebar.perfectScrollbar({
            wheelSpeed: 20
        });

        angular.element(window).resize(function() {
            sidebar.perfectScrollbar("update");
        });
    }
});