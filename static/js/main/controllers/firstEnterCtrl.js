'use strict';


app.controller('FirstEnterCtrl', function($scope, $location, $timeout, $rootScope, $anchorScroll, $window) {


    /**
     * Викликається при кліку на кнопку "Искать".
     * Перевіряє чи поле вводу міста не пусте, і, якщо все ок —
     * перекидає користувача на сторінку пошуку.
     */
    $scope.startSearch = function(){
        if (! $scope.home.city){
            $scope.home.cityRequired = true; // контроли будуть підсвічені автоматично.
            return;
        }


        $rootScope.$emit("first-enter-done", {
            operation: $scope.home.operation,
            type: $scope.home.type,
            latLng: $scope.home.latLng
        });

        console.log($scope.home.latLng)
        $location.path("/search");
    };

    /**
     * Використовується для переходу по якорям.
     * @param id — id якоря, до якого слід перейти.
     */
    $scope.scrollTo = function(id) {
      $location.hash(id);
      $anchorScroll();
   };
});