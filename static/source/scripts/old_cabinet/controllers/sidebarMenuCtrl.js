'use strict';

app.controller('SidebarMenuCtrl', function($scope, $rootScope, $timeout, $location, $compile, Tags, Publication) {

    /**
     * Ініціалізкація компонентів
     */
    initScrollBar();


    /**
     * Ініціалізкація загрузки тегів
     */
    loadTags();


    /**
     * Ініціалізкація отримання кількості оголошень
     */
    Publication.getCounts();


    /**
     * Змінні створення тега
     */
    $scope.newTag = {};
    $scope.tags = [];
    $scope.tagParameters = Tags.getParameters();

    initBaseTagParameters();


    /**
     * Змінні створення оголошення
     */
    $scope.newPublication = {
        tid: Publication.getTypes()[0].id,
        for_sale: true,
        for_rent: false
    };
    $scope.publicationCount = $rootScope.publicationsCount;


    $location.search().cp ? $scope.creatingPublication = true : $scope.creatingPublication = false;



    $scope.returnToMap = function() {
        window.location = localStorage.lastMapUrl || sessionStorage.lastMapUrl || 'map/#!/';
    };


    /**
     * Створення нового оголошенн
     */
    $scope.createPublication = function() {
        var btn = angular.element(".new-pub-toggle .btn-group-justified > .btn-success").button("loading");

        Publication.create($scope.newPublication, function(data) {
            $scope.creatingPublication = false;
            $location.search("cp", null);

            btn.button("reset");
        });
    };


    /**
     * Закриття діалога створення оголошення
     */
    $scope.closeCreatingPublication = function() {
        $scope.creatingPublication = false;
        $location.search("cp", null);
    };


    /**
     * Логіка загрузки тегів
     */
    function loadTags() {
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
            $scope.editingTag = _.clone(arguments[0]);

            var e = arguments[1],
                htmlText = "<div class='tag-edit-toggle state-edit'>" +
                                "<div class='form-group'>" +
                                    "<input type='text' class='form-control' ng-model='editingTag.title' required>" +
                                    "<span class='input-has-error' ng-show='tagNameDuplicated'>Такое имя уже используеться</span>" +
                                "</div>" +
                                "<div class='pick-color-box text-center'>" +
                                    "<div class='color-item' ng-repeat='color in tagParameters.colors' ng-click='editingTag.color = color' style='background-color: [[ color ]]'></div>" +
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
                $scope.editingTag.color_id = $scope.tagParameters.colors.indexOf(newColor);
            });

            angular.element(e.target.parentNode.parentNode).after(template);
        }
    };


    /**
     * Логіка створення тега
     */
    $scope.createTag = function() {
        if (_.isEmpty($scope.newTag.title))
            return;

        $scope.tagNameDuplicated = false;

        var btn = angular.element(".btn-creating").button("loading");

        Tags.create($scope.newTag, function(data) {
            btn.button("reset");

            if (data == "error") {
                $scope.tagNameDuplicated = true;
                return;
            }

            $scope.tags = data;

            $scope.closeTagDialog();
        });
    };


    /**
     * Логіка редагування тега
     */
    $scope.editTag = function(tag) {
        var btn = angular.element(".btn-creating").button("loading");

        Tags.update(tag, function(data) {
            btn.button("reset");

            $scope.tags = data;

            $scope.closeTagDialog();
        });
    };


    /**
     * Логіка видалення тега
     */
    $scope.removeTag = function(tag) {
        Tags.remove(tag, function(data) {
            $scope.tags = data;
        });
    };


    /**
     * Повернення змінних на базові значеня
     * після закриття діалога створення тега
     */
    $scope.closeTagDialog = function() {
        initBaseTagParameters();

        $scope.creatingTag = false;
        angular.element(".tag-edit-toggle.state-edit").remove();
    };


    /**
     * Базові параметри тега
     */
    function initBaseTagParameters() {
        $scope.newTag = {
            title: $scope.tagParameters.default_title,
            selected_color: $scope.tagParameters.default_color
        };
    }



    /**
     * Ініціалізація скролбара
     */
    function initScrollBar() {
        $timeout(function() {

            var sidebar = angular.element(".sidebar-menu-body");

            sidebar.perfectScrollbar("destroy");
            sidebar.perfectScrollbar({
                wheelSpeed: 10,
                useKeyboard: false
            });

            angular.element(window).resize(function() {
                sidebar.perfectScrollbar("update")
            });

        }, 50);
    }
});