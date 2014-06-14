'use strict';

app.controller('SettingsCtrl', function($scope, $rootScope, $timeout, Settings) {

    $rootScope.pageTitle = "Параметры - Mappino";
    $rootScope.loadings.settings = true;

    initScrollBar();
    initInputsChange();
    initDropdowns();


    Settings.load(function(data) {
        $scope.user = data;
        $rootScope.loadings.settings = false;
    });


    /**
     * Ініціалізація діалога загрузки зображення
     */
    $scope.openPhotoDialog = function() {
        $timeout(function() {
            angular.element("input[type='file']").trigger("click");
        }, 0);
    };


    /**
     * Логіка загрузки зображень
     */
    $scope.onFileSelect = function(files) {
        $scope.user.account.avatar_url = "";
        $scope.uploadingAvatar = true;

        Settings.uploadUserPhoto(files[0], function(data) {
            $scope.user = data;
            $scope.uploadingAvatar = false;

            data.code !== 0 ? $scope.avatarErrorCode = data.code : $scope.avatarErrorCode = 0;
        });
    };


    /**
    * При втраті фокуса з інпута
    * викликати запит на відправку на сервер
    */
    function initInputsChange() {
        angular.element(".sidebar-item-detailed-body input[type='text']").bind("focusout", function(e) {
            var name  = e.currentTarget.name,
                value = e.currentTarget.value.replace(/\s+/g, " ");

            if (!$scope.form.user[name].$dirty)
                return;

            if (name == "mobile_phone" && (value == "+38 (0__) __ - __ - ___" || value[22] == "_"))
                return;

            Settings.checkInputs({ f: name, v: value }, function(newValue, code) {
                if (newValue)
                    e.currentTarget.value = newValue;

                $scope.form.user[name].$setValidity("incorrect", code !== 10);
                $scope.form.user[name].$setValidity("duplicated", code !== 11);
            });

        });

        angular.element(".sidebar-item-detailed-body input[type='checkbox']").bind("change", function(e) {
            var name  = e.currentTarget.name,
                value = e.currentTarget.checked;

            Settings.checkInputs({ f: name, v: value }, null);
        });

        angular.element(".sidebar-item-detailed-body select").bind('change',function(e) {
            var name  = e.currentTarget.name,
                value = e.currentTarget.value;

            Settings.checkInputs({ f: name, v: value }, null);
        });
    }


    /**
     * Ініціалізація дропдаунів
     */
    function initDropdowns() {
        angular.element("select").selectpicker({
            style: 'btn-default btn-md'
        });
    }



    /**
     * Функція скролбара
     */
    function initScrollBar() {
        var sidebar = angular.element(".sidebar-item-detailed-body");

        sidebar.perfectScrollbar("destroy");

        sidebar.perfectScrollbar({
            wheelSpeed: 20,
            useKeyboard: false,
            suppressScrollX: true
        });

        angular.element(window).resize(function() {
            sidebar.perfectScrollbar("update");
        });
    }

});