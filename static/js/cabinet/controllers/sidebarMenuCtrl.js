'use strict';

app.controller('SidebarMenuCtrl', function($scope, $rootScope, $routeParams, $timeout, $compile, tagQueries) {

    loadTags();

    /**
     * Змінні створення тега
     **/
    $scope.newTag = {
        colors:         ["#9861dd", "#465eec", "#60b4cf", "#54b198", "#7cc768", "#dfb833", "#f38a23", "#f32363"],

        defaultTagName: "Название",
        title:          "Название",

        defaultColor:   "#9861dd",
        selectedColor:  "#9861dd"
    };

    $rootScope.tags = [];


    $scope.newPublication = {
        tid: $rootScope.publicationTypes[0].id,
        for_sale: true,
        for_rent: false
    };


    /**
     * Ініціалізація дропдауна
     **/
    $timeout(function() {
        angular.element("select[name='typeSelect']").selectpicker({
            style: 'btn-success btn-md'
        });
    }, 50);


    /**
     * Ініціалізкація скролбара
     **/
    initScrollbar();


    /**
     * Створення нового оголошенн
     **/
    $scope.createPublication = function() {
        var btn = angular.element(".new-pub-panel .btn-group-justified > .btn-success").button("loading");

        tagQueries.createPublication($scope.newPublication).success(function() {
            $scope.creatingPublication = false;
            btn.button("reset");
        })
    };


    /**
     * Логіка загрузки тегів
     **/
    function loadTags() {
        $scope.loadingTags = true;

        tagQueries.loadTags().success(function(data) {
            for (var i = 0; i <= data.dirtags.length - 1; i++) {
                $scope.tags.push({
                    id: data.dirtags[i].id,
                    title: data.dirtags[i].title,
                    color_id: data.dirtags[i].color_id,
                    color: $scope.newTag.colors[data.dirtags[i].color_id]
                })
            }

            $scope.loadingTags = false;
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
                                "<div class='form-group'>" +
                                    "<input type='text' class='form-control' ng-model='editingTag.title' required>" +
                                "</div>" +
                                "<div class='pick-color-box text-center'>" +
                                    "<div class='color-item' ng-repeat='color in newTag.colors' ng-click='editingTag.color = color' style='background-color: [[ color ]]'></div>" +
                                "</div>" +
                                "<span>Пример: </span>" +
                                "<span class='label' style='background-color: [[ editingTag.color ]]'>[[ editingTag.title ]]</span>" +
                                "<div class='btn-group btn-group-justified'>" +
                                    "<div class='btn btn-cancel btn-block' ng-click='closeTagDialog()'>Отмена</div>" +
                                    "<div class='btn btn-success btn-block btn-creating' data-loading-text='Применение...' ng-click='editTag(editingTag)'>Применить</div>" +
                                "</div>" +
                            "</div>",
            template = angular.element($compile(htmlText)($scope));

            $scope.$watch("editingTag.color", function(newColor) {
                $scope.editingTag.color_id = $scope.newTag.colors.indexOf(newColor);
            });

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

            if (data.code === 1)
                return;

            $rootScope.tags.push({
                id: data.id,
                title: $scope.newTag.title,
                color: $scope.newTag.selectedColor,
                color_id: $rootScope.tags.indexOf($scope.newTag.selectedColor)
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
            for (var i = 0; i <= $rootScope.tags.length - 1; i++) {
                if ($rootScope.tags[i].id == tag.id)
                    $rootScope.tags[i] = tag;
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