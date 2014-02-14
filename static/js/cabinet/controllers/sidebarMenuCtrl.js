'use strict';

app.controller('SidebarMenuCtrl', function($scope, $rootScope, $timeout, $location, $compile, Briefs, Tags, Publication) {

    /**
     * Ініціалізкація компонентів
     */
    initScrollBar();
    initDropDown();


    /**
     * Ініціалізкація загрузки тегів
     */
    loadTags();

    /**
     * Змінні створення тега
     */
    $scope.newTag = Tags.getParameters();
    $scope.tags = [];
    $scope.newPublication = {
        tid: $rootScope.publicationTypes[0].id,
        for_sale: true,
        for_rent: false
    };



    /**
     * Створення нового оголошенн
     */
    $scope.createPublication = function() {
        var btn = angular.element(".new-pub-panel .btn-group-justified > .btn-success").button("loading");

        Publication.create($scope.newPublication, function(data) {
            $scope.creatingPublication = false;

            btn.button("reset");

            $location.path("/publications/unpublished/" + $scope.newPublication.tid + ":" + data.id);

            if (!$scope.$$phase)
                $scope.$apply();
        })
    };


    /**
     * Логіка загрузки тегів
     */
    function loadTags() {
        $scope.tags = [];

        initScrollBar();

        Tags.load(function(data) {
            $scope.tags = data;

            initScrollBar();
        });
    }


    /**
     * Створення діалога редагування
     */
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
     */
    $scope.createTag = function() {
        if (!$scope.newTag.tagName && $scope.newTag.tagName === "")
            return;

        var btn = angular.element(".btn-creating").button("loading");

        Tags.create($scope.newTag, function(status) {
            btn.button("reset");

            if (status === "error")
                return;

            $scope.closeTagDialog();
        });
    };


    /**
     * Логіка редагування тега
     */
    $scope.editTag = function(tag) {
        var btn = angular.element(".btn-creating").button("loading");

        Tags.update(tag, function() {
            btn.button("reset");
        });
    };


    /**
     * Логіка видалення тега
     */
    $scope.removeTag = function(tag) {
        Tags.remove(tag);
    };


    /**
     * Повернення змінних на базові значеня
     * після закриття діалога створення тега
     */
    $scope.closeTagDialog = function() {
        $scope.newTag = angular.copy(Tags.getParameters());
        $scope.creatingTag = false;
        angular.element(".tag-edit-panel.state-edit").remove();
    };


    /**
     * Ініціалізація дропдауна
     */
    function initDropDown() {
        $timeout(function() {
            angular.element("select[name='typeSelect']").selectpicker({
                style: 'btn-success btn-md'
            });
        }, 0);
    }

    /**
     * Ініціалізація скролбара
     */
    function initScrollBar() {
        $timeout(function() {

            var sidebar = angular.element(".sidebar-menu-body");

            sidebar.perfectScrollbar("destroy");
            sidebar.perfectScrollbar({
                wheelSpeed: 20
            });

            angular.element(window).resize(function() {
                sidebar.perfectScrollbar("update")
            });

        }, 50);
    }
});