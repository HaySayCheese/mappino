'use strict';

app.controller('SidebarMenuCtrl', function($scope, $rootScope, $timeout, $location, $compile, publicationQueries, tagQueries, Briefs, Tags) {

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
     * Ініціалізація дропдауна
     */
    $timeout(function() {
        angular.element("select[name='typeSelect']").selectpicker({
            style: 'btn-success btn-md'
        });
    }, 50);


    /**
     * Ініціалізкація скролбара
     */
    initScrollBar();


    /**
     * Створення нового оголошенн
     **/
    $scope.createPublication = function() {
        var btn = angular.element(".new-pub-panel .btn-group-justified > .btn-success").button("loading");

        publicationQueries.createPublication($scope.newPublication).success(function(data) {
            $scope.creatingPublication = false;
            btn.button("reset");

            $location.path("/publications/unpublished/" + $scope.newPublication.tid + ":" + data.id);

            if ($rootScope.routeSection === "unpublished")
                Briefs.add({
                    id: data.id,
                    for_rent: $scope.newPublication.for_rent,
                    for_sale: $scope.newPublication.for_sale,
                    photo_url: "",
                    tags: "",
                    title: "",
                    tid: $scope.newPublication.tid
                });

            if (!$scope.$$phase)
                $scope.$apply();
        })
    };


    /**
     * Логіка загрузки тегів
     */
    function loadTags() {
        $scope.tags = [];

        Tags.load(function(data) {
            $scope.tags = data;
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

        var btn = $(".btn-creating").button("loading");

        tagQueries.createTag($scope.newTag).success(function(data) {
            btn.button("reset");

            if (data.code === 1)
                return;

            Tags.add({
                id: data.id,
                title: $scope.newTag.title,
                color: $scope.newTag.selectedColor,
                color_id: $scope.newTag.colors.indexOf($scope.newTag.selectedColor)
            });

            $scope.closeTagDialog();
        });
    };


    /**
     * Логіка редагування тега
     */
    $scope.editTag = function(tag) {
        var btn = $(".btn-creating").button("loading");

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
     * Функція скролбара
     */
    function initScrollBar() {
        var sidebar = angular.element(".sidebar-menu-body");

        sidebar.perfectScrollbar("destroy");
        sidebar.perfectScrollbar({
            wheelSpeed: 20
        });

        angular.element(window).resize(function() {
            sidebar.perfectScrollbar("update");
        });
    }
});