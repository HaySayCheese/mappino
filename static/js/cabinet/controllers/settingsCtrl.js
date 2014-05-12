'use strict';

app.controller('SettingsCtrl', function($scope, $rootScope, $timeout, Settings) {

    $rootScope.loadings.settings = true;

    initScrollBar();
    initInputsChange();
    initDropdowns();


    Settings.load(function(data) {
        $scope.user = data;
        $rootScope.loadings.settings = false;
    });


    /**
    * При втраті фокуса з інпута
    * викликати запит на відправку на сервер
    */
    function initInputsChange() {
        angular.element(".sidebar-item-detailed-body input[type='text']").bind("focusout", function(e) {
            var name  = e.currentTarget.name,
                value = e.currentTarget.value.replace(/\s+/g, " ");

            if (!$scope.form.user[name].$dirty || !value)
                return;

            Settings.checkInputs({ f: name, v: value }, function(newValue, code) {
                if (newValue)
                    e.currentTarget.value = newValue;

                $scope.form.user[name].$setValidity("incorrect", code === 10);
                $scope.form.user[name].$setValidity("duplicated", code === 11);
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
            wheelSpeed: 40,
            useKeyboard: false,
            suppressScrollX: true
        });

        angular.element(window).resize(function() {
            sidebar.perfectScrollbar("update");
        });
    }

});