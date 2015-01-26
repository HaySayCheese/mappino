'use strict';


app.controller('FirstEnterCtrl', function($scope, $location, $timeout, $rootScope, $anchorScroll, $window) {
    $rootScope.pageTitle = "Добро пожаловать на mappino"; // translate



    /*
     * $scope variables initialisation
     */
    $scope.home = {
        type: 0,
        operation: 'sale',
        city: "",
        latLng: "",

        /* якщо true — контрол вводу міста на формі підсвітиться,
         * і з’явиться повідомлення про те, що "місто" є необхідним полем.*/
        cityRequired: false
    };



    /*
     * Controls initialisation
     */

    /* За замовчуванням, фонове зображення має бути на всю висоту вікна браузера. */
    $(window).on('resize', function(){
        $('.img-holder.top').css('height', $window.innerHeight + 'px');
    }).resize(); // перший виклик ініціює івент


    /* autocomplete */
    var cityInput = document.getElementById('home-location-autocomplete'),
    autocomplete = new google.maps.places.Autocomplete(cityInput, {
        componentRestrictions: {
            country: "ua"
        }
    });

    /* Google autocomplete після вибору міста із запропонованих підказок не оновлює scope,
     * через що на сторінку пошуку подається не повна адреса, а лише її частина,
     * та, яка була введена вручну користувачем, і на яку angular зміг зреагувати по ng-change.
     *
     * Даний код змушує ангулар оновлювати scope кожного разу при виборі нового місця.
     */
    var geocoder = new google.maps.Geocoder();
    google.maps.event.addListener(autocomplete, 'place_changed', function() {
        geocoder.geocode( { 'address': autocomplete.getPlace().formatted_address}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK)
                $scope.home.latLng = results[0].geometry.location.lat() + "," + results[0].geometry.location.lng();
        });

        $scope.$apply(function(){
            $scope.home.city = autocomplete.getPlace().formatted_address;
        });
    });


    /* modal initialisation */
    var firstEnterModal = angular.element(".first-enter-modal"),
        dropdown = angular.element(".type-selectpicker");
    firstEnterModal.modal();


    $timeout(function() {
        dropdown.selectpicker({
            style: 'btn-default btn-lg'
        });

        /* таймаут необхідний, оскільки в процесі рендеру сторінки
         * фокус декілька разів переходить з рук в руки */
        cityInput.focus();
    }, 500);



    /*
     * $scope logic
     */

    /**
     * Використовується для заповнення строки пошуку даними з підказок під полем.
     * @param city — строка, яку слід вставити в поле.
     */
    $scope.fillSearchSuggest = function(city){
        $scope.home.city = city;

        geocoder.geocode( { 'address': city }, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK)
                $scope.home.latLng = results[0].geometry.location.lat() + "," + results[0].geometry.location.lng();
        });
    };

    /**
     * Викликається кожного разу при зміні строки вводу міста.
     * Використовується для скидання флагу required після кожної зміни поля,
     * щоб коли користувач починає вводити місто, привести поле в стандартний вигляд,
     * навіть, якщо на попередньому етапі воно було підсвіченим.
     */
    $scope.cityInputChanged = function(){
        $scope.home.cityRequired = false;
    };

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
     * Використовується для простановки року у футері.
     * @returns {number}
     */
    $scope.currentYear = function(){
        return new Date().getFullYear();
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